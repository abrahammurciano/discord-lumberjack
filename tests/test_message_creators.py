from logging import LogRecord, Logger
from typing import Callable
from discord_lumberjack.message_creators import MessageCreator, EmbedMessageCreator
from tests.utils import assert_messages_sent


def test_message_creators(logger: Logger, function_that_raises: Callable[[], None]):
	logger.debug("This is a debug message.")
	try:
		function_that_raises()
	except ValueError:
		logger.exception("An exception was thrown.")
	assert_messages_sent(logger)


def test_messages(message_creator: MessageCreator, record: LogRecord):
	messages = message_creator.messages(record, lambda _: "Formatted record")
	assert messages, "Messages should not be empty."
	for message in messages:
		has_content = "content" in message and bool(message["content"])
		has_embeds = "embeds" in message and bool(message["embeds"])
		assert has_content or has_embeds, "Message should have content or embeds."
		if has_content:
			assert isinstance(
				message["content"], str
			), "Message content should be a string."
		if has_embeds:
			for embed in message["embeds"]:
				for field in embed["fields"]:
					assert isinstance(field, dict), "Embed field should be a dict."
					assert field["name"], "Embed field should have a name."
					assert field["value"], "Embed field should have a value."


def test_long_log_message(logger: Logger):
	logger.info(
		"This is a long message that should be split into multiple messages." * 100
	)
	assert_messages_sent(logger)


def test_long_message_field_order(
	embed_message_creator: EmbedMessageCreator, long_record: LogRecord
):
	msgs = list(embed_message_creator.messages(long_record, lambda _: ""))
	assert msgs, "Messages should not be empty."
	embed1 = msgs[0]["embeds"][0]
	embed2 = msgs[0]["embeds"][1]
	assert (
		not embed1["description"] and embed2["description"]
	), "Description should be in the second embed, not the first."
  