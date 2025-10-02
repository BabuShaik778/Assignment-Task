import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    logger = logging.getLogger("api_gateway")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    fmt = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s %(module)s %(funcName)s')
    handler.setFormatter(fmt)
    logger.handlers = [handler]
    return logger

logger = setup_logging()
