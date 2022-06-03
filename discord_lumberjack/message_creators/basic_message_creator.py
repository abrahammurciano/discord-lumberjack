from logging import LogRecord
from typing import Callable, Iterable
from .message_creator import MessageCreator
from .chunks import chunks


class BasicMessageCreator(MessageCreator):
    """
    This class creates messages displayed in plain text.

    Args:
        monospace (bool, optional): Whether or not to format the messages as monospace. Defaults to True.
        lang (str, optional): The language to be used by Discord syntax highlighting. Defaults to "ansi". This is only considered if monospace is True.
    """

    def __init__(self, monospace: bool = True, lang: str = "ansi") -> None:
        super().__init__()
        if monospace:
            self.__prefix = f"```{lang}\n"
            self.__suffix = "```"
        else:
            self.__prefix = ""
            self.__suffix = ""
        self.__content_limit = 2000 - len(self.__prefix) - len(self.__suffix)

    def messages(
        self, record: LogRecord, format_func: Callable[[LogRecord], str]
    ) -> Iterable[dict]:
        return (
            {"content": self.__prefix + "".join(chunk) + self.__suffix}
            for chunk in chunks(format_func(record), self.__content_limit)
        )
