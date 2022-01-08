import logging
from logging import Logger
import os
from pytest import fixture
from discord_lumberjack.handler import DiscordWebhookHandler
import random
from dotenv import load_dotenv

load_dotenv()


class TestWebhookHandler:
	@fixture
	def url(self) -> str:
		result = os.getenv("WEBHOOK_URL")
		assert result is not None, "WEBHOOK_URL environment variable not set"
		return result

	@fixture
	def logger(self, url: str) -> Logger:
		result = logging.getLogger(f"{__name__}.{random.random()}")
		result.setLevel(logging.DEBUG)
		handler = DiscordWebhookHandler(url, username=f"Test Webhook Handler")
		handler.setFormatter(
			logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
		)
		result.addHandler(handler)
		return result

	def test_webhook_handler(self, logger: Logger):
		"""Log a message to a Discord Webhook"""
		logger.info(f"test_webhook_handler passed successfully.")