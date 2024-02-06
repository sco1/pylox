import typing as t


class BoolEq(t.Protocol):
    def __eq__(self, other: object) -> bool: ...
