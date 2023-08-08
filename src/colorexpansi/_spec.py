"""
Parsing color specifications.
"""

import re
from typing import Final

from ._ansi import GraphicsMode, SGRControlSequence, StandardColor

_COLOR_IDENTS: Final[dict[str, StandardColor]] = {
    "k": StandardColor.BLACK,
    "r": StandardColor.RED,
    "g": StandardColor.GREEN,
    "y": StandardColor.YELLOW,
    "b": StandardColor.BLUE,
    "m": StandardColor.MAGENTA,
    "c": StandardColor.CYAN,
    "w": StandardColor.WHITE,
}


_MODE_IDENTS: Final[dict[str, GraphicsMode]] = {
    "b": GraphicsMode.BOLD,
    "f": GraphicsMode.DIM,
    "i": GraphicsMode.ITALIC,
    "u": GraphicsMode.UNDERLINE,
    "k": GraphicsMode.BLINK,
    "r": GraphicsMode.REVERSE,
    "h": GraphicsMode.HIDDEN,
    "s": GraphicsMode.STRIKE,
}

_COLOR_SPECIFIER: Final[str] = f"[{''.join(_COLOR_IDENTS.keys())}]+"

_MODE_SPECIFIER: Final[str] = f"[{''.join(_MODE_IDENTS.keys())}]+"

_SPECIFICATION_GRAMMAR: Final[re.Pattern] = re.compile(
    rf"""
    (?P<foreground>{_COLOR_SPECIFIER})?
    (?:\.(?P<background>{_COLOR_SPECIFIER}))?
    (?:\+(?P<add_mode>{_MODE_SPECIFIER}))?
    (?:-(?P<sub_mode>{_MODE_SPECIFIER}))?
    """,
    flags=re.VERBOSE,
)


def parse_control(spec: str) -> SGRControlSequence:
    raise NotImplementedError
