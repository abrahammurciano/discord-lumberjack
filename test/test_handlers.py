from unittest.mock import patch
import threading
import logging
from typing import Any, Callable, Dict, Generator, Iterable, Optional
from pytest import fixture, raises
from logging import LogRecord, Logger
from discord_lumberjack.handler import (
	DiscordHandler,
	DiscordChannelHandler,
	DiscordWebhookHandler,
	DiscordDMHandler,
)
from discord_lumberjack.message_creators import MessageCreator
import random
import os


@fixture
def broken_message_creator() -> MessageCreator:
	"""Return a message creator that creates messages with extra fields."""

	class BrokenMessageCreator(MessageCreator):
		def messages(self, record: LogRecord, format_func) -> Iterable[Dict[str, Any]]:
			return [{"content": format_func(record), "extra_field": "extra_value"}]

	return BrokenMessageCreator()


@fixture
def handler_with_broken_creator(broken_message_creator) -> DiscordHandler:
	return DiscordHandler(
		url="https://discordapp.com/api/webhooks/123456789/abcdefghijklmnopqrstuvwxyz",
		message_creator=broken_message_creator,
		allowed_fields=("content",),
	)


@fixture
def record() -> LogRecord:
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


@fixture(autouse=True)
def raise_exceptions_in_threads() -> Generator[None, None, None]:
	"""
	Replaces Thread with a a wrapper to record any exceptions and re-raise them after test execution.
	In case multiple threads raise exceptions only one will be raised.
	"""

	class ThreadWrapper(threading.Thread):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.last_exception: Optional[BaseException] = None

		def run(self):
			try:
				super().run()
			except BaseException as e:
				self.last_exception = e

		def join(self, timeout: float | None = None) -> None:
			super().join(timeout=timeout)
			if self.last_exception:
				raise self.last_exception

	with patch("threading.Thread", ThreadWrapper):
		yield


@fixture(
	params=[
		lambda: DiscordWebhookHandler(
			os.environ["WEBHOOK_URL"], username="Test Webhook Handler"
		),
		lambda: DiscordChannelHandler(
			os.environ["BOT_TOKEN"], int(os.environ["CHANNEL_ID"])
		),
		lambda: DiscordDMHandler(
			os.environ["BOT_TOKEN"], int(os.environ["DISCORD_DM_ID"])
		),
	]
)
def handler(request) -> DiscordHandler:
	_handler = request.param()
	_handler.setFormatter(
		logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	)
	return _handler


@fixture
def handler_with_untextable_user() -> DiscordDMHandler:
	return DiscordDMHandler(
		os.environ["BOT_TOKEN"], int(os.environ["DISCORD_UNTEXTABLE_DM_ID"])
	)


@fixture
def logger(handler: DiscordHandler) -> Logger:
	_logger = logging.getLogger(f"{__name__}.{random.random()}")
	_logger.setLevel(logging.DEBUG)
	_logger.addHandler(handler)
	return _logger


@fixture
def logger_with_untextable_user(
	handler_with_untextable_user: DiscordDMHandler,
) -> Logger:
	_logger = logging.getLogger(f"{__name__}.{random.random()}")
	_logger.setLevel(logging.DEBUG)
	_logger.addHandler(handler_with_untextable_user)
	return _logger


def test_allowed_fields(handler_with_broken_creator: DiscordHandler, record: LogRecord):
	"""Test that only allowed fields are present in the message dict."""
	messages = handler_with_broken_creator.prepare_messages(record)
	for message in messages:
		assert tuple(message.keys()) == ("content",)


def test_handler(logger: Logger):
	"""Log a message with each handler."""
	logger.info(f"test_webhook_handler passed successfully.")
	for thread in threading.enumerate():
		if thread.name == "DiscordLumberjack":
			thread.join()


def test_untextable_user(logger_with_untextable_user: Logger):
	"""Log a message with each handler."""
	with raises(RuntimeError):
		logger_with_untextable_user.info(f"test_webhook_handler passed successfully.")
		for thread in threading.enumerate():
			if thread.name == "DiscordLumberjack":
				thread.join()
