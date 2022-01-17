from pytest import fixture
from typing import Callable
import os
import logging
from logging import LogRecord, Logger
from tests import utils
from dotenv import load_dotenv
from discord_lumberjack.handlers import DiscordHandler, DiscordDMHandler
from discord_lumberjack.message_creators import (
	BasicMessageCreator,
	EmbedMessageCreator,
	MessageCreator,
)

load_dotenv()


@fixture(
	params=[
		BasicMessageCreator(),
		EmbedMessageCreator(),
		utils.CustomEmbedMessageCreator(),
	]
)
def message_creator(request) -> MessageCreator:
	return request.param


@fixture
def embed_message_creator() -> EmbedMessageCreator:
	return EmbedMessageCreator()


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


@fixture
def long_record() -> LogRecord:
	return logging.LogRecord(
		name="long_record",
		level=logging.DEBUG,
		pathname="/this/path/should/be/in/second/embed",
		lineno=1,
		msg="This message is more than 256 characters. " * 8,
		args=(),
		exc_info=None,
	)


@fixture(params=utils.handler_factories)
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
	return utils.logger([handler], handler.__class__.name or "unknown_handler")


@fixture
def logger_with_untextable_user(
	handler_with_untextable_user: DiscordDMHandler,
) -> Logger:
	return utils.logger(
		[handler_with_untextable_user],
		f"{handler_with_untextable_user.__class__.name}_with_untextable_user",
	)


@fixture
def logger_with_all_handlers(message_creator: MessageCreator) -> Logger:
	return utils.logger(
		(factory(message_creator) for factory in utils.handler_factories),
		"all_handlers",
	)


@fixture
def function_that_raises() -> Callable[[], None]:
	def _function_that_raises():
		raise ValueError("This is a test ValueError exception.")

	return _function_that_raises
