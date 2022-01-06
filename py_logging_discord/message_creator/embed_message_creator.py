from logging import LogRecord
from typing import Callable, Iterable, Mapping
from message_creator import MessageCreator
from .log_colours import LogColours
from .embed import Embed


class EmbedMessageCreator(MessageCreator):
	def __init__(self, colours: Mapping[int, int]) -> None:
		super().__init__()
		self.__colours = LogColours(colours)

	def messages(
		self, record: LogRecord, format_func: Callable[[LogRecord], str]
	) -> Iterable[dict]:
		raise NotImplementedError()
