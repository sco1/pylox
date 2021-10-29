import typing as t


class InterpreterProtocol(t.Protocol):  # noqa: D101
    def report_error(self) -> None:  # noqa: D102
        ...
