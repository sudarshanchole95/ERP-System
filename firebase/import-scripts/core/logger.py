import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "importer.log"

FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter(FORMAT))

file_handler = RotatingFileHandler(str(LOG_FILE), maxBytes=5_000_000, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(FORMAT))

logger = logging.getLogger("importer")
logger.setLevel(logging.DEBUG)
logger.addHandler(console)
logger.addHandler(file_handler)

# Reduce noise
logging.getLogger("google").setLevel(logging.WARNING)
logging.getLogger("firebase_admin").setLevel(logging.WARNING)