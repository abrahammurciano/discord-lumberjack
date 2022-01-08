import logging
from logging import Logger
import os
from pytest import fixture
import random
from dotenv import load_dotenv
from discord_lumberjack.handler import DiscordChannelHandler

load_dotenv()


class TestChannelHandler:
	@fixture
	def token(self) -> str:
		result = os.getenv("BOT_TOKEN")
		assert result is not None, "BOT_TOKEN environment variable not set"
		return result

	@fixture
	def logger(self, token: str) -> Logger:
		result = logging.getLogger(f"{__name__}.{random.random()}")
		result.setLevel(logging.DEBUG)
		handler = DiscordChannelHandler(token, 928988880911360020)
		handler.setFormatter(
			logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
		)
		result.addHandler(handler)
		return result

	def test_channel_handler(self, logger: Logger):
		"""Log a message to a Discord Channel by a Bot."""
		logger.info(f"test_channel_handler passed successfully.")