from threading import Thread
from typing import Optional

from rxpy_backpressure.observer import Observer


class LatestBackPressureStrategy(Observer):

    def __init__(self, wrapped_observer: Observer):
        self.wrapped_observer: Observer = wrapped_observer
        self.__locked: bool = False
        self.message_cache: Optional = None
        self.error_cache: Optional = None

    def on_next(self, message):
        if self.is_locked():
            self.message_cache = message
            return

        self.function_runner(self.__on_next, message)

    @staticmethod
    def __on_next(self, message: any):
        self.wrapped_observer.on_next(message)
        if self.message_cache:
            self.function_runner(self.__on_next, self.message_cache)
            self.message_cache = None
        else:
            self.__unlock()

    @staticmethod
    def __run_function(self, message: any):
        self.wrapped_observer.on_next(message)
        if self.message_cache:
            self.function_runner(self.__on_next, self.message_cache)
            self.message_cache = None
        else:
            self.__unlock()

    def __lock(self):
        self.__locked = True

    def __unlock(self):
        self.__locked = False

    def is_locked(self) -> bool:
        return self.__locked

    def function_runner(self, func, message: any):
        self.__lock()
        Thread(target=func, args=(self, message)).start()

    def on_error(self, error: any):
        if self.is_locked():
            self.error_cache = error
            return

        self.function_runner(self.__on_error, error)

    @staticmethod
    def __on_error(self, error: any):
        self.wrapped_observer.on_error(error)
        if self.error_cache:
            self.function_runner(self.__on_error, self.error_cache)
            self.error_cache = None
        else:
            self.__unlock()

    def on_completed(self):
        self.wrapped_observer.on_completed()


def wrap_observer_with_latest_backpressure_strategy(observer: Observer) -> Observer:
    return LatestBackPressureStrategy(observer)