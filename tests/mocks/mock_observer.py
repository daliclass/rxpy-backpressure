from unittest.mock import MagicMock

import time

from rxpy_backpressure.observer import Observer


class MockObserver(Observer):

    def __init__(self, include_sleeps: bool = False):
        self.on_next_mock = MagicMock()
        self.on_completed_mock = MagicMock()
        self.on_error_mock = MagicMock()
        self.include_sleeps: bool = include_sleeps

    def on_next(self, value):
        if self.include_sleeps:
            time.sleep(0.25)
        self.on_next_mock(value)

    def on_error(self, error):
        self.on_error_mock(error)

    def on_completed(self):
        self.on_completed_mock()
