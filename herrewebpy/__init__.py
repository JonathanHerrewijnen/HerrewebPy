from . import *
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        #logging.FileHandler('.log'),  # Log file handler
        logging.StreamHandler()  # Console handler
    ]
)

logger = logging.getLogger(__name__)