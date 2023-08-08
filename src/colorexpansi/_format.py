"""
String formatting.
"""
import string
from typing import Any


class ColorFormatter(string.Formatter):
    spec_separator: str

    def __init__(self, sep: str = "$") -> None:
        self.spec_separator = sep

    def format_field(self, value: Any, format_spec: str) -> str:
        value_spec, _sep, color_spec = format_spec.partition(self.spec_separator)

        return super().format_field(value, value_spec)
