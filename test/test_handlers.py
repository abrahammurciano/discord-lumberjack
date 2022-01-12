from typing import Callable
from pytest import raises
from logging import Logger


def test_handler(logger: Logger, wait_for_messages: Callable[[], None]):
	"""Log a message with each handler."""
	logger.info(f"test_webhook_handler passed successfully.")
	wait_for_messages()


def test_untextable_user(
	logger_with_untextable_user: Logger, wait_for_messages: Callable[[], None]
):
	"""Log a message with each handler."""
	with raises(RuntimeError):
		logger_with_untextable_user.info(f"test_webhook_handler passed successfully.")
		wait_for_messages()