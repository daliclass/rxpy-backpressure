from unittest import TestCase
from unittest.mock import call

from rxpy_backpressure import BackPressure
from rxpy_backpressure.drop import DropBackPressureStrategy
from tests.mocks.mock_observer import MockObserver


class TestBufferBackPressureStrategy(TestCase):
    def test_when_on_next_called_and_wrapped_is_processing_then_buffer_messages_when_cache_is_full(
        self
    ):
        mock_observer: MockObserver = MockObserver(include_sleeps=True)
        buffer: DropBackPressureStrategy = BackPressure.BUFFER(mock_observer)
        messages = [
            {"id": 1, "payload": "OK"},
            {"id": 2, "payload": "OK"},
            {"id": 3, "payload": "OK"},
            {"id": 4, "payload": "OK"},
            {"id": 5, "payload": "OK"},
            {"id": 6, "payload": "OK"},
            {"id": 7, "payload": "OK"},
            {"id": 8, "payload": "OK"},
            {"id": 9, "payload": "OK"},
            {"id": 10, "payload": "OK"},
            {"id": 11, "payload": "OK"},
            {"id": 12, "payload": "OK"},
        ]

        buffer.on_next(messages[0])
        buffer.on_next(messages[1])
        buffer.on_next(messages[2])
        buffer.on_next(messages[3])
        buffer.on_next(messages[4])
        buffer.on_next(messages[5])

        while buffer.is_locked():
            pass  # wait to become unlocked

        buffer.on_next(messages[6])
        buffer.on_next(messages[7])
        buffer.on_next(messages[8])
        buffer.on_next(messages[9])
        buffer.on_next(messages[10])
        buffer.on_next(messages[11])

        while buffer.is_locked():
            pass  # wait to become unlocked

        mock_observer.on_next_mock.assert_has_calls(
            [
                call(messages[0]),
                call(messages[1]),
                call(messages[2]),
                call(messages[3]),
                call(messages[4]),
                call(messages[5]),
                call(messages[6]),
                call(messages[7]),
                call(messages[8]),
                call(messages[9]),
                call(messages[10]),
                call(messages[11]),
            ]
        )

    def test_when_on_error_called_and_wrapped_is_processing_then_buffer_messages_when_cache_is_full(
        self
    ):
        mock_observer: MockObserver = MockObserver(include_sleeps=True)
        buffer: DropBackPressureStrategy = BackPressure.BUFFER(mock_observer)
        messages = [
            {"id": 1, "payload": "OK"},
            {"id": 2, "payload": "OK"},
            {"id": 3, "payload": "OK"},
            {"id": 4, "payload": "OK"},
            {"id": 5, "payload": "OK"},
            {"id": 6, "payload": "OK"},
            {"id": 7, "payload": "OK"},
            {"id": 8, "payload": "OK"},
            {"id": 9, "payload": "OK"},
            {"id": 10, "payload": "OK"},
            {"id": 11, "payload": "OK"},
            {"id": 12, "payload": "OK"},
        ]

        buffer.on_error(messages[0])
        buffer.on_error(messages[1])
        buffer.on_error(messages[2])
        buffer.on_error(messages[3])
        buffer.on_error(messages[4])
        buffer.on_error(messages[5])

        while buffer.is_locked():
            pass  # wait to become unlocked

        buffer.on_error(messages[6])
        buffer.on_error(messages[7])
        buffer.on_error(messages[8])
        buffer.on_error(messages[9])
        buffer.on_error(messages[10])
        buffer.on_error(messages[11])

        while buffer.is_locked():
            pass  # wait to become unlocked

        mock_observer.on_error_mock.assert_has_calls(
            [
                call(messages[0]),
                call(messages[1]),
                call(messages[2]),
                call(messages[3]),
                call(messages[4]),
                call(messages[5]),
                call(messages[6]),
                call(messages[7]),
                call(messages[8]),
                call(messages[9]),
                call(messages[10]),
                call(messages[11]),
            ]
        )
