from typing import Iterable, Sequence, TypeVar

T = TypeVar("T")


def chunks(seq: Sequence[T], chunk_size: int) -> Iterable[Sequence[T]]:
	return (seq[pos : pos + chunk_size] for pos in range(0, len(seq), chunk_size))
