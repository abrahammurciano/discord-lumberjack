import logging
from py_logging_discord.message_creator import MessageCreator
from .discord_channel_handler import DiscordChannelHandler


class DiscordDMHandler(DiscordChannelHandler):
	def __init__(
		self,
		bot_token: str,
		user_id: int,
		level: int = logging.NOTSET,
		msg_creator: MessageCreator = None,
	) -> None:
		super().__init__(
			bot_token,
			self.create_dm_channel(user_id),
			level=level,
			msg_creator=msg_creator,
		)

	def create_dm_channel(self, user_id: int) -> int:
		"""Create a DM channel through the discord API.

		Args:
			user_id (int): The ID of the user to create a DM channel with.

		Returns:
			int: The ID of the DM channel.

		Raises:
			ValueError: If the bot has no permissions to create a DM channel with the user.
		"""
		# TODO: Implement this.
		raise NotImplementedError()