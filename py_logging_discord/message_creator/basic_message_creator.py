from logging import LogRecord
from typing import Callable, Iterable, Sequence, TypeVar
from .message_creator import MessageCreator

T = TypeVar("T")


class BasicMessageCreator(MessageCreator):
	"""
	This class creates messages displayed in plain text.

	Args:
		monospace (bool, optional): Whether or not to format the messages as monospace. Defaults to True.
	"""

	def __init__(self, monospace: bool = True) -> None:
		super().__init__()
		if monospace:
			self.__prefix = "```"
			self.__suffix = "```"
			self.__content_limit = 1994
		else:
			self.__prefix = ""
			self.__suffix = ""
			self.__content_limit = 2000

	def messages(
		self, record: LogRecord, format_func: Callable[[LogRecord], str]
	) -> Iterable[dict]:
		return (
			{"content": self.__prefix + "".join(chunk) + self.__suffix}
			for chunk in self.__chunks(format_func(record), self.__content_limit)
		)

	def __chunks(self, seq: Sequence[T], chunk_size: int) -> Iterable[Sequence[T]]:
		return (seq[pos : pos + chunk_size] for pos in range(0, len(seq), chunk_size))
