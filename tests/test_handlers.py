from pytest import raises
from logging import Logger
from tests.utils import assert_messages_sent


def test_handler(logger: Logger):
	"""Log a message with each handler."""
	logger.info(f"test_webhook_handler passed successfully.")
	assert_messages_sent(logger)


def test_untextable_user(logger_with_untextable_user: Logger):
	"""Log a message with each handler."""
	with raises(Exception):
		logger_with_untextable_user.info(f"test_webhook_handler passed successfully.")
		assert_messages_sent(logger_with_untextable_user)