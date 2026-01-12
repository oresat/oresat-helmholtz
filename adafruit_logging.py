# SPDX-FileCopyrightText: 2019 Dave Astels for Adafruit Industries
# SPDX-FileCopyrightText: 2024 Pat Satyshur
#
# SPDX-License-Identifier: MIT

"""
`adafruit_logging`
==================

Logging module for CircuitPython


* Author(s): Dave Astels, Alec Delaney

Implementation Notes
--------------------

**Hardware:**


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. note::

    This module has a few key differences compared to its CPython counterpart, notably
    that loggers do not form a hierarchy that allows record propagation.
    Additionally, the default formatting for handlers is different.

Attributes
----------
    LEVELS: list
        A list of tuples representing the valid logging levels used by
        this module. Each tuple contains exactly two elements: one int and one
        str. The int in each tuple represents the relative severity of that
        level (00 to 50). The str in each tuple is the string representation of
        that logging level ("NOTSET" to "CRITICAL"; see below).
    NOTSET: int
        The NOTSET logging level can be used to indicate that a `Logger` should
        process any logging messages, regardless of how severe those messages are.
    DEBUG: int
        The DEBUG logging level, which is the lowest (least severe) real level.
    INFO: int
        The INFO logging level for informative/informational messages.
    WARNING: int
        The WARNING logging level, which is the default logging level, for warnings
        that should be addressed/fixed.
    ERROR: int
        The ERROR logging level for Python exceptions that occur during runtime.
    CRITICAL: int
        The CRITICAL logging level, which is the highest (most severe) level for
        unrecoverable errors that have caused the code to halt and exit.

"""

import os
import sys
import time
from collections import namedtuple

try:
    from typing import Dict, Hashable, Optional

    from typing_extensions import Protocol

    class WriteableStream(Protocol):
        """Any stream that can ``write`` strings"""

        def write(self, buf: str) -> int:
            """Write to the stream

            :param str buf: The string data to write to the stream
            """

except ImportError:
    pass

__version__ = "5.6.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Logger.git"

__all__ = [
    "LEVELS",
    "NOTSET",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "Handler",
    "StreamHandler",
    "logger_cache",
    "getLogger",
    "Logger",
    "NullHandler",
    "FileHandler",
    "LogRecord",
]

# The level module-global variables get created when loaded

LEVELS = [
    (00, "NOTSET"),
    (10, "DEBUG"),
    (20, "INFO"),
    (30, "WARNING"),
    (40, "ERROR"),
    (50, "CRITICAL"),
]

for __value, __name in LEVELS:
    globals()[__name] = __value


def _level_for(value: int) -> str:
    """Convert a numeric level to the most appropriate name.

    :param int value: a numeric level
    """
    for i, level in enumerate(LEVELS):
        if value == level[0]:
            return level[1]
        if value < level[0]:
            return LEVELS[i - 1][1]
    return LEVELS[0][1]


LogRecord = namedtuple("_LogRecord", ("name", "levelno", "levelname", "msg", "created", "args"))
"""An object used to hold the contents of a log record.  The following attributes can
be retrieved from it:

- ``name`` - The name of the logger
- ``levelno`` - The log level number
- ``levelname`` - The log level name
- ``msg`` - The log message
- ``created`` - When the log record was created
- ``args`` - The additional positional arguments provided
"""


def _logRecordFactory(name, level, msg, args):
    return LogRecord(name, level, _level_for(level), msg, time.monotonic(), args)


class Formatter:
    """
    Responsible for converting a LogRecord to an output string to be
    interpreted by a human or external system.

    Only implements a sub-set of CPython logging.Formatter behavior,
    but retains all the same arguments in order to match the API.

    The only init arguments currently supported are: fmt, defaults and
    style. All others are currently ignored

    The only two styles currently supported are '%' and '{'. The default
    style is '{'
    """

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: str = "%",
        validate: bool = True,
        defaults: Dict = None,
    ):
        self.fmt = fmt
        self.datefmt = datefmt
        self.style = style
        if self.style not in {"{", "%"}:
            raise ValueError("Only '%' and '{' formatting style are supported at this time.")

        self.validate = validate
        self.defaults = defaults

    def format(self, record: LogRecord) -> str:
        """
        Format the given LogRecord into an output string
        """
        if self.fmt is None:
            return record.msg

        vals = {
            "name": record.name,
            "levelno": record.levelno,
            "levelname": record.levelname,
            "message": record.msg,
            "created": record.created,
            "args": record.args,
        }
        if "{asctime}" in self.fmt or "%(asctime)s" in self.fmt:
            now = time.localtime()
            vals["asctime"] = (
                f"{now.tm_year}-{now.tm_mon:02d}-{now.tm_mday:02d} {now.tm_hour:02d}:{now.tm_min:02d}:{now.tm_sec:02d}"  # noqa: E501
            )

        if self.defaults:
            for key, val in self.defaults.items():
                if key not in vals:
                    vals[key] = val

        if self.style not in {"{", "%"}:
            raise ValueError("Only '%' and '{' formatting style are supported at this time.")

        if self.style == "%":
            return self.fmt % vals

        return self.fmt.format(**vals)


class Handler:
    """Base logging message handler."""

    def __init__(self, level: int = NOTSET) -> None:
        """Create Handler instance"""
        self.level = level
        self.formatter = None

    def setLevel(self, level: int) -> None:
        """
        Set the logging level of this handler.
        """
        self.level = level

    def format(self, record: LogRecord) -> str:
        """Generate a timestamped message.

        :param record: The record (message object) to be logged
        """
        if self.formatter:
            return self.formatter.format(record)
        return f"{record.created:<0.3f}: {record.levelname} - {record.msg}"

    def emit(self, record: LogRecord) -> None:
        """Send a message where it should go.
        Placeholder for subclass implementations.

        :param record: The record (message object) to be logged
        """

        raise NotImplementedError()

    def flush(self) -> None:
        """Placeholder for flush function in subclasses."""

    def setFormatter(self, formatter: Formatter) -> None:
        """
        Set the Formatter to be used by this Handler.
        """
        self.formatter = formatter


class StreamHandler(Handler):
    """Send logging messages to a stream, `sys.stderr` (typically
    the serial console) by default.

    :param stream: The stream to log to, default is `sys.stderr`;
        can accept any stream that implements ``stream.write()``
        with string inputs
    """

    terminator = "\n"

    def __init__(self, stream: Optional[WriteableStream] = None) -> None:
        super().__init__()
        if stream is None:
            stream = sys.stderr
        self.stream = stream
        """The stream to log to"""

    def format(self, record: LogRecord) -> str:
        """Generate a string to log

        :param record: The record (message object) to be logged
        """
        text = super().format(record)
        lines = text.splitlines()
        return self.terminator.join(lines)

    def emit(self, record: LogRecord) -> None:
        """Send a message to the console.

        :param record: The record (message object) to be logged
        """
        self.stream.write(self.format(record) + self.terminator)

    def flush(self) -> None:
        """flush the stream. You might need to call this if your messages
        are not appearing in the log file.
        """
        self.stream.flush()


class FileHandler(StreamHandler):
    """File handler for working with log files off of the microcontroller (like
    an SD card)

    :param str filename: The filename of the log file
    :param str mode: Whether to write ('w') or append ('a'); default is to append
    """

    terminator = "\r\n"

    def __init__(self, filename: str, mode: str = "a") -> None:
        if mode == "r":
            raise ValueError("Can't write to a read only file")
        super().__init__(open(filename, mode=mode))

    def close(self) -> None:
        """Closes the file"""
        self.stream.flush()
        self.stream.close()

    def emit(self, record: LogRecord) -> None:
        """Generate the message and write it to the file.

        :param record: The record (message object) to be logged
        """
        super().emit(record)
        self.stream.flush()


class RotatingFileHandler(FileHandler):
    """File handler for writing log files to flash memory or external memory such as an SD card.
    This handler implements a very simple log rotating system similar to the python function of the
    same name (https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler)

    If maxBytes is set, the handler will check to see if the log file is larger than the given
    limit. If the log file is larger than the limit, it is renamed and a new file is started.
    The old log file will be renamed with a numerical appendix '.1', '.2', etc... The variable
    backupCount controls how many old log files to keep. For example, if the filename is 'log.txt'
    and backupCount is 5, you will end up with six log files: 'log.txt', 'log.txt.1', 'log.txt.3',
    up to 'log.txt.5' Therefore, the maximum amount of disk space the logs can use is
    maxBytes*(backupCount+1).

    If either maxBytes or backupCount is not set, or set to zero, the log rotation is disabled.
    This will result in a single log file with a name `filename` that will grow without bound.

    :param str filename: The filename of the log file
    :param str mode: Whether to write ('w') or append ('a'); default is to append
    :param int maxBytes: The max allowable size of the log file in bytes.
    :param int backupCount: The number of old log files to keep.
    """

    def __init__(
        self,
        filename: str,
        mode: str = "a",
        maxBytes: int = 0,
        backupCount: int = 0,
    ) -> None:
        if maxBytes < 0:
            raise ValueError("maxBytes must be a positive number")
        if backupCount < 0:
            raise ValueError("backupCount must be a positive number")

        self._LogFileName = filename
        self._WriteMode = mode
        self._maxBytes = maxBytes
        self._backupCount = backupCount

        # Open the file and save the handle to self.stream
        super().__init__(self._LogFileName, mode=self._WriteMode)

    def doRollover(self) -> None:
        """Roll over the log files. This should not need to be called directly"""
        # At this point, we have already determined that we need to roll the log files.
        # Close the log file. Probably needed if we want to delete/rename files.
        self.close()

        for i in range(self._backupCount, 0, -1):
            CurrentFileName = self._LogFileName + "." + str(i)
            CurrentFileNamePlus = self._LogFileName + "." + str(i + 1)
            try:
                if i == self._backupCount:
                    # This is the oldest log file. Delete this one.
                    os.remove(CurrentFileName)
                else:
                    # Rename the current file to the next number in the sequence.
                    os.rename(CurrentFileName, CurrentFileNamePlus)
            except OSError as e:
                if e.args[0] == 2:
                    # File does not exsist. This is okay.
                    pass
                else:
                    raise e

        # Rename the current log to the first backup
        os.rename(self._LogFileName, CurrentFileName)

        # Reopen the file.
        self.stream = open(self._LogFileName, mode=self._WriteMode)

    def GetLogSize(self) -> int:
        """Check the size of the log file."""
        try:
            self.stream.flush()  # We need to call this or the file size is always zero.
            LogFileSize = os.stat(self._LogFileName)[6]
        except OSError as e:
            if e.args[0] == 2:
                # Log file does not exsist. This is okay.
                LogFileSize = None
            else:
                raise e
        return LogFileSize

    def emit(self, record: LogRecord) -> None:
        """Generate the message and write it to the file.

        :param record: The record (message object) to be logged
        """
        if (
            (self.GetLogSize() >= self._maxBytes)
            and (self._maxBytes > 0)
            and (self._backupCount > 0)
        ):
            self.doRollover()
        super().emit(record)


class NullHandler(Handler):
    """Provide an empty log handler.

    This can be used in place of a real log handler to more efficiently disable
    logging.
    """

    def emit(self, record: LogRecord) -> None:
        """Dummy implementation"""


logger_cache = {}
_default_handler = StreamHandler()


def _addLogger(logger_name: Hashable) -> None:
    """Adds the logger if it doesn't already exist"""
    if logger_name not in logger_cache:
        new_logger = Logger(logger_name)
        logger_cache[logger_name] = new_logger


def getLogger(logger_name: Hashable = "") -> "Logger":
    """Create or retrieve a logger by name; only retrieves loggers
    made using this function; if a Logger with this name does not
    exist it is created

    :param Hashable logger_name: The name of the `Logger` to create/retrieve, this
        is typically a ``str``.  If none is provided, the single root logger will
        be created/retrieved.  Note that unlike CPython, a blank string will also
        access the root logger.
    """
    _addLogger(logger_name)
    return logger_cache[logger_name]


class Logger:
    """The actual logger that will provide the logging API.

    :param Hashable name: The name of the logger, typically assigned by the
        value from `getLogger`; this is typically a ``str``
    :param int level: (optional) The log level, default is ``WARNING``
    """

    def __init__(self, name: Hashable, level: int = WARNING) -> None:
        """Create an instance."""
        self._level = level
        self.name = name
        """The name of the logger, this should be unique for proper
        functionality of `getLogger()`"""
        self._handlers = []
        self.emittedNoHandlerWarning = False

    def setLevel(self, log_level: int) -> None:
        """Set the logging cutoff level.

        :param int log_level: the lowest level to output
        """

        self._level = log_level

    def getEffectiveLevel(self) -> int:
        """Get the effective level for this logger.

        :return: the lowest level to output
        """

        return self._level

    def addHandler(self, hdlr: Handler) -> None:
        """Adds the handler to this logger.

        :param Handler hdlr: The handler to add
        """
        self._handlers.append(hdlr)

    def removeHandler(self, hdlr: Handler) -> None:
        """Remove handler from this logger.

        :param Handler hdlr: The handler to remove
        """
        self._handlers.remove(hdlr)

    def hasHandlers(self) -> bool:
        """Whether any handlers have been set for this logger"""
        return len(self._handlers) > 0

    def _log(self, level: int, msg: str, *args) -> None:
        record = _logRecordFactory(self.name, level, (msg % args) if args else msg, args)
        self.handle(record)

    def handle(self, record: LogRecord) -> None:
        """Pass the record to all handlers registered with this logger.

        :param LogRecord record: log record
        """
        if _default_handler is None and not self.hasHandlers() and not self.emittedNoHandlerWarning:
            sys.stderr.write(f"Logger '{self.name}' has no handlers and default handler is None\n")
            self.emittedNoHandlerWarning = True
            return

        emitted = False
        if record.levelno >= self._level:
            for handler in self._handlers:
                if record.levelno >= handler.level:
                    handler.emit(record)
                    emitted = True

            if not emitted and _default_handler and record.levelno >= _default_handler.level:
                _default_handler.emit(record)

    def log(self, level: int, msg: str, *args) -> None:
        """Log a message.

        :param int level: the priority level at which to log
        :param str msg: the core message string with embedded
            formatting directives
        :param args: arguments to ``msg % args``;
            can be empty
        """

        self._log(level, msg, *args)

    def debug(self, msg: str, *args) -> None:
        """Log a debug message.

        :param str msg: the core message string with embedded
            formatting directives
        :param args: arguments to ``msg % args``;
            can be empty
        """
        self._log(DEBUG, msg, *args)

    def info(self, msg: str, *args) -> None:
        """Log a info message.

        :param str msg: the core message string with embedded
            formatting directives
        :param args: arguments to ``msg % args``;
            can be empty
        """

        self._log(INFO, msg, *args)

    def warning(self, msg: str, *args) -> None:
        """Log a warning message.

        :param str msg: the core message string with embedded
            formatting directives
        :param args: arguments to ``msg % args``;
            can be empty
        """

        self._log(WARNING, msg, *args)

    def error(self, msg: str, *args) -> None:
        """Log a error message.

        :param str msg: the core message string with embedded
            formatting directives
        :param args: arguments to ``msg % args``;
            can be empty
        """

        self._log(ERROR, msg, *args)

    def critical(self, msg: str, *args) -> None:
        """Log a critical message.

        :param str msg: the core message string with embedded
            formatting directives
        :param args: arguments to ``msg % args``;
            can be empty
        """
        self._log(CRITICAL, msg, *args)

    def exception(self, err: Exception) -> None:
        """Convenience method for logging an ERROR with exception information.

        :param Exception err: the exception to be logged
        """
        try:
            import traceback
        except ImportError:
            self._log(
                ERROR,
                "%s: %s (No traceback on this board)",
                err.__class__.__name__,
                str(err),
            )
        else:
            lines = [str(err)] + traceback.format_exception(err)
            lines = str(err) + "".join(lines)
            # some of the returned strings from format_exception already have newlines in them,
            # so we can't add the indent in the above line - needs to be done separately
            lines = lines.replace("\n", "\n  ")
            self._log(ERROR, lines)


def critical(msg, *args, **kwargs):
    """
    Log a message with severity 'CRITICAL' on the root logger.
    """
    getLogger().critical(msg, *args, **kwargs)


def fatal(msg, *args, **kwargs):
    """
    Don't use this function, use critical() instead.
    """
    critical(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger.
    """
    getLogger().error(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """
    Log a message with severity 'WARNING' on the root logger.
    """
    getLogger().warning(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    """
    Don't use this function, use warning() instead.
    """
    warning(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """
    Log a message with severity 'INFO' on the root logger.
    """
    getLogger().info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """
    Log a message with severity 'DEBUG' on the root logger.
    """
    getLogger().debug(msg, *args, **kwargs)


def log(level, msg, *args, **kwargs):
    """
    Log 'msg % args' with the integer severity 'level' on the root logger.
    """
    getLogger().log(level, msg, *args, **kwargs)
