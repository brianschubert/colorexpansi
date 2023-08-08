"""
String formatting.
"""

import string
from typing import Any, Final

from ._ansi import ResetControlSequence
from ._spec import parse_control

_RESET_SEQ: Final[str] = ResetControlSequence().as_str()


class ColorFormatter(string.Formatter):
    spec_separator: str

    def __init__(self, sep: str = "$") -> None:
        self.spec_separator = sep

    def format_field(self, value: Any, format_spec: str) -> str:
        value_spec, _sep, color_spec = format_spec.partition(self.spec_separator)

        formatted_value = super().format_field(value, value_spec)

        if not color_spec:
            return formatted_value

        style_cs = parse_control(color_spec)

        return f"{style_cs}{formatted_value}{_RESET_SEQ}"
