from time import sleep
from unittest import TestCase
from unittest.mock import call

from rxpy_backpressure.backpressure import BackPressure
from rxpy_backpressure.sized_buffer import SizedBufferBackPressureStrategy
from rxpy_backpressure.observer import Observer
from tests.mocks.mock_observer import MockObserver


class TestDropBackPressureStrategy(TestCase):
    def test_when_on_complete_called_then_defer_to_wrapped_observer(self):
        mock_observer: MockObserver = MockObserver()
        buffer: Observer = SizedBufferBackPressureStrategy(mock_observer, cache_size=1)

        buffer.on_completed()
        mock_observer.on_completed_mock.assert_called_once()

    def test_when_on_error_called_then_defer_to_wrapped_observer(self):
        mock_observer: MockObserver = MockObserver()
        buffer: Observer = SizedBufferBackPressureStrategy(mock_observer, cache_size=1)
        error: Exception = Exception("Some error happened")

        buffer.on_error(error)
        mock_observer.on_error_mock.assert_called_once_with(error)

    def test_when_on_next_called_and_wrapped_is_not_processing_then_call_wrapped(self):
        mock_observer: MockObserver = MockObserver()
        buffer: Observer = SizedBufferBackPressureStrategy(mock_observer, cache_size=1)
        message: dict = {"id": 1, "payload": "OK"}

        buffer.on_next(message)
        mock_observer.on_next_mock.assert_called_once_with(message)

    def test_when_on_next_called_cache_subsequent_messages_and_call_afterwards(self):
        mock_observer: MockObserver = MockObserver(include_sleeps=True)
        buffer: SizedBufferBackPressureStrategy = BackPressure.SIZED_BUFFER(
            mock_observer
        )
        messages = [
            {"id": 0, "payload": "OK"},
            {"id": 1, "payload": "OK"},
            {"id": 2, "payload": "OK"},
        ]

        buffer.on_next(messages[0])
        buffer.on_next(messages[1])
        buffer.on_next(messages[2])

        while buffer.is_locked():
            sleep(0.25)

        mock_observer.on_next_mock.assert_has_calls(
            [
                call(messages[0]),
                call(messages[1]),
                call(messages[1]),
                call(messages[2]),
                call(messages[2]),
            ]
        )

    def test_when_on_error_called_cache_subsequent_messages_and_call_afterwards(self):
        mock_observer: MockObserver = MockObserver(include_sleeps=True)
        buffer: SizedBufferBackPressureStrategy = BackPressure.SIZED_BUFFER(
            mock_observer
        )
        messages = [
            {"id": 0, "payload": "OK"},
            {"id": 1, "payload": "OK"},
            {"id": 2, "payload": "OK"},
        ]

        buffer.on_error(messages[0])
        buffer.on_error(messages[1])
        buffer.on_error(messages[2])

        while buffer.is_locked():
            sleep(0.25)

        mock_observer.on_error_mock.assert_has_calls(
            [
                call(messages[0]),
                call(messages[1]),
                call(messages[1]),
                call(messages[2]),
                call(messages[2]),
            ]
        )

    def test_when_on_next_buffer_following_messages(self):
        mock_observer: MockObserver = MockObserver(include_sleeps=True)
        buffer: SizedBufferBackPressureStrategy = BackPressure.SIZED_BUFFER(
            mock_observer, cache_size=10
        )
        messages = [
            {"id": 0, "payload": "OK"},
            {"id": 1, "payload": "OK"},
            {"id": 2, "payload": "OK"},
            {"id": 3, "payload": "OK"},
            {"id": 4, "payload": "OK"},
            {"id": 5, "payload": "OK"},
            {"id": 6, "payload": "OK"},
            {"id": 7, "payload": "OK"},
        ]

        buffer.on_next(messages[0])
        buffer.on_next(messages[1])
        buffer.on_next(messages[2])
        buffer.on_next(messages[3])

        while buffer.is_locked():
            sleep(0.25)

        buffer.on_next(messages[4])
        buffer.on_next(messages[5])
        buffer.on_next(messages[6])
        buffer.on_next(messages[7])

        while buffer.is_locked():
            sleep(0.25)

        mock_observer.on_next_mock.assert_has_calls(
            [
                call(messages[0]),
                call(messages[1]),
                call(messages[1]),
                call(messages[2]),
                call(messages[2]),
                call(messages[3]),
                call(messages[3]),
                call(messages[4]),
                call(messages[5]),
                call(messages[5]),
                call(messages[6]),
                call(messages[6]),
                call(messages[7]),
                call(messages[7]),
            ]
        )

    def test_on_next_drop_new_message_when_buffer_full(self):
        mock_observer: MockObserver = MockObserver(include_sleeps=True)
        buffer: SizedBufferBackPressureStrategy = BackPressure.SIZED_BUFFER(
            mock_observer, cache_size=2
        )
        messages = [
            {"id": 0, "payload": "OK"},
            {"id": 1, "payload": "OK"},
            {"id": 2, "payload": "OK"},
            {"id": 3, "payload": "OK"},
            {"id": 4, "payload": "OK"},
            {"id": 5, "payload": "OK"},
            {"id": 6, "payload": "OK"},
            {"id": 7, "payload": "OK"},
        ]

        buffer.on_next(messages[0])
        buffer.on_next(messages[1])
        buffer.on_next(messages[2])
        buffer.on_next(messages[3])

        while buffer.is_locked():
            sleep(0.25)

        buffer.on_next(messages[4])
        buffer.on_next(messages[5])
        buffer.on_next(messages[6])
        buffer.on_next(messages[7])

        while buffer.is_locked():
            sleep(0.25)

        mock_observer.on_next_mock.assert_has_calls(
            [
                call(messages[0]),
                call(messages[1]),
                call(messages[1]),
                call(messages[4]),
                call(messages[5]),
                call(messages[5]),
            ]
        )
