import logging

from discord_lumberjack.message_creators import MessageCreator
from .discord_handler import DiscordHandler


class DiscordChannelHandler(DiscordHandler):
	"""A logging handler that sends messages to a Discord Channel from a Bot.

	Args:
		bot_token (str): The authentication token of the Bot to send the message with.
		channel_id (int): The ID of the Channel to send the message to.
		level (int, optional): The level at which to log. Defaults to logging.NOTSET.
		message_creator (MessageCreator, optional): An instance of MessageCreator or one of its subclasses that will be used to create the message to send from each log record. Defaults to one that sends messages in monospace.
	"""

	def __init__(
		self,
		bot_token: str,
		channel_id: int,
		level: int = logging.NOTSET,
		message_creator: MessageCreator = None,
	) -> None:
		super().__init__(
			f"https://discord.com/api/channels/{channel_id}/messages",
			level=level,
			message_creator=message_creator,
			http_headers={"Authorization": f"Bot {bot_token}"},
		)
