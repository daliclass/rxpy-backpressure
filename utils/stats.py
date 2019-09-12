from functools import wraps
from time import time
from typing import List


class Counter:
    def __init__(self):
        self.__timestamp_last_cached: float = 0
        self.__number_processed_events: int = 0
        self.__number_dropped_events: int = 0
        self.__waited_times: List[float] = []

    def time(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.__timestamp_last_cached == 0:
                self.__timestamp_last_cached = time()
            else:
                current_time = time()
                self.__waited_times.append(current_time - self.__timestamp_last_cached)
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

    def get_stats(self) -> dict:
        return {
            "dropped_events": self.__number_dropped_events,
            "successful_events": self.__number_processed_events
            - self.__number_dropped_events,
            "mean_time": sum(self.__waited_times) / len(self.__waited_times),
            "max_time": max(self.__waited_times),
        }
