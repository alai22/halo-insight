"""
Tests for the Snowflake read-only guardrail.

The PAT is role-restricted to HALO_ANALYST_ADMIN, which can write. assert_read_only()
is the only thing standing between this feature and a mutating statement, so it gets
tested harder than the rest of the feature.
"""

import pytest

from backend.services.snowflake_client import (
    ReadOnlyQueryError,
    assert_read_only,
)

TABLE = 'DBT_CORE_PROD.silver_ops.order_fulfillment_tracking'


class TestAllowsReadOnly:
    @pytest.mark.parametrize('sql', [
        f'SELECT * FROM {TABLE} LIMIT 5',
        f'select order_number from {TABLE}',
        f'  \n SELECT 1 FROM {TABLE}',
        f'WITH open_orders AS (SELECT * FROM {TABLE}) SELECT * FROM open_orders',
        f'DESCRIBE TABLE {TABLE}',
        f'DESC TABLE {TABLE}',
        'SHOW TABLES IN SCHEMA DBT_CORE_PROD.silver_ops',
        f'SELECT * FROM {TABLE};',  # single trailing semicolon is fine
    ])
    def test_permitted(self, sql):
        assert_read_only(sql)

    def test_literal_containing_keyword_is_not_rejected(self):
        """`status_label = 'Pending Update'` must not trip the UPDATE check."""
        assert_read_only(
            f"SELECT * FROM {TABLE} WHERE status_label = 'Pending Billing/Update'"
        )

    def test_column_names_prefixed_with_keywords_are_fine(self):
        """created_at / updated_at must not trip CREATE / UPDATE."""
        assert_read_only(
            f'SELECT created_at, updated_at, deleted_flag FROM {TABLE}'
        )

    def test_comment_mentioning_keyword_is_not_rejected(self):
        assert_read_only(
            f'-- do not DROP this table\nSELECT order_number FROM {TABLE}'
        )
        assert_read_only(
            f'/* TRUNCATE is forbidden here */ SELECT order_number FROM {TABLE}'
        )


class TestRejectsMutations:
    @pytest.mark.parametrize('keyword', [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'MERGE', 'TRUNCATE', 'GRANT',
    ])
    def test_each_forbidden_keyword_as_leading_statement(self, keyword):
        with pytest.raises(ReadOnlyQueryError):
            assert_read_only(f'{keyword} SOMETHING FROM {TABLE}')

    @pytest.mark.parametrize('keyword', [
        'insert', 'UpDaTe', 'DELETE', 'drop', 'Alter', 'CREATE', 'merge', 'Truncate', 'grant',
    ])
    def test_case_insensitive_when_smuggled_after_select(self, keyword):
        with pytest.raises(ReadOnlyQueryError, match='forbidden keyword'):
            assert_read_only(f'SELECT * FROM {TABLE} WHERE 1=1 {keyword} x')

    def test_stacked_statement_is_rejected(self):
        with pytest.raises(ReadOnlyQueryError, match='one statement'):
            assert_read_only(f'SELECT 1 FROM {TABLE}; DROP TABLE {TABLE}')

    def test_stacked_statement_of_two_selects_is_still_rejected(self):
        """Even benign stacking is refused — it is the vector, not the payload."""
        with pytest.raises(ReadOnlyQueryError, match='one statement'):
            assert_read_only('SELECT 1; SELECT 2')

    def test_keyword_hidden_after_a_comment_terminator(self):
        with pytest.raises(ReadOnlyQueryError, match='forbidden keyword'):
            assert_read_only(f'SELECT 1 FROM {TABLE} /* ok */ DELETE FROM {TABLE}')

    def test_cte_wrapping_a_mutation_is_rejected(self):
        with pytest.raises(ReadOnlyQueryError, match='forbidden keyword'):
            assert_read_only(
                f'WITH x AS (SELECT 1) INSERT INTO {TABLE} SELECT * FROM x'
            )

    def test_call_procedure_is_rejected(self):
        with pytest.raises(ReadOnlyQueryError, match='must start with'):
            assert_read_only('CALL some_procedure()')

    def test_copy_into_is_rejected(self):
        with pytest.raises(ReadOnlyQueryError, match='must start with'):
            assert_read_only(f'COPY INTO {TABLE} FROM @stage')

    @pytest.mark.parametrize('sql', ['', '   ', '\n\t'])
    def test_empty_is_rejected(self, sql):
        with pytest.raises(ReadOnlyQueryError, match='Empty query'):
            assert_read_only(sql)


class TestDescribeTableIdentifierValidation:
    """describe_table interpolates the identifier, so it must validate it."""

    @pytest.mark.parametrize('bad', [
        'tbl; DROP TABLE x',
        'tbl WHERE 1=1',
        'a.b.c.d',
        '',
        '1bad',
        'tbl--comment',
        "tbl' OR '1'='1",
    ])
    def test_rejects_non_identifier(self, bad):
        from backend.services.snowflake_client import SnowflakeClient

        client = SnowflakeClient(account='a', user='u', token='t')
        with pytest.raises(ValueError, match='Invalid table identifier'):
            client.describe_table(bad)


class TestClientConfiguration:
    def test_is_configured_false_without_token(self):
        from backend.services.snowflake_client import SnowflakeClient

        assert not SnowflakeClient(account='a', user='u', token=None).is_configured()

    def test_is_configured_true_with_token(self):
        from backend.services.snowflake_client import SnowflakeClient

        assert SnowflakeClient(account='a', user='u', token='tok').is_configured()

    def test_connect_names_missing_settings(self):
        from backend.services.snowflake_client import SnowflakeClient

        client = SnowflakeClient(account='a', user='u', token=None)
        with pytest.raises(ValueError, match='SNOWFLAKE_PAT'):
            client._connect()

    def test_run_select_never_connects_when_guard_rejects(self, monkeypatch):
        """The guardrail must run before any connection attempt."""
        from backend.services.snowflake_client import SnowflakeClient

        client = SnowflakeClient(account='a', user='u', token='tok')

        def _boom():
            raise AssertionError('_connect() must not be reached for a rejected query')

        monkeypatch.setattr(client, '_connect', lambda: _boom())
        with pytest.raises(ReadOnlyQueryError):
            client.run_select(f'DROP TABLE {TABLE}')
