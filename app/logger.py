
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

def get_logger(name: str = "app"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured

    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_fmt = logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
    ch.setFormatter(ch_fmt)

    # Rotating file handler
    fh = RotatingFileHandler(LOG_FILE, maxBytes=512_000, backupCount=3)
    fh.setLevel(logging.INFO)
    fh_fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    fh.setFormatter(fh_fmt)

    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.propagate = False
    return logger
