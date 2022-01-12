from pytest import fixture
from unittest.mock import patch
from typing import Generator, Optional, Callable
import threading
import os
import logging
from logging import LogRecord, Logger
import random
from discord_lumberjack.handlers import (
	DiscordHandler,
	DiscordChannelHandler,
	DiscordWebhookHandler,
	DiscordDMHandler,
)
from discord_lumberjack.message_creators import (
	BasicMessageCreator,
	EmbedMessageCreator,
	MessageCreator,
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


@fixture
def wait_for_messages() -> Callable[[], None]:
	"""
	Waits for all message threads to finish.
	"""

	def _wait_for_messages() -> None:
		for thread in threading.enumerate():
			if thread.name == "DiscordLumberjack":
				thread.join()

	return _wait_for_messages


class CustomEmbedMessageCreator(EmbedMessageCreator):
	pass


@fixture(
	params=[BasicMessageCreator(), EmbedMessageCreator(), CustomEmbedMessageCreator()]
)
def message_creator(request) -> MessageCreator:
	return request.param


@fixture
def record() -> LogRecord:
	return logging.LogRecord(
		name="dummy_record",
		level=logging.DEBUG,
		pathname="path/to/dummy/file.py",
		lineno=1,
		msg="This is a dummy log record.",
		args=(),
		exc_info=None,
	)


@fixture(
	params=[
		lambda message_creator: DiscordWebhookHandler(
			os.environ["WEBHOOK_URL"],
			username="Webhook Handler",
			message_creator=message_creator,
		),
		lambda message_creator: DiscordChannelHandler(
			os.environ["BOT_TOKEN"],
			int(os.environ["CHANNEL_ID"]),
			message_creator=message_creator,
		),
		lambda message_creator: DiscordDMHandler(
			os.environ["BOT_TOKEN"],
			int(os.environ["DISCORD_DM_ID"]),
			message_creator=message_creator,
		),
	]
)
def handler(message_creator: MessageCreator, request) -> DiscordHandler:
	_handler = request.param(message_creator)
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


@fixture
def function_that_raises() -> Callable[[], None]:
	def _function_that_raises():
		raise ValueError("This is a test ValueError exception.")

	return _function_that_raises