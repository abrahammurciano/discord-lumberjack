import logging
from typing import Mapping

default_colours = {
	logging.NOTSET: 0x888888,
	logging.DEBUG: 0x7289DA,
	logging.INFO: 0x43B581,
	logging.WARNING: 0xFAA61A,
	logging.ERROR: 0xF47B68,
	logging.CRITICAL: 0xF04747,
}


class LogColours:
	"""This class defines a set of colours used for different log levels.

	It takes a mapping of log levels to colours. The colours are represented as integers, and are expected to be in the range of 0x000000 to 0xFFFFFF.

	You can then access a colour value for any log level by using the brackets operator. If the log level is not in the mapping, the colour for the highest log level that is lower than the log level will be used.

	Args:
		colours (Mapping[int, int], optional): A mapping of log levels to colours. Log levels which are not given will be taken from the closest provided log level less than it. Defaults to a sensible selection of colours.
	"""

	def __init__(self, colours: Mapping[int, int] = None) -> None:
		self.__colours = colours or default_colours

	def __getitem__(self, level: int) -> int:
		try:
			return self.__colours[
				max(min_lvl for min_lvl in self.__colours if min_lvl <= level)
			]
		except KeyError:
			return 0xFFFFFF
