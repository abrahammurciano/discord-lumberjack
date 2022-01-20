import time
import pytest
from logging import Logger
from tests.utils import assert_messages_sent


def test_handler(logger: Logger):
	"""Log a message with each handler."""
	logger.info(f"test_handler passed successfully.")
	assert_messages_sent(logger)


def test_untextable_user(logger_with_untextable_user: Logger):
	"""Log a message with each handler."""
	with pytest.raises(Exception):
		logger_with_untextable_user.info(f"test_untextable_user failed.")
		assert_messages_sent(logger_with_untextable_user)


def test_log_speed(logger_with_all_handlers: Logger):
	"""Make sure calls to the logger return quickly."""
	start = time.time()
	logger_with_all_handlers.info(f"testing log speed...")
	end = time.time()
	diff = end - start
	limit = 0.01
	assert (
		diff < limit
	), f"Logging took too long. Limit is {limit} seconds. Took {diff} seconds."


@pytest.mark.timeout(30)
def test_recursion(root_logger: Logger):
	"""Make sure there's no infinite recursion when a DiscordHandler is added to the root logger."""
	root_logger.info(f"Pop goes the stack...")
	assert_messages_sent(root_logger)
