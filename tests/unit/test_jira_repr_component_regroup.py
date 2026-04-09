"""Tests for component-grouped reprioritization markdown (post-validate)."""

from backend.api.routes.jira_routes import (
    _extract_reprioritization_keys,
    _regroup_reprioritization_section_by_component,
    _validate_reprioritization_rows,
)


def _issue(key, components=None, component=None, priority='Major'):
    row = {
        'key': key,
        'title': 'T',
        'priority': priority,
        'status': 'Open',
    }
    if components is not None:
        row['components'] = components
    if component is not None:
        row['component'] = component
    return row


def _mk_table(*data_rows: str) -> str:
    return '\n'.join(
        [
            '### Recommended Jira priority changes',
            '',
            '| Ticket | Title | Current priority | Jira priority recommendation | Reason |',
            '|---|---|---|---|---|',
            *data_rows,
            '',
        ]
    )


def test_regroup_splits_ios_android_both_other():
    md = _mk_table(
        '| HALO-1 | a | Major | Lower to Normal | r |',
        '| HALO-2 | b | Major | Lower to Normal | r |',
        '| HALO-3 | c | Major | Lower to Normal | r |',
        '| HALO-4 | d | Major | Lower to Normal | r |',
    )
    cleaned, _ = _validate_reprioritization_rows(
        md,
        {
            'HALO-1': 'major',
            'HALO-2': 'major',
            'HALO-3': 'major',
            'HALO-4': 'major',
        },
    )
    issues = [
        _issue('HALO-1', components=['iOS']),
        _issue('HALO-2', components=['Android']),
        _issue('HALO-3', components=['iOS', 'Android']),
        _issue('HALO-4', components=['Backend']),
    ]
    out = _regroup_reprioritization_section_by_component(cleaned, issues)

    assert '#### iOS' in out
    assert '#### Android' in out
    assert '#### iOS and Android' in out
    assert '#### Other components' in out

    ios_i = out.index('#### iOS')
    and_i = out.index('#### Android')
    both_i = out.index('#### iOS and Android')
    other_i = out.index('#### Other components')
    assert ios_i < and_i < both_i < other_i

    assert 'HALO-1' in out[ios_i:and_i]
    assert 'HALO-2' in out[and_i:both_i]
    assert 'HALO-3' in out[both_i:other_i]
    assert 'HALO-4' in out[other_i:]


def test_regroup_unknown_key_goes_to_other():
    md = _mk_table('| HALO-99 | x | Major | Lower to Normal | r |')
    cleaned, _ = _validate_reprioritization_rows(md, {'HALO-99': 'major'})
    out = _regroup_reprioritization_section_by_component(cleaned, [])
    assert '#### Other components' in out
    assert 'HALO-99' in out
    assert '#### iOS' not in out


def test_regroup_prose_only_unchanged():
    md = (
        '### Recommended Jira priority changes\n'
        '\n'
        'No priority changes recommended for this backlog.\n'
    )
    out = _regroup_reprioritization_section_by_component(md, [])
    assert out == md


def test_regroup_preserves_leading_prose():
    md = (
        '### Recommended Jira priority changes\n'
        '\n'
        'Summary line before table.\n'
        '\n'
        '| Ticket | Title | Current priority | Jira priority recommendation | Reason |\n'
        '|---|---|---|---|---|\n'
        '| HALO-1 | a | Major | Lower to Normal | r |\n'
    )
    cleaned, _ = _validate_reprioritization_rows(md, {'HALO-1': 'major'})
    issues = [_issue('HALO-1', components=['iOS'])]
    out = _regroup_reprioritization_section_by_component(cleaned, issues)
    assert 'Summary line before table.' in out
    assert out.index('Summary line before table.') < out.index('#### iOS')


def test_regroup_legacy_four_column_table():
    md = '\n'.join(
        [
            '### Recommended Jira priority changes',
            '',
            '| Ticket | Current priority | Jira priority recommendation | Reason |',
            '|---|---|---|---|',
            '| HALO-1 | Major | Lower to Normal | r |',
            '',
        ]
    )
    cleaned, _ = _validate_reprioritization_rows(md, {'HALO-1': 'major'})
    issues = [_issue('HALO-1', components=['Android'])]
    out = _regroup_reprioritization_section_by_component(cleaned, issues)
    assert '#### Android' in out
    assert '| Ticket | Current priority |' in out
    assert 'HALO-1' in out


def test_extract_keys_after_regroup():
    md = _mk_table(
        '| HALO-1 | a | Major | Lower to Normal | r |',
        '| HALO-2 | b | Major | Lower to Normal | r |',
    )
    cleaned, _ = _validate_reprioritization_rows(
        md,
        {'HALO-1': 'major', 'HALO-2': 'major'},
    )
    issues = [
        _issue('HALO-1', components=['iOS']),
        _issue('HALO-2', components=['Android']),
    ]
    regrouped = _regroup_reprioritization_section_by_component(cleaned, issues)
    keys = _extract_reprioritization_keys(regrouped)
    assert keys == ['HALO-1', 'HALO-2']
