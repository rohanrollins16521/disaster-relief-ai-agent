import logging
import json

logger = logging.getLogger("disaster_assistant")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log_event(event: dict):
    logger.info(json.dumps(event))
