import logging
import threading
from typing import Any, Dict, Iterable, Mapping
import requests
from discord_lumberjack.message_creators import BasicMessageCreator, MessageCreator

_default_message_creator = BasicMessageCreator()


class DiscordHandler(logging.Handler):
	"""A base class for logging handlers that send messages to Discord.

	Args:
		url (str): The URL to make the request to. This can be a webhook URL, a channel URL, a direct message URL, or any other URL that Discord supports.
		level (int, optional): The level at which to log. Defaults to logging.NOTSET.
		msg_creator (MessageCreator, optional): An instance of MessageCreator or one of its subclasses that will be used to create the message to send from each log record. Defaults to one that sends messages in monospace.
		http_headers (Mapping[str, Any], optional): A mapping of HTTP headers to send with the request. Defaults to an empty mapping.
		allowed_fields (Iterable[str], optional): A list of fields that the provided URL accepts. All other fields provided by the message creator will be removed. If None, all fields will be included. Defaults to None.
	"""

	def __init__(
		self,
		url: str,
		level: int = logging.NOTSET,
		message_creator: MessageCreator = None,
		http_headers: Mapping[str, Any] = None,
		allowed_fields: Iterable[str] = None,
	) -> None:
		super().__init__(level=level)
		self.__url = url
		self.__session = requests.Session()
		self.__message_creator = message_creator or _default_message_creator
		self.__session.headers.update(http_headers or {})
		self.__allowed_fields = allowed_fields

	def emit(self, record: logging.LogRecord) -> None:
		"""Log the messages to Discord.

		This method is non-blocking. The message will be send in the background.

		Args:
			record (logging.LogRecord): The log record to send.
		"""
		try:
			thread = threading.Thread(
				target=self.send_messages, name="DiscordLumberjack", args=(record,)
			)
			thread.start()
		except Exception:
			self.handleError(record)

	def transform_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
		"""Transform a message before sending it to Discord.

		This method is called for each message that is sent to Discord. It is called before any fields are filtered out.

		This method may be overridden by subclasses to transform each message as desired by each handler. By default, it keeps the message as is.

		Args:
			message (Dict[str, Any]): The message to transform.

		Returns:
			Dict[str, Any]: The transformed message.
		"""
		return message

	def filter_fields(self, message: Mapping[str, Any]) -> Dict[str, Any]:
		"""Remove any fields that are not in the allowed fields list, returning a new message with only allowed fields.

		Args:
			message (Mapping[str, Any]): The message as provided by the message creator.

		Returns:
			Dict[str, Any]: The message after removing any fields that are not in the allowed fields list.
		"""
		return {
			field: message[field]
			for field in message
			if self.__allowed_fields is None or field in self.__allowed_fields
		}

	def prepare_messages(self, record: logging.LogRecord) -> Iterable[Dict[str, Any]]:
		"""Given a log record, obtain all the message objects that will be sent to Discord.

		This method gets all the messages from the message creator, calls transform_message, which may be overridden by subclasses to transform each message as desired by each handler, and then filters out any fields that are not in the allowed fields list.

		Args:
			record (logging.LogRecord): The log record to send.

		Returns:
			Iterable[Dict[str, Any]]: The messages to send to Discord.
		"""
		return (
			self.filter_fields(self.transform_message(msg))
			for msg in self.__message_creator.messages(record, self.format)
		)

	def send_messages(self, record: logging.LogRecord):
		"""Send the messages returned by prepare_messages to Discord.

		Args:
			record (logging.LogRecord): The log record to send messages about

		Raises:
			RuntimeError: If the request to Discord was unsuccessful.
		"""
		for msg in self.prepare_messages(record):
			response = self.__session.post(self.__url, json=msg)
			if response.status_code >= 300:
				raise RuntimeError(
					f"Failed to send message to Discord: {response.text}"
				)
