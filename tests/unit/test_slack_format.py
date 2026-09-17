"""
Unit tests for Slack mrkdwn formatting (shared by Ops and Product bots).
"""

from backend.services.slack_bot.slack_format import to_slack_mrkdwn


class TestToSlackMrkdwn:
    def test_converts_headers_to_bold(self):
        text = '# Halo Health: Components\n\n## What It Is\n\nBody here.'
        out = to_slack_mrkdwn(text)
        assert '# ' not in out
        assert '## ' not in out
        assert '*Halo Health: Components*' in out
        assert '*What It Is*' in out
        assert 'Body here.' in out

    def test_converts_double_asterisk_bold(self):
        text = '**Hardware:**\n- **Harness Insert** – measures activity'
        out = to_slack_mrkdwn(text)
        assert '**' not in out
        assert '*Hardware:*' in out
        assert '*Harness Insert*' in out

    def test_leaves_single_asterisk_bold(self):
        text = '*Already Slack bold*\n- item'
        out = to_slack_mrkdwn(text)
        assert '*Already Slack bold*' in out

    def test_empty(self):
        assert to_slack_mrkdwn('') == ''
        assert to_slack_mrkdwn(None) is None

    def test_product_reexport_matches_shared(self):
        from backend.services.product_bot.slack_format import (
            to_slack_mrkdwn as product_fn,
        )

        sample = '# Title\n\n**Bold** item'
        assert product_fn(sample) == to_slack_mrkdwn(sample)
