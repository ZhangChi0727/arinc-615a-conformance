"""Named D-stage engineering failures.  None of these codes is an IUT FAIL."""


class EngineeringError(ValueError):
    """Closed engineering-delivery error with a stable diagnostic code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code

    def __str__(self) -> str:
        return f"{self.code}: {super().__str__()}"
