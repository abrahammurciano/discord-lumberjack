from typing import List, Optional, TypedDict


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
	"""
	An embed footer object.
	"""

	text: Optional[str]
	icon_url: Optional[str]


class EmbedImage(TypedDict):
	"""
	An embed image object.
	"""

	url: Optional[str]
	proxy_url: Optional[str]
	height: Optional[int]
	width: Optional[int]


class EmbedThumbnail(TypedDict):
	"""
	An embed thumbnail object.
	"""

	url: Optional[str]
	proxy_url: Optional[str]
	height: Optional[int]
	width: Optional[int]


class Embed(TypedDict):
	"""
	An embed object.
	"""

	author: EmbedAuthor
	title: Optional[str]
	description: Optional[str]
	fields: List[EmbedField]
	url: Optional[str]
	timestamp: Optional[str]
	color: Optional[int]
	footer: EmbedFooter
	image: EmbedImage
	thumbnail: EmbedThumbnail
