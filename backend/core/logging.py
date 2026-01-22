"""
Structured JSON logging configuration.
Provides consistent, parseable logs for production monitoring.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import Processor

from core.config import settings


def setup_logging() -> None:
    """
    Configure structured logging for the application.
    Uses JSON formatting in production, pretty printing in development.
    """
    # Shared processors for all loggers
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if settings.environment == "development":
        # Pretty console output for development
        processors: list[Processor] = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    else:
        # JSON output for production
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging to use structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: The logger name, typically __name__.
    
    Returns:
        A bound structlog logger instance.
    """
    return structlog.get_logger(name)


def log_with_context(
    logger: structlog.stdlib.BoundLogger,
    level: str,
    message: str,
    **context: Any,
) -> None:
    """
    Log a message with additional context.
    
    Args:
        logger: The logger instance to use.
        level: The log level (info, warning, error, etc.).
        message: The log message.
        **context: Additional context key-value pairs.
    """
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message, **context)
