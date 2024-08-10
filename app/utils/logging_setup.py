# utils/logging_setup.py

"""
This script sets up a logging configuration for a Python application, including log rotation,
configurable log level and format, and dynamic inclusion of the script name in log messages.
The main function, setup_logging, ensures that all log messages are stored in a specified
directory and optionally outputs them to the console.

Features:
1. **Log Directory Creation**: Ensures that the specified log directory exists. If it does not,
   the directory is created using `os.makedirs` with `exist_ok=True` to handle existing directories
   gracefully.

2. **Log Filename**: The log file is named with a timestamp to ensure uniqueness per run and is stored
   in the specified log directory. The filename includes a timestamp in the format `daily_email_%Y%m%d_%H%M%S.log`.

3. **Log Rotation**: Utilizes `logging.handlers.TimedRotatingFileHandler` to rotate the log file at
   midnight every day. The rotated files are suffixed with a timestamp in the format `%Y%m%d_%H%M%S`.

4. **Configurable Log Level and Format**: Allows the caller to specify the log level (e.g., INFO, DEBUG)
   and log format through function parameters. The default log level is set to `logging.INFO`, and the
   default format is `'%(script_name)s - %(asctime)s %(message)s'`.

5. **Console Output**: Adds a `StreamHandler` to the logger to also output log messages to the console,
   making it easier to monitor logs in real-time.

6. **Script Name Inclusion**: Uses a custom logging filter to dynamically include the script name in each
   log message, making it clear which script generated each log entry.

Usage:
- Import the `setup_logging` function from this script.
- Call `setup_logging` with optional parameters for log folder, log level, and log format.
- The function returns the log filename being used.

Example:
```
from utils.logging_setup import setup_logging

log_file = setup_logging(log_folder='my_logs', log_level=logging.DEBUG, log_format='%(levelname)s %(message)s')
```

This example sets up logging to store logs in the 'my_logs' directory, with a log level of DEBUG,
and a custom log format that includes the log level and the message.
"""

import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

class ScriptNameFilter(logging.Filter):
    def filter(self, record):
        record.script_name = os.path.basename(record.pathname)
        return True

def setup_logging(log_folder="logs", log_level=logging.INFO, log_format='%(script_name)s - %(asctime)s %(message)s'):
    """
    Set up logging with log rotation and configurable log level and format.

    Args:
        log_folder (str): Directory to store log files.
        log_level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        log_format (str): Log message format.
    
    Returns:
        str: The filename of the log file being used.
    """
    # Ensure log directory exists
    os.makedirs(log_folder, exist_ok=True)
    
    # Define log filename with formatted timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = os.path.join(log_folder, f'daily_email_{timestamp}.log')

    # Set up log rotation handler
    file_handler = TimedRotatingFileHandler(log_filename, when='midnight', interval=1)
    file_handler.suffix = "%Y%m%d_%H%M%S"
    file_handler.setFormatter(logging.Formatter(log_format))

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Check if handlers already exist and clear them
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(logging.StreamHandler())

    # Add the script name filter
    script_name_filter = ScriptNameFilter()
    root_logger.addFilter(script_name_filter)

    logging.info("Logging initialized.")
    return log_filename