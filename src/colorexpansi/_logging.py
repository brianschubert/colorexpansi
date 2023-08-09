"""
Logging extensions.
"""
from __future__ import annotations

import logging
from typing import Literal

from ._format import ANSIStringFormatter


class ANSILogFormatter(logging.Formatter):
    """Format ``logging.LogRecord``s using ANSI escape sequences."""

    _formatter: ANSIStringFormatter

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        validate: bool = True,
        formatter: ANSIStringFormatter = ANSIStringFormatter(),
    ) -> None:
        super().__init__(fmt, datefmt, "{", validate)
        self._formatter = formatter

    def formatMessage(self, record: logging.LogRecord) -> str:
        return self._formatter.format(self._fmt, record.__dict__)
