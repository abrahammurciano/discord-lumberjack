import logging
from typing import Any, Dict, Iterable
from pytest import fixture
from logging import LogRecord
from discord_lumberjack.handler import DiscordHandler
from discord_lumberjack.message_creator import MessageCreator


class TestHandler:
	@fixture
	def broken_message_creator(self) -> MessageCreator:
		"""Return a message creator that creates messages with extra fields."""

		class BrokenMessageCreator(MessageCreator):
			def messages(
				self, record: LogRecord, format_func
			) -> Iterable[Dict[str, Any]]:
				return [{"content": format_func(record), "extra_field": "extra_value"}]

		return BrokenMessageCreator()

	@fixture
	def handler(self, broken_message_creator) -> DiscordHandler:
		return DiscordHandler(
			url="https://discordapp.com/api/webhooks/123456789/abcdefghijklmnopqrstuvwxyz",
			message_creator=broken_message_creator,
			allowed_fields=("content",),
		)

	@fixture
	def record(self) -> LogRecord:
		return LogRecord(
			name="test_name",
			level=logging.DEBUG,
			pathname="test_path",
			lineno=1,
			msg="test_message",
			args=None,
			exc_info=None,
			func=None,
		)

	def test_allowed_fields(self, handler: DiscordHandler, record: LogRecord):
		"""Test that only allowed fields are present in the message dict."""
		messages = handler.prepare_messages(record)
		for message in messages:
			assert tuple(message.keys()) == ("content",)