import logging
from typing import Any, Dict
from discord_lumberjack.message_creators import MessageCreator
from .discord_handler import DiscordHandler


class DiscordWebhookHandler(DiscordHandler):
	"""A logging handler that sends messages to a Discord webhook.

	The username and avatar fields will override those provided by the message creator if provided here.

	Args:
		url (str): The URL to make the request to. This must be a webhook URL.
		level (int, optional): The level at which to log. Defaults to logging.NOTSET.
		message_creator (MessageCreator, optional): An instance of MessageCreator or one of its subclasses that will be used to create the message to send from each log record. Defaults to one that sends messages in monospace.
		username (str, optional): The username to use when sending messages. Defaults to None.
		avatar_url (str, optional): The avatar URL to use when sending messages. Defaults to None.
	"""

	def __init__(
		self,
		url: str,
		level: int = logging.NOTSET,
		message_creator: MessageCreator = None,
		username: str = None,
		avatar_url: str = None,
	) -> None:
		super().__init__(url, level=level, message_creator=message_creator)
		self.__username = username
		self.__avatar_url = avatar_url

	def transform_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
		"""Replace the username and avatar fields set by the message creator (if any) with those provided to the handler (if any).

		Args:
			message (Dict[str, Any]): The message provided by the message creator.

		Returns:
			Dict[str, Any]: The transformed message.
		"""
		message = message.copy()
		if self.__username:
			message["username"] = self.__username
		if self.__avatar_url:
			message["avatar_url"] = self.__avatar_url
		return message
