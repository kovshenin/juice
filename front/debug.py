import logging
from django.conf import settings

logger = logging.getLogger()
hdlr = logging.FileHandler(settings.LOG_FILE)
formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s"%(message)s"','%Y-%m-%d %H:%M:%S') 

hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.NOTSET)

def debug(msg):
    logger.debug(msg)
