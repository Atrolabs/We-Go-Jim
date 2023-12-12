import os
import logging
from logging.handlers import RotatingFileHandler

def configure_logging(logs_folder='../logs', log_file_name='app.log', max_file_size=10*1024*1024, backup_count=5, log_level=logging.ERROR):
    """
    Configure logging to save logs to a file.

    Parameters:
        - logs_folder (str): The folder path where logs will be saved.
        - log_file_name (str): The name of the log file.
        - max_file_size (int): The maximum size of each log file in bytes before it rotates.
        - backup_count (int): The number of backup log files to keep.
        - log_level (int): The logging level (e.g., logging.ERROR, logging.INFO, logging.DEBUG).

    Returns:
        None
    """
    # Configure the logs folder path
    logs_folder_path = os.path.join(os.path.dirname(__file__), logs_folder)

    # Create the logs folder if it doesn't exist
    os.makedirs(logs_folder_path, exist_ok=True)

    # Configure the logging
    log_file_path = os.path.join(logs_folder_path, log_file_name)

    # Create a rotating file handler
    file_handler = RotatingFileHandler(log_file_path, maxBytes=max_file_size, backupCount=backup_count)

    # Set the logging level
    file_handler.setLevel(log_level)

    # Create a formatter and attach it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the root logger
    logging.getLogger('').addHandler(file_handler)

def log_error(message):
    """
    Log an error message.

    Parameters:
        - message (str): The error message to log.

    Returns:
        None
    """
    logging.error(message)