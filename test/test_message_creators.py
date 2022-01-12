# TODO: Write tests for message creators
from logging import DEBUG, Logger
import logging
from discord_lumberjack.handlers import DiscordWebhookHandler
from discord_lumberjack.handlers.discord_handler import DiscordHandler
from discord_lumberjack.message_creators import (
	EmbedMessageCreator,
	BasicMessageCreator,
)
from pytest import fixture
import os
import random
from discord_lumberjack.message_creators import MessageCreator


@fixture(params=[BasicMessageCreator(), EmbedMessageCreator()])
def message_creator(request) -> MessageCreator:
	return request.param


@fixture
def handler(message_creator: MessageCreator) -> DiscordWebhookHandler:
	return DiscordWebhookHandler(
		url=os.environ["WEBHOOK_URL"], level=DEBUG, message_creator=message_creator,
	)


@fixture
def logger(handler: DiscordHandler) -> Logger:
	_logger = logging.getLogger(f"{__name__}.{random.random()}")
	_logger.setLevel(logging.DEBUG)
	_logger.addHandler(handler)
	return _logger


def test_message_creators(logger: Logger):
	logger.debug("This is a debug message.")
	try:
		raise ValueError("This is a test ValueError exception.")
	except ValueError:
		logger.exception("An exception was thrown.")
