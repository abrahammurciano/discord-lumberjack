from logging import LogRecord
from typing import Callable, Generator, Iterable, List, Mapping, Tuple
from .message_creator import MessageCreator
from .log_colours import LogColours
from .embed import Embed, EmbedFieldSetter, embed_length, empty_embed
import datetime as dt
from itertools import chain
import traceback


class EmbedMessageCreator(MessageCreator):
	"""This message creator creates messages with the `LogRecord`'s data nicely formatted in an embed.

	To customise the way the embed looks, you should subclass this class and override any or all of the methods starting with `get_`. All of these (except two) take a `LogRecord`, and most of them simply return the string to put in one of the embed's fields.

	The first exceptions is `get_field_definitions`, which returns a list of tuples of two functions, these are used to get the name or value of the field, respectively. They both take a `LogRecord` and return a string.

	The second exception is `get_new_embed`, which returns an embed prefilled with the fields that should be set on every embed that a `LogRecord` is split into.

	Args:
		colours (Mapping[int, int]): A mapping of log levels to colours. If a log level doesn't have an index in this mapping, the colour of the closest level lower than it will be used. If not provided, sensible selection of colours will be used.
	"""

	def __init__(self, colours: Mapping[int, int] = None,) -> None:
		super().__init__()
		self.__colours = LogColours(colours)
		self.__field_setters = self.__create_field_setters()

	def messages(
		self, record: LogRecord, format_func: Callable[[LogRecord], str]
	) -> Iterable[dict]:
		"""This method is responsible for creating a batch of messages for each `LogRecord`. It creates messages with a fancy looking embed. If there is too much data in the `LogRecord` for one embed, it will create more as needed.

		This method ignores the `format_func` argument.

		Args:
			record (LogRecord): The record to create messages for.
			format_func (Callable[[LogRecord], str]): This argument is ignored.

		Returns:
			Iterable[dict]: The messages to pass on to the handler.
		"""
		first_embed = self.get_new_embed(record)
		embeds = [first_embed]
		for field_setter in self.__field_setters:
			for new_embed in field_setter.set_field(
				embeds[-1], record, None, self.get_new_embed, 6000
			):
				embeds.append(new_embed)
		for embed in embeds:
			self.__fix_fields(embed)
		return (
			{"embeds": embeds_chunk} for embeds_chunk in self.__embed_chunks(embeds)
		)

	def __embed_chunks(
		self, embeds: Iterable[Embed]
	) -> Generator[List[Embed], None, None]:
		"""This method splits the given embeds into chunks of up to 10, keeping within the limit of 6000 total characters (on certain fields).

		This method assumes that each embed has a length of at most 6000 characters.

		Args:
			embeds (Iterable[Embed]): The embeds to split.

		Yields:
			List[Embed]: The embeds in chunks of 10.
		"""
		limit = 6000
		chunk: List[Embed] = []
		for embed in embeds:
			length = embed_length(embed)
			if length < limit and len(chunk) < 10:
				chunk.append(embed)
				limit -= length
			else:
				yield chunk
				chunk = [embed]
				limit = 6000 - length
		yield chunk

	def get_colour(self, record: LogRecord) -> int:
		"""Returns the colour to set the embed to.

		This is obtained from the `colours` mapping passed to the constructor and from the log level. If you want to customise the colours you should probably do it by passing the colours you want to the constructor rather than by overriding this method. However if you want some more advanced custom behaviour, such as setting the colour based on the file that created the log record, feel free to override this method to do that.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			int: The colour to set the embed to.
		"""
		return self.__colours[record.levelno]

	def get_thumbnail_url(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's thumbnail URL to. By default this is left empty.

		You can override this method to return a custom thumbnail URL.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The string to set the thumbnail URL to.
		"""
		return ""

	def get_author_url(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's author's URL to. By default there is no URL.

		You can override this method to return a custom URL.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The URL to set for the author.
		"""
		return ""

	def get_author_icon_url(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's author's icon URL to. By default this is an appropriate image corresponding to the log level.

		You can override this method to return a custom icon URL.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The URL to set the author's icon to.
		"""
		return f"https://raw.githubusercontent.com/abrahammurciano/discord-lumberjack/main/images/{record.levelname.lower()}.png"

	def get_author_name(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's author's name to. By default this is the name of the log level. FOr example "ERROR", "INFO", etc.

		You can override this method to return a custom name.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The string to set the author's name to.
		"""
		return record.levelname

	def get_title(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's title to. By default this is the message that was logged, for examply by calling a log method like `log.info("This is the message that was logged")`.

		You can override this method to return a custom title.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The string to set the title to.
		"""
		return record.getMessage()

	def get_description(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's description to. By default this is the path to the file and the line that the log was created at.

		You can override this method to return a custom description.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The string to set the description to.
		"""
		return f"In {record.pathname} at line {record.lineno}"

	def get_url(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's URL to. By default there is no URL.

		You can override this method to return a custom URL.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The URL to set the embed's URL to.
		"""
		return ""

	def get_footer_icon_url(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's footer icon to. By default the footer icon is left empty.

		You can override this method to return a custom footer icon URL.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The string to set the footer icon to.
		"""
		return ""

	def get_footer_text(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's footer to. By default the footer is left empty.

		You can override this method to return a custom footer.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The string to set the footer to.
		"""
		return ""

	def get_timestamp(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's timestamp to. By default this is the time the log was created.

		You probably won't need to override this method.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The string to set the timestamp to.
		"""
		tzinfo = dt.datetime.now().astimezone().tzinfo
		return dt.datetime.fromtimestamp(record.created, tz=tzinfo).isoformat()

	def get_image_url(self, record: LogRecord) -> str:
		"""Returns the string to set the embed's image URL to. By default this is left empty.

		You can override this method to return a custom image URL.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			str: The string to set the image URL to.
		"""
		return ""

	def get_field_definitions(
		self,
	) -> List[Tuple[Callable[[LogRecord], str], Callable[[LogRecord], str]]]:
		"""This method defines which fields will be included in the embed.

		By default, it defines one field which contains exception information, if there was an exception. You can override this method to change what fields are included.

		This function should return a list of tuples, one for each field definition. Each tuple should consist of two functions both of which take the `LogRecord` as input and return a string. The first returns the string to set the field name to, and the second returns the string to set the field value to.

		Note, if a field name or value is left empty, it will be set to a dash "-" instead. If both the field name *and* value are left empty, the field will be removed. Therefore if you want to conditionally include a field, both functions in that field's tuple should conditionally return an empty string.

		Returns:
			List[Tuple[Callable[[LogRecord], str], Callable[[LogRecord], str]]]: A list of tuples, each containing two functions similar to the other getters in this class. One for the field name and one for the field value.
		"""

		def exception_title(record: LogRecord) -> str:
			return (
				f"{record.exc_info[0].__name__}: {record.exc_info[1]}"
				if record.exc_info and record.exc_info[0]
				else ""
			)

		def exception_info(record: LogRecord) -> str:
			nl = "\n"
			return (
				f"```{nl.join(traceback.format_tb(record.exc_info[2]))}```"
				if record.exc_info and record.exc_info[2]
				else ""
			)

		return [(exception_title, exception_info)]

	def get_new_embed(self, record: LogRecord) -> Embed:
		"""This method is called to create each embed that a `LogRecord` splits up into. So if there are any properties you want to be set for every embed that gets produced from a single `LogRecord`, here is the place to set them.

		For example -- and this is the default behaviour -- you might want all embeds of a particular `LogRecord` to have the colour set (according to the log level most likely). Then in the new embed created by this function, you should set the colour before returning it.

		Args:
			record (LogRecord): The `LogRecord` containing the data to use.

		Returns:
			Embed: A new embed with possibly some properties preset.
		"""
		embed = empty_embed(len(self.get_field_definitions()))
		embed["color"] = self.get_colour(record)
		return embed

	def __create_field_setters(self) -> Iterable[EmbedFieldSetter]:

		fields_field_setters = chain.from_iterable(
			(
				EmbedFieldSetter(("fields", i, "name"), get_name, 256),
				EmbedFieldSetter(("fields", i, "value"), get_value, 1024),
			)
			for i, (get_name, get_value) in enumerate(self.get_field_definitions())
		)

		return [
			EmbedFieldSetter(("color",), self.get_colour),
			EmbedFieldSetter(("thumbnail", "url"), self.get_thumbnail_url),
			EmbedFieldSetter(("author", "url"), self.get_author_url),
			EmbedFieldSetter(("author", "icon_url"), self.get_author_icon_url),
			EmbedFieldSetter(("author", "name"), self.get_author_name, 256),
			EmbedFieldSetter(("title",), self.get_title, 256),
			EmbedFieldSetter(("description",), self.get_description, 4096),
			EmbedFieldSetter(("url",), self.get_url),
			*fields_field_setters,
			EmbedFieldSetter(("footer", "icon_url"), self.get_footer_icon_url),
			EmbedFieldSetter(("footer", "text"), self.get_footer_text, 2048),
			EmbedFieldSetter(("timestamp",), self.get_timestamp),
			EmbedFieldSetter(("image", "url"), self.get_image_url),
		]

	def __fix_fields(self, embed: Embed) -> None:
		"""This method is called to fix any fields that are invalid.

		It removes fields with no name and no value. If sets empty name or values to "-" if it has either a name or value.

		Args:
			embed (Embed): The embed whose fields to fix.
		"""
		embed["fields"] = [
			field for field in embed["fields"] if field["name"] or field["value"]
		]
		for field in embed["fields"]:
			if not field["name"]:
				field["name"] = "-"
			if not field["value"]:
				field["value"] = "-"
