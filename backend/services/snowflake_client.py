"""
Snowflake client for read-only analytics queries.

Auth is a Programmatic Access Token (PAT), not key-pair or password. The PAT is
role-restricted to HALO_ANALYST_ADMIN in Snowflake, but that role is *not* scoped
read-only, so every query issued through this module is forced through
`assert_read_only()` before it reaches Snowflake. See BOTTLENECKS.md — this is a
stopgap until a properly scoped service account exists.
"""

from __future__ import annotations

import re
import threading
from typing import Any, Dict, List, Optional, Sequence, Tuple

from backend.utils.config import Config
from backend.utils.logging import get_logger

logger = get_logger('snowflake_client')

# Statements that mutate data/schema or change grants. Word-boundary matched against
# SQL with string literals, quoted identifiers and comments already stripped out.
_FORBIDDEN_KEYWORDS = (
    'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'MERGE', 'TRUNCATE', 'GRANT',
)
_FORBIDDEN_RE = re.compile(r'\b(' + '|'.join(_FORBIDDEN_KEYWORDS) + r')\b', re.IGNORECASE)

# Read-only statement openers we allow. DESCRIBE/SHOW are needed for schema discovery.
_ALLOWED_OPENERS = ('SELECT', 'WITH', 'DESCRIBE', 'DESC', 'SHOW')
_OPENER_RE = re.compile(r'^\s*(' + '|'.join(_ALLOWED_OPENERS) + r')\b', re.IGNORECASE)

_LINE_COMMENT_RE = re.compile(r'--[^\n]*')
_BLOCK_COMMENT_RE = re.compile(r'/\*.*?\*/', re.DOTALL)
_SINGLE_QUOTED_RE = re.compile(r"'(?:[^']|'')*'", re.DOTALL)
_DOUBLE_QUOTED_RE = re.compile(r'"(?:[^"]|"")*"', re.DOTALL)


class ReadOnlyQueryError(ValueError):
    """Raised when a query fails the read-only guardrail (never sent to Snowflake)."""


class _Unset:
    """Sentinel so an explicit `token=None` means "no token", not "read the env"."""

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return '<unset>'


_UNSET = _Unset()


def _strip_noise(sql: str) -> str:
    """
    Remove comments, string literals and quoted identifiers.

    Without this, `WHERE status_label = 'Pending Update'` would trip the UPDATE
    check, and a keyword buried in a comment would too.
    """
    stripped = _BLOCK_COMMENT_RE.sub(' ', sql)
    stripped = _LINE_COMMENT_RE.sub(' ', stripped)
    stripped = _SINGLE_QUOTED_RE.sub("''", stripped)
    stripped = _DOUBLE_QUOTED_RE.sub('""', stripped)
    return stripped


def assert_read_only(sql: str) -> None:
    """
    Reject anything that isn't a single read-only statement.

    Raises:
        ReadOnlyQueryError: multi-statement, non-SELECT opener, or a mutating keyword.
    """
    if not sql or not sql.strip():
        raise ReadOnlyQueryError('Empty query')

    stripped = _strip_noise(sql)

    # Multi-statement guards against `SELECT 1; DROP TABLE t` slipping past the opener check.
    statements = [s for s in stripped.split(';') if s.strip()]
    if len(statements) > 1:
        raise ReadOnlyQueryError(
            f'Only one statement per query is allowed (found {len(statements)})'
        )

    if not _OPENER_RE.match(stripped):
        opener = (stripped.strip().split() or ['<empty>'])[0]
        raise ReadOnlyQueryError(
            f"Query must start with one of {', '.join(_ALLOWED_OPENERS)} (got '{opener}')"
        )

    match = _FORBIDDEN_RE.search(stripped)
    if match:
        raise ReadOnlyQueryError(
            f"Query contains forbidden keyword '{match.group(1).upper()}'; "
            'this connection is read-only'
        )


class SnowflakeClient:
    """
    Thin read-only wrapper over snowflake-connector-python.

    Connections are opened per query rather than pooled: this feature runs a handful
    of cached queries per 15-minute window, so a pool would add failure modes
    (stale sockets, token refresh) for no measurable gain.
    """

    def __init__(
        self,
        account: Any = _UNSET,
        user: Any = _UNSET,
        token: Any = _UNSET,
        role: Any = _UNSET,
        warehouse: Any = _UNSET,
        database: Any = _UNSET,
        schema: Any = _UNSET,
    ):
        # Omitted args fall back to Config; an explicitly passed None stays None, so
        # tests can construct an unconfigured client without ambient env bleeding in.
        def pick(value: Any, fallback: Any) -> Any:
            return fallback if isinstance(value, _Unset) else value

        self.account = pick(account, Config.SNOWFLAKE_ACCOUNT)
        self.user = pick(user, Config.SNOWFLAKE_USER)
        self.token = pick(token, Config.SNOWFLAKE_PAT)
        self.role = pick(role, Config.SNOWFLAKE_ROLE)
        self.warehouse = pick(warehouse, Config.SNOWFLAKE_WAREHOUSE)
        self.database = pick(database, Config.SNOWFLAKE_DATABASE)
        self.schema = pick(schema, Config.SNOWFLAKE_SCHEMA)

    def is_configured(self) -> bool:
        """True when enough config is present to attempt a connection."""
        return bool(self.account and self.user and self.token)

    def _connect(self):
        if not self.is_configured():
            missing = [
                name for name, value in (
                    ('SNOWFLAKE_ACCOUNT', self.account),
                    ('SNOWFLAKE_USER', self.user),
                    ('SNOWFLAKE_PAT', self.token),
                )
                if not value
            ]
            raise ValueError(
                f"Snowflake is not configured (missing: {', '.join(missing)}). "
                'Set these in .env — see env.example.'
            )

        try:
            import snowflake.connector
        except ImportError as exc:  # pragma: no cover - import guard
            raise RuntimeError(
                'snowflake-connector-python is not installed; '
                'run pip install -r requirements.txt'
            ) from exc

        return snowflake.connector.connect(
            account=self.account,
            user=self.user,
            token=self.token,
            authenticator='PROGRAMMATIC_ACCESS_TOKEN',
            role=self.role,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema,
            client_session_keep_alive=False,
            login_timeout=Config.SNOWFLAKE_LOGIN_TIMEOUT_SEC,
            network_timeout=Config.SNOWFLAKE_QUERY_TIMEOUT_SEC,
        )

    def run_select(
        self,
        sql: str,
        params: Optional[Sequence[Any]] = None,
        max_rows: Optional[int] = None,
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Execute a read-only query and return (column_names, rows_as_dicts).

        Args:
            sql: A single SELECT/WITH/DESCRIBE/SHOW statement. Bind filter values
                 with %s placeholders rather than string interpolation.
            params: Bind parameters for the %s placeholders.
            max_rows: Stop fetching after this many rows (None = all).

        Raises:
            ReadOnlyQueryError: if the guardrail rejects the query.
        """
        assert_read_only(sql)

        conn = self._connect()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    sql,
                    tuple(params) if params else None,
                    timeout=Config.SNOWFLAKE_QUERY_TIMEOUT_SEC,
                )
                columns = [col[0] for col in (cursor.description or [])]
                if max_rows is not None:
                    raw_rows = cursor.fetchmany(max_rows)
                else:
                    raw_rows = cursor.fetchall()
                rows = [dict(zip(columns, row)) for row in raw_rows]
                logger.info(
                    'Snowflake query returned %d row(s), %d column(s)', len(rows), len(columns)
                )
                return columns, rows
            finally:
                cursor.close()
        finally:
            conn.close()

    def describe_table(self, table: str) -> List[Dict[str, Any]]:
        """
        DESCRIBE TABLE for schema discovery.

        The table name is validated against a strict identifier pattern rather than
        bound as a parameter, because Snowflake does not accept binds for identifiers.
        """
        if not re.fullmatch(r'[A-Za-z_][\w$]*(\.[A-Za-z_][\w$]*){0,2}', table):
            raise ValueError(f'Invalid table identifier: {table!r}')
        _, rows = self.run_select(f'DESCRIBE TABLE {table}')
        return rows


_CLIENT_LOCK = threading.Lock()
_CLIENT: Optional[SnowflakeClient] = None


def get_snowflake_client() -> SnowflakeClient:
    """Shared client instance (config is read once at first use)."""
    global _CLIENT
    with _CLIENT_LOCK:
        if _CLIENT is None:
            _CLIENT = SnowflakeClient()
        return _CLIENT
