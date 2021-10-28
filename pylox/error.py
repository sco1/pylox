import attr


@attr.s(slots=True)
class LoxException:
    """Base Lox exception type."""

    line: int = attr.ib()
    col: int = attr.ib()
    message: str = attr.ib()

    def __str__(self) -> str:
        return f"{self.__name__}: {self.message}"  # type: ignore[attr-defined]
