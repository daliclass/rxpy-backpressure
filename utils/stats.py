from functools import wraps
from time import time


class Counter:
    def __init__(self):
        self.__timestamp_last_cached: float = 0
        self.__total_wait_time_sec: float = 0
        self.__number_processed_events: int = 0
        self.__number_dropped_events: int = 0

    def time(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.__timestamp_last_cached == 0:
                self.__timestamp_last_cached = time()
            else:
                current_time = time()
                self.__total_wait_time_sec += current_time
                self.__timestamp_last_cached = current_time
            return func(*args, **kwargs)

        return wrapper

    def dropped_event(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            if not ret:
                self.__number_dropped_events += 1
            return func(*args, **kwargs)

        return wrapper

    def processed_event(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.__number_processed_events += 1
            return func(*args, **kwargs)

        return wrapper
