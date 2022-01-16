from typing import Any, Callable, Generator, List, Optional, Sequence, TypedDict, Union
from logging import LogRecord


class EmbedAuthor(TypedDict):
	name: str
	url: Optional[str]
	icon_url: Optional[str]
	proxy_icon_url: Optional[str]


class EmbedField(TypedDict):
	name: str
	value: str
	inline: bool


class EmbedFooter(TypedDict):
	text: Optional[str]
	icon_url: Optional[str]


class EmbedImage(TypedDict):
	url: Optional[str]
	proxy_url: Optional[str]
	height: Optional[int]
	width: Optional[int]


class Embed(TypedDict):
	author: EmbedAuthor
	title: Optional[str]
	description: Optional[str]
	fields: List[EmbedField]
	url: Optional[str]
	timestamp: Optional[str]
	color: Optional[int]
	footer: EmbedFooter
	image: EmbedImage
	thumbnail: EmbedImage


def empty_embed(n_fields: int = 0) -> Embed:
	"""Create an empty embed with the specified number of empty fields.

	Args:
		n_fields (int, optional): The number of empty fields to initialise the embed with. Defaults to 0.

	Returns:
		Embed: An empty embed.
	"""
	return Embed(
		author=EmbedAuthor(name="", url=None, icon_url=None, proxy_icon_url=None),
		title=None,
		description=None,
		fields=[EmbedField(name="", value="", inline=False) for _ in range(n_fields)],
		url=None,
		timestamp=None,
		color=None,
		footer=EmbedFooter(text=None, icon_url=None),
		image=EmbedImage(url=None, proxy_url=None, height=None, width=None),
		thumbnail=EmbedImage(url=None, proxy_url=None, height=None, width=None),
	)


def embed_length(embed: Embed) -> int:
	"""Calculates the total length of the size-limited fields of an embed.

	Args:
		embed (Embed): The embed to calculate the length of.

	Returns:
		int: The total length of the size-limited fields of the embed.
	"""
	return sum(
		len(string)
		for string in (
			embed["title"],
			embed["description"],
			embed["footer"]["text"],
			embed["author"]["name"],
			*(field["name"] for field in embed["fields"]),
			*(field["value"] for field in embed["fields"]),
		)
		if string
	)


class EmbedFieldSetter:
	"""Sets a field of an embed as specified by the user, providing a mechanism for not overflowing the embeds.

	Args:
		key_chain (Sequence[str | int]): A sequence of the keys (at least one) to index the embed with. For example if the value `v` should be set like this, `embed["fields"][2]["name"] = v`, then the `key_chain` would be `("fields", 2, "name")`.
		get_value (Callable[[LogRecord], Any]): A function that gets a value to pass to `set_value` from a log record.
		limit (int): The limit of the field this `EmbedFieldSetter` is setting.
	"""

	def __init__(
		self,
		key_chain: Sequence[Union[str, int]],
		get_value: Callable[[LogRecord], Any],
		limit: Optional[int] = None,
	):
		self.__limit = limit
		if not key_chain:
			raise ValueError("There must be at least one key in key_chain.")
		self.__key_chain = key_chain[:-1]
		self.__last_key = key_chain[-1]
		self.__get_value = get_value

	def set_field(
		self,
		embed: Embed,
		record: LogRecord,
		remainder: str = None,
		new_embed_creator: Callable[[LogRecord], Embed] = None,
		remaining_global_limit: Optional[int] = None,
	) -> Generator[Embed, Any, None]:
		"""[summary]

		Args:
			embed (Embed): The embed to set the field in.
			record (LogRecord): The log record containing the data to set.
			remainder (str, optional): The text that should have been in the same field of the previous embed but couldn't be set due to length limitations. Defaults to None.
			new_embed_creator (Callable[[LogRecord], Embed], optional): A function that generates a new embed and sets whatever fields will persist across all the embeds that a log record is split up into. Defaults to a function that returns an empty embed.
			remaining_global_limit (Optional[int], optional): The number of remaining characters that can be added to limited fields of the embed before it is split up. Defaults to None.

		Yields:
			Embed: This function yields any embeds which it creates.

		Raises:
			KeyError: If the key chain is invalid.
		"""
		full_value = remainder or self.__get_value(record)
		if full_value is None:
			return
		msg_component: Any = embed
		for key in self.__key_chain:
			msg_component = msg_component[key]
		limit = (
			min(self.__limit, remaining_global_limit)
			if self.__limit and remaining_global_limit
			else self.__limit or remaining_global_limit
		)
		if isinstance(full_value, str):
			value = full_value[:limit]
			remainder = full_value[limit:] if limit is not None else None
		else:
			value = full_value
			remainder = None
		msg_component[self.__last_key] = value
		if remainder:
			new_embed_creator = new_embed_creator or (lambda _: empty_embed())
			new_embed = new_embed_creator(record)
			yield new_embed
			yield from self.set_field(
				new_embed,
				record,
				remainder,
				new_embed_creator,
				remaining_global_limit - len(value) if remaining_global_limit else None,
			)
