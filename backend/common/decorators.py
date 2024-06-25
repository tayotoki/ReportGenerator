import logging
import time
from functools import wraps


def task_logging(func):
    """
    Логер задач
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        logging.info(f"Started: {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Success: {func.__name__}")
        logging.info(
            f"time:{time.perf_counter() - start_time} s.",
        )
        return result

    return wrapper
