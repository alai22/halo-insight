"""
Backward-compatible re-export — shared formatter lives in slack_bot.slack_format.
"""

from backend.services.slack_bot.slack_format import to_slack_mrkdwn

__all__ = ['to_slack_mrkdwn']
