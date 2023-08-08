"""
ANSI escape codes.

References
----------

1. https://en.wikipedia.org/wiki/ANSI_escape_code
2. https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

"""
from __future__ import annotations

import abc
import enum
import itertools
from collections.abc import Iterable
from dataclasses import dataclass
from typing import ClassVar, Final, Literal

from typing_extensions import TypeAlias

Region: TypeAlias = Literal["foreground", "background"]

Int8: TypeAlias = int

CONTROL_SEQUENCE_INTRODUCER: Final[str] = "\N{ESC}["

SGR_DELIMITER: Final[str] = ";"

SGR_TERMINATOR: Final[str] = "m"


@enum.unique
class GraphicsMode(enum.IntEnum):
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7
    HIDDEN = 8
    STRIKE = 9


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


class SGRControlSequence(abc.ABC):
    """Base class for ANSI Set Graphic Rendition escape sequences."""

    @abc.abstractmethod
    def arguments(self) -> Iterable[str]:
        """Return the arguments for this SGR escape sequence."""

    def as_str(self) -> str:
        body = SGR_DELIMITER.join(self.arguments())
        return f"{CONTROL_SEQUENCE_INTRODUCER}{body}{SGR_TERMINATOR}"

    def __str__(self) -> str:
        return self.as_str()

    def __bytes__(self) -> bytes:
        return self.as_str().encode("ascii")


@dataclass
class ResetControlSequence(SGRControlSequence):
    def arguments(self) -> tuple[str]:
        return ("0",)


@dataclass
class ConcatenatedSequence(SGRControlSequence):
    parts: list[SGRControlSequence]

    def arguments(self) -> Iterable[str]:
        return itertools.chain.from_iterable(seq.arguments() for seq in self.parts)


@dataclass
class ColorDefaultControlSequence(SGRControlSequence):
    region: Region = "foreground"

    def arguments(self) -> tuple[str]:
        if self.region == "foreground":
            return ("39",)
        else:
            return ("49",)


@dataclass
class GraphicsModeControlSequence(SGRControlSequence):
    mode: GraphicsMode
    set: bool = True

    def arguments(self) -> tuple[str]:
        value = self.mode.value

        if not self.set:
            # Convert set mode argument to reset mode argument.
            value += 20

            # Special case - BOLD is reset by 22 instead of 21
            if value == 21:
                value = 22

        return (str(value),)


@dataclass
class Color16ControlSequence(SGRControlSequence):
    color: StandardColor
    region: Region = "foreground"
    bright: bool = False

    OFFSET_MAP: ClassVar[dict[tuple[bool, Region], int]] = {
        (False, "foreground"): 30,
        (False, "background"): 40,
        (True, "foreground"): 90,
        (True, "background"): 100,
    }

    def _argument_offset(self) -> int:
        return self.OFFSET_MAP[(self.bright, self.region)]

    def arguments(self) -> tuple[str]:
        return (str(self._argument_offset() + self.color.value),)


@dataclass
class Color256ControlSequence(SGRControlSequence):
    color_id: Int8
    region: Region = "foreground"

    def arguments(self) -> tuple[str, str, str]:
        if self.region == "foreground":
            prefix = "38"
        else:
            prefix = "48"
        return prefix, "5", str(self.color_id)


@dataclass
class ColorRGBControlSequence(SGRControlSequence):
    red: Int8
    blue: Int8
    green: Int8
    region: Region = "foreground"

    def arguments(self) -> tuple[str, str, str, str, str]:
        if self.region == "foreground":
            prefix = "38"
        else:
            prefix = "48"
        return prefix, "2", str(self.red), str(self.blue), str(self.green)
