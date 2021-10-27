import attr


@attr.s(slots=True)
class LoxException:
    line: int
    col: int
    message: str

    def __str__(self) -> str:
        return f"{self.__name__}: {self.message}"  # type: ignore[attr-defined]
