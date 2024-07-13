# utils/logging_setup.py

import os
import logging
from datetime import datetime

def setup_logging():
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    log_filename = os.path.join(log_folder, f"email_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s %(message)s'
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info("Logging initialized.")
    return log_filename
