import logging
from core.config import settings

def setup_logger():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    return logging.getLogger("pool_fish_app")