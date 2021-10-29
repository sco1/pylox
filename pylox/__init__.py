import typing as t


class InterpreterProtocol(t.Protocol):  # pragma: no cover  # noqa: D101
    def report_error(self) -> None:  # noqa: D102
        ...
