import logging
import requests
from discord_lumberjack.message_creators import MessageCreator
from .discord_channel_handler import DiscordChannelHandler


class DiscordDMHandler(DiscordChannelHandler):
	"""A logging handler that sends messages to a Discord  Direct Message Channel from a Bot.

	Upon construction, this handler will attempt to create a DM channel with the user specified by the user_id argument. If this fails, the constructor will raise a ValueError.

	Since a DM channel is a kind of channel, this handler is a subclass of DiscordChannelHandler.

	Args:
		bot_token (str): The authentication token of the Bot to send the message with.
		user_id (int): The ID of the user to send the message to.
		level (int, optional): The level at which to log. Defaults to logging.NOTSET.
		message_creator (MessageCreator, optional): An instance of MessageCreator or one of its subclasses that will be used to create the message to send from each log record. Defaults to one that sends messages in monospace.
	"""

	def __init__(
		self,
		bot_token: str,
		user_id: int,
		level: int = logging.NOTSET,
		message_creator: MessageCreator = None,
	) -> None:
		super().__init__(
			bot_token,
			self.create_dm_channel(user_id, bot_token),
			level=level,
			message_creator=message_creator,
		)

	def create_dm_channel(self, user_id: int, bot_token: str) -> int:
		"""Create a DM channel through the discord API.

		Args:
			user_id (int): The ID of the user to create a DM channel with.

		Returns:
			int: The ID of the DM channel.

		Raises:
			ValueError: If the bot was unable to create a DM channel with the user.
		"""
		r = requests.post(
			"https://discord.com/api/users/@me/channels",
			json={"recipient_id": user_id},
			headers={"Authorization": f"Bot {bot_token}"},
		)
		if r.status_code >= 300:
			raise ValueError(
				f"Could not create DM channel with user {user_id}. Response: {r.text}"
			)
		return r.json()["id"]
