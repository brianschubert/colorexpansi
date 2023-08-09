"""
Logging extensions.
"""
from __future__ import annotations

import logging

from ._format import ANSIStringFormatter


class ANSILogFormatter(logging.Formatter):
    """Format ``logging.LogRecord``s using ANSI escape sequences."""

    _formatter: ANSIStringFormatter

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        formatter: ANSIStringFormatter = ANSIStringFormatter(),
    ) -> None:
        # Must set style="{" so that timestamp detection in format string works correctly.
        # Otherwise, asctime won't be added to the log records.
        super().__init__(fmt, datefmt, style="{", validate=False)
        self._formatter = formatter

    def formatMessage(self, record: logging.LogRecord) -> str:
        return self._formatter.format(self._fmt, **record.__dict__)
