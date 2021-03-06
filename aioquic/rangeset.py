from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Iterable, List, Optional


class RangeSet(Sequence):
    def __init__(self, ranges: Iterable[range] = []):
        self.__ranges: List[range] = []
        for r in ranges:
            assert r.step == 1
            self.add(r.start, r.stop)

    def add(self, start: int, stop: Optional[int] = None) -> None:
        if stop is None:
            stop = start + 1
        assert stop > start

        for i, r in enumerate(self.__ranges):
            # the added range is entirely before current item, insert here
            if stop < r.start:
                self.__ranges.insert(i, range(start, stop))
                return

            # the added range is entirely after current item, keep looking
            if start > r.stop:
                continue

            # the added range touches the current item, merge it
            start = min(start, r.start)
            stop = max(stop, r.stop)
            while i < len(self.__ranges) - 1 and self.__ranges[i + 1].start <= stop:
                stop = max(self.__ranges[i + 1].stop, stop)
                self.__ranges.pop(i + 1)
            self.__ranges[i] = range(start, stop)
            return

        # the added range is entirely after all existing items, append it
        self.__ranges.append(range(start, stop))

    def shift(self) -> range:
        return self.__ranges.pop(0)

    def __bool__(self) -> bool:
        return bool(self.__ranges)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RangeSet):
            return NotImplemented

        return self.__ranges == other.__ranges

    def __getitem__(self, key: Any) -> range:
        return self.__ranges[key]

    def __len__(self) -> int:
        return len(self.__ranges)

    def __repr__(self) -> str:
        return "RangeSet({})".format(repr(self.__ranges))
