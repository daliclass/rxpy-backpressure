from typing import List, Any, Optional

from rxpy_backpressure.function_runner import thread_function_runner
from rxpy_backpressure.locks import Lock, BooleanLock
from rxpy_backpressure.observer import Observer
from utils.logging import Logger
from utils.stats import Counter


class SizedBufferBackPressureStrategy(Observer):
    counter: Counter = Counter()

    def __init__(self, wrapped_observer: Observer, cache_size: int):
        self.wrapped_observer: Observer = wrapped_observer
        self.__function_runner = thread_function_runner
        self.__lock: Lock = BooleanLock()
        self.__cache_size: Optional[int] = cache_size
        self.__message_cache: List = []
        self.__error_cache: List = []
        self.__logger = Logger()

    @counter.processed_event
    @counter.time
    def on_next(self, message):
        if self.__lock.is_locked():
            if not self.__update_cache(self.__message_cache, message):
                self.__logger.warning("value not added, buffer full")
        else:
            self.__lock.lock()
            self.__function_runner(self, self.__on_next, message)

    @staticmethod
    def __on_next(self, message: any):
        self.wrapped_observer.on_next(message)
        if len(self.__message_cache) > 0:
            self.__function_runner(self, self.__on_next, self.__message_cache.pop(0))
        else:
            self.__lock.unlock()

    def on_error(self, error: any):
        if self.__lock.is_locked():
            if not self.__update_cache(self.__error_cache, error):
                self.__logger.warning("value not added, buffer full")
        else:
            self.__lock.lock()
            self.__function_runner(self, self.__on_error, error)

    @staticmethod
    def __on_error(self, error: any):
        self.wrapped_observer.on_error(error)
        if len(self.__error_cache) > 0:
            self.__function_runner(self, self.__on_error, self.__error_cache.pop(0))
        else:
            self.__lock.unlock()

    @counter.dropped_event
    def __update_cache(self, cache: List, item: Any) -> bool:
        if self.__cache_size is None or len(cache) < self.__cache_size:
            cache.append(item)
            return True
        return False

    def on_completed(self):
        self.wrapped_observer.on_completed()

    def is_locked(self):
        return self.__lock.is_locked()


def wrap_observer_with_sized_buffer_strategy(
    observer: Observer, cache_size: int = 50
) -> Observer:
    return SizedBufferBackPressureStrategy(observer, cache_size=cache_size)
