"""
Parsing color specifications.
"""

import re
from typing import Final

import colorexpansi._ansi as ansi

_COLOR_IDENTS: Final[dict[str, ansi.StandardColor]] = {
    "k": ansi.StandardColor.BLACK,
    "r": ansi.StandardColor.RED,
    "g": ansi.StandardColor.GREEN,
    "y": ansi.StandardColor.YELLOW,
    "b": ansi.StandardColor.BLUE,
    "m": ansi.StandardColor.MAGENTA,
    "c": ansi.StandardColor.CYAN,
    "w": ansi.StandardColor.WHITE,
}


_MODE_IDENTS: Final[dict[str, ansi.GraphicsMode]] = {
    "b": ansi.GraphicsMode.BOLD,
    "f": ansi.GraphicsMode.FAINT,
    "i": ansi.GraphicsMode.ITALIC,
    "u": ansi.GraphicsMode.UNDERLINE,
    "k": ansi.GraphicsMode.BLINK,
    "r": ansi.GraphicsMode.REVERSE,
    "h": ansi.GraphicsMode.HIDDEN,
    "s": ansi.GraphicsMode.STRIKE,
}

_COLOR_SPECIFIER: Final[str] = f"[{''.join(_COLOR_IDENTS.keys())}]+"

_MODE_SPECIFIER: Final[str] = f"[{''.join(_MODE_IDENTS.keys())}]+"

_SPECIFICATION_GRAMMAR: Final[re.Pattern] = re.compile(
    rf"""
    (?P<foreground>{_COLOR_SPECIFIER})?
    (?:\.(?P<background>{_COLOR_SPECIFIER}))?
    (?:\+(?P<add_modes>{_MODE_SPECIFIER}))?
    (?:-(?P<sub_modes>{_MODE_SPECIFIER}))?
    """,
    flags=re.VERBOSE,
)


def parse_control(spec: str) -> ansi.SGRControlSequence:
    match = _SPECIFICATION_GRAMMAR.fullmatch(spec)
    if match is None:
        # TODO richer error messages
        raise ValueError("invalid spec")

    groups = match.groupdict()

    parts = []

    if foreground := groups["foreground"]:
        parts.append(
            ansi.Color16ControlSequence(_COLOR_IDENTS[foreground], region="foreground")
        )

    if background := groups["background"]:
        parts.append(
            ansi.Color16ControlSequence(_COLOR_IDENTS[background], region="background")
        )

    if add_modes := groups["add_modes"]:
        parts.extend(
            ansi.GraphicsModeControlSequence(_MODE_IDENTS[mode], set=True)
            for mode in add_modes
        )

    if sub_modes := groups["sub_modes"]:
        parts.extend(
            ansi.GraphicsModeControlSequence(_MODE_IDENTS[mode], set=False)
            for mode in sub_modes
        )

    return ansi.ConcatenatedSequence(parts)
