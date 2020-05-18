"""Logging utilities."""

import logging
import sys

class _NiceFormatter(logging.Formatter):
    """winston-esque log formatter"""
    message_format = "%(asctime)s (%(name)s) - %(levelname)s: %(message)s"
    date_format = "%d %b %Y %H:%M:%S"

    def __init__(self):
        super(_NiceFormatter, self).__init__(
            self.message_format, self.date_format)

    def format(self, record):
        if record.levelno < logging.WARNING:
            record.levelname = record.levelname.lower()

        return super(_NiceFormatter, self).format(record)

default_log_formatter = _NiceFormatter()
default_log_handler = logging.StreamHandler(sys.stdout)
default_log_handler.setFormatter(default_log_formatter)
default_level = logging.INFO

_loggers = {}
def get(name=None) -> logging.Logger:
    """Create/get a logger.

    :param name: desired logger name. If None, default logger is returned.
    """
    if name not in _loggers:
        log = logging.getLogger(name) if name else logging.getLogger()

        log.setLevel(default_level)
        if not log.handlers:
            log.addHandler(default_log_handler)

        _loggers[name] = log

    return _loggers[name]

class LoggerMixin:
    """Mixin providing :class:`~logging.Logger` instance as "log" attribute."""
    _logger: logging.Logger

    @property
    def log(self) -> logging.Logger:
        if not hasattr(self, "_logger") or not self._logger:
            self._logger = get(self.__class__.__name__)

        return self._logger
