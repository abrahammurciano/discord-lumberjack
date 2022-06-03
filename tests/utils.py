import os
from typing import Callable, Iterable, List, Tuple
from logging import LogRecord, Logger
import logging
import random
from discord_lumberjack.handlers import (
    DiscordHandler,
    DiscordWebhookHandler,
    DiscordChannelHandler,
    DiscordDMHandler,
)
from discord_lumberjack.message_creators import EmbedMessageCreator, MessageCreator
from discord_lumberjack.message_creators.embed import Embed


def assert_messages_sent(logger: Logger):
    """Assert that all messages sent to the logger's `DiscordHandler`s have been sent and didn't raise exceptions.

    Args:
        logger (Logger): The logger whose handlers should be checked.

    Raises:
        Exception: If any of the handlers raised an exception when sending a message.
    """
    for handler in logger.handlers:
        if isinstance(handler, DiscordHandler):
            handler.flush()


def logger(handlers: Iterable[DiscordHandler], name: str = ""):
    """Create a logger with the given handler.

    Args:
        handlers (Iterable[DiscordHandler]): The handlers to use for the logger.
        name (str, optional): The name of the logger. Defaults to the empty string.

    Returns:
            Logger: The created logger.
    """
    _logger = Logger(f"tests.{name}.{random.random()}")
    _logger.setLevel(logging.DEBUG)
    for handler in handlers:
        _logger.addHandler(handler)
    return _logger


class CustomEmbedMessageCreator(EmbedMessageCreator):
    """This custom message creator:
    - puts the title (logged message) in the description,
    - puts the description (file and line) in the title,
    - sets the author name to "Custom Embed" in every embed that a record is split into,
    - sets the footer to "This is a custom footer",
    - adds a field with name "Field Name 1" and value "Field Value 1" before the exception field,
    - adds an empty field which is supposed to be removed before the embed is sent,
    - adds a field with name "Field Name 2" and value "Field Value 2" after the exception field,
    """

    def get_description(self, record: LogRecord) -> str:
        return super().get_title(record)

    def get_title(self, record: LogRecord) -> str:
        return super().get_description(record)

    def get_new_embed(self, record: LogRecord) -> Embed:
        embed = super().get_new_embed(record)
        embed["author"]["name"] = "Custom Embed"
        return embed

    def get_author_name(self, record: LogRecord) -> str:
        return "Custom Embed"

    def get_footer_text(self, record: LogRecord) -> str:
        return "This is a custom footer"

    def get_field_definitions(
        self,
    ) -> List[Tuple[Callable[[LogRecord], str], Callable[[LogRecord], str]]]:
        return [
            (lambda _: "Field Name 1", lambda _: "Field Value 1"),
            (lambda _: "", lambda _: ""),
            *super().get_field_definitions(),
            (lambda _: "Field Name 2", lambda _: "Field Value 2"),
        ]


handler_factories: List[Callable[[MessageCreator], DiscordHandler]] = [
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
