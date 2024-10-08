import logging
import sys


class LoggerUtil:
    @staticmethod
    def get_logger():
        logger = logging.getLogger()
        if not logger.hasHandlers():
            # Make sure to send logs to stdout (picked up by CloudWatch)
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        logger.setLevel(logging.INFO)
        return logger
