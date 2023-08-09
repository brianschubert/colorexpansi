"""
Logging extensions.
"""
from __future__ import annotations

import logging
from typing import Literal


class ANSILogFormatter(logging.Formatter):
    """Format ``logging.LogRecord``s using ANSI escape sequences."""

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal["%", "$", "{"] = "%",
        validate: bool = True,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate)
