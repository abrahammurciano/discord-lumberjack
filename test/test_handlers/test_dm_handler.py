import logging
from logging import Logger
import os
import random
from dotenv import load_dotenv
from discord_lumberjack.handler import DiscordDMHandler
from pytest import fixture

load_dotenv()


class TestDMHandler:
	@fixture
	def token(self) -> str:
		result = os.getenv("BOT_TOKEN")
		assert result is not None, "BOT_TOKEN environment variable not set"
		return result

	@fixture(params=[688455111181205561, 758390455661494303])
	def logger(self, token: str, request) -> Logger:
		result = logging.getLogger(f"{__name__}.{random.random()}")
		result.setLevel(logging.DEBUG)
		handler = DiscordDMHandler(token, request.param)
		handler.setFormatter(
			logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
		)
		result.addHandler(handler)
		return result

	def test_dm_handler(self, logger: Logger):
		"""Log a message to a DM from a Bot."""
		logger.info(f"test_dm_handler passed successfully.")
