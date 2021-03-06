class Handle:
    def __init__(self, value: str) -> None:
        if len(value) > 15:
            raise ValueError(f"Handle can have up to 15 characters: {value!r}")
        if len(value) < 2:
            raise ValueError(f"Handle must have at least 2 characters: {value!r}")
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Handle):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> "str":
        return self.value

    def __repr__(self) -> "str":
        return f"{self.__class__.__name__}(value={self.value})"

    def __hash__(self) -> int:
        return hash(str(self))
