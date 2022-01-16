from abc import ABC, abstractmethod
from logging import LogRecord, Formatter
from typing import Any, Callable, Iterable, Dict


class MessageCreator(ABC):
	"""
	A class which is able to create messages from a log record.

	Subclasses must implement the `create_message` method.
	"""

	@abstractmethod
	def messages(
		self, record: LogRecord, format_func: Callable[[LogRecord], str]
	) -> Iterable[Dict[str, Any]]:
		"""
		Format a log record to a discord message object (dict).

		This method should be overridden by subclasses for the subclass to be able to specify the format of the message it creates.

		Subclasses may choose to use the `format_func` argument to format the log record to a string, or may ignore it completely and format the messages directly using the log record, or a combination of the two.

		Subclasses should make sure the messages it creates are not too long to be rejected by discord. If they are, they should split the message into multiple messages.

		Args:
			record (LogRecord): The log record to format into a message.
			format_func (Callable[[LogRecord], str]): A function which formats a log record into a string. This function is expected to originate from a `Formatter` instance.

		Returns:
			Iterable[dict]: An iterable of discord message objects (dicts). The reason it returns many messages is in case there is too much information in the log record to fit into a single message.
		"""
		pass
