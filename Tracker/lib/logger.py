import logging

logging.basicConfig(filename="tracker.log", level=logging.INFO)
LOGGER = logging.getLogger(name="Logger")
CoreLogger = logging.getLogger(name="CoreLogger")