"""
ANSI escape codes.

References
----------

1. https://en.wikipedia.org/wiki/ANSI_escape_code
2. https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

"""
import abc
import enum
import itertools
from dataclasses import dataclass
from typing import ClassVar, Final, Literal

from typing_extensions import TypeAlias

Region: TypeAlias = Literal["foreground", "background"]

CONTROL_SEQUENCE_INTRODUCER: Final[str] = "\N{ESC}"

SGR_DELIMITER: Final[str] = ";"

SGR_TERMINATOR: Final[str] = "m"


@enum.unique
class GraphicsMode(enum.IntEnum):
    RESET = 0
    SET_BOLD = 1
    SET_DIM = 2
    SET_ITALIC = 3
    SET_UNDERLINE = 4
    SET_BLINK = 5
    SET_REVERSE = 7
    SET_HIDDEN = 8
    SET_STRIKE = 9
    RESET_BOLD_DIM = 22
    RESET_ITALIC = 23
    RESET_UNDERLINE = 24
    RESET_BLINK = 25
    RESET_REVERSE = 27
    RESET_HIDDEN = 28
    RESET_STRIKE = 29


@enum.unique
class StandardColor(enum.IntEnum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    DEFAULT = 9


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


@dataclass
class ConcatenatedSequence(SGRControlSequence):
    parts: list[SGRControlSequence]

    def arguments(self) -> list[str]:
        return list(
            itertools.chain.from_iterable(seq.arguments() for seq in self.parts)
        )


@dataclass
class GraphicsModeControlSequence(SGRControlSequence):
    mode: GraphicsMode

    def arguments(self) -> list[str]:
        return [str(self.mode.value)]


@dataclass
class Color16ControlSequence(SGRControlSequence):
    color: StandardColor
    bright: bool = False
    which: Region = "foreground"

    OFFSET_MAP: ClassVar[dict[tuple[bool, Region], int]] = {
        (False, "foreground"): 30,
        (False, "background"): 40,
        (True, "foreground"): 90,
        (True, "background"): 100,
    }

    def _argument_offset(self) -> int:
        which = self.which
        if self.color == StandardColor.DEFAULT:
            which = "foreground"

        return self.OFFSET_MAP[(self.bright, which)]

    def arguments(self) -> list[str]:
        return [str(self._argument_offset() + self.color.value)]
