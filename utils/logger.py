#!/usr/bin/env python3
"""
Logging Utilities
Centralized logging configuration for the PSEO system
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str = 'pseo',
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """
    Set up a logger with consistent formatting

    Args:
        name: Logger name (default: 'pseo')
        level: Logging level (default: INFO)
        log_file: Optional file path for log output
        console: Whether to log to console (default: True)

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logger('my_agent', level=logging.DEBUG)
        >>> logger.info("Agent initialized")
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Default logger for the PSEO system
pseo_logger = setup_logger('pseo', level=logging.INFO)
