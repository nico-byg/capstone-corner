"""
logger.py
This module provides functionality to write entries into a log file 
"""

import logging
import os
import datetime

def write_to_log(log_file, message, severity="WARNING"):
    '''
    write_to_log
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Ensure the log file exists; if not, create it
    if not os.path.exists(log_file):
        open(log_file, 'a').close()
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Avoid adding multiple handlers if function is called repeatedly
    if not logger.handlers:
        logger.addHandler(file_handler)

    if severity.upper() == "DEBUG":
        logger.debug(message)
    elif severity.upper() == "WARNING":
        logger.warning(message)
    elif severity.upper() == "ERROR":
        logger.error(message)
    elif severity.upper() == "CRITICAL":
        logger.critical(message)
    else:
        logger.info(message)

    # Check the log file size to ensure it doesn't grow too big. 
    manage_log_size(log_file)


def manage_log_size(log_file, max_size=5*1024*1024):
    '''
    manage_log_size
    '''
    if os.path.exists(log_file) and os.path.getsize(log_file) > max_size:
        # Read all log entries and filter out those older than 6 months
        six_months_ago = datetime.datetime.now() - datetime.timedelta(days=182)
        new_lines = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
            # Try to parse the date from the log line
                try:
                    date_str = line.split(' - ')[0]
                    log_time = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S,%f')
                    if log_time >= six_months_ago:
                        new_lines.append(line)
                except Exception:
                    # If parsing fails, keep the line (could be a malformed line)
                    new_lines.append(line)
        
        # Overwrite the log file with filtered lines
        with open(log_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        open(log_file, 'a').close()

# Testing of the log file function
# Delete below this line before completing

message = "Test Debug Message"
log_file = r'./res/test.log'
message = "Test Debug Message"
write_to_log(log_file, message, "DEBUG")
message = "Test Warning Message"
write_to_log(log_file, message, "WARNING")
message = "Test Error Message"
write_to_log(log_file, message, "ERROR")
message = "Test Critical Message"
write_to_log(log_file, message, "CRITICAL")
message = "Test Default Message"
write_to_log(log_file, message)
message = "Test Info Message"
write_to_log(log_file, message, "INFO")