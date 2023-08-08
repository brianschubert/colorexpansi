"""
ANSI escape codes.

References
----------

1. https://en.wikipedia.org/wiki/ANSI_escape_code
2. https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

"""
import abc
from typing import Final

CONTROL_SEQUENCE_INTRODUCER: Final[str] = "\N{ESC}"

SGR_DELIMITER: Final[str] = ";"

SGR_TERMINATOR: Final[str] = "m"


class SGRControlSequence(abc.ABC):
    """Base class for ANSI Set Graphic Rendition escape sequences."""

    @abc.abstractmethod
    def arguments(self) -> list[str]:
        """Return the argument list for this SGR escape sequence."""

    def as_str(self) -> str:
        body = SGR_DELIMITER.join(self.arguments())
        return f"{CONTROL_SEQUENCE_INTRODUCER}{body}{SGR_TERMINATOR}"

    def __str__(self) -> str:
        return self.as_str()

    def __bytes__(self) -> bytes:
        return self.as_str().encode("ascii")
