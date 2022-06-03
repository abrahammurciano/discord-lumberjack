from .embed_message_creator import EmbedMessageCreator
from logging import LogRecord


class EmbedLongMessageCreator(EmbedMessageCreator):
    """Similar to the `EmbedMessageCreator`, but it switches the title and the description.

    This is useful for when your log messages might be longer than Discord's limit for embed titles. This class therefore puts the message in the description and the path to the file and line number in the title.
    """

    def get_description(self, record: LogRecord) -> str:
        return f"**{super().get_title(record)}**"

    def get_title(self, record: LogRecord) -> str:
        return super().get_description(record)
