import logging

from py_logging_discord.message_creator import MessageCreator
from .discord_handler import DiscordHandler


class DiscordChannelHandler(DiscordHandler):
	def __init__(
		self,
		bot_token: str,
		channel_id: int,
		level: int = logging.NOTSET,
		msg_creator: MessageCreator = None,
	) -> None:
		super().__init__(
			f"https://discord.com/api/channels/{channel_id}/messages",
			level=level,
			msg_creator=msg_creator,
			http_headers={"Authorization": f"Bot {bot_token}"},
			allowed_fields=(
				"content",
				"tts",
				"embeds",
				"embed",
				"allowed_mentions",
				"message_reference",
				"components",
				"sticker_ids",
				"files",
				"payload_json",
				"attachments",
			),
		)
