from logging import LogRecord, Logger
from typing import Callable
from discord_lumberjack.message_creators import MessageCreator
from discord_lumberjack.message_creators.embed import EmbedField


def test_message_creators(
	logger: Logger,
	function_that_raises: Callable[[], None],
	wait_for_messages: Callable[[], None],
):
	logger.debug("This is a debug message.")
	try:
		function_that_raises()
	except ValueError:
		logger.exception("An exception was thrown.")
	wait_for_messages()


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