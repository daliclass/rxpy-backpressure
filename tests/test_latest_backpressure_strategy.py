from unittest import TestCase
from unittest.mock import call

from rxpy_backpressure.backpressure import BackPressure
from rxpy_backpressure.latest import LatestBackPressureStrategy
from rxpy_backpressure.observer import Observer
from tests.mocks.mock_observer import MockObserver


class TestLatestBackPressureStrategy(TestCase):
    def test_when_on_complete_called_then_defer_to_wrapped_observer(self):
        mock_observer: MockObserver = MockObserver()
        latest: Observer = LatestBackPressureStrategy(mock_observer)

        latest.on_completed()
        mock_observer.on_completed_mock.assert_called_once()

    def test_when_on_error_called_then_defer_to_wrapped_observer(self):
        mock_observer: MockObserver = MockObserver()
        latest: Observer = LatestBackPressureStrategy(mock_observer)
        error: Exception = Exception("Some error happened")

        latest.on_error(error)
        mock_observer.on_error_mock.assert_called_once_with(error)

    def test_when_on_next_called_and_wrapped_is_not_processing_then_call_wrapped(self):
        mock_observer: MockObserver = MockObserver()
        latest: Observer = LatestBackPressureStrategy(mock_observer)
        message: dict = {"id": 1, "payload": "OK"}

        latest.on_next(message)
        mock_observer.on_next_mock.assert_called_once_with(message)

    """
        Integration style tests to check that the asynchronous behaviour of this strategy
        works as expected.
    """

    def test_when_on_next_called_and_wrapped_is_processing_then_cache_latest_message_only(
        self
    ):
        mock_observer: MockObserver = MockObserver(include_sleeps=True)
        latest: LatestBackPressureStrategy = BackPressure.LATEST(mock_observer)
        messages = [
            {"id": 1, "payload": "OK"},
            {"id": 2, "payload": "OK"},
            {"id": 3, "payload": "OK"},
            {"id": 4, "payload": "OK"},
            {"id": 5, "payload": "OK"},
            {"id": 6, "payload": "OK"},
        ]

        latest.on_next(messages[0])
        latest.on_next(messages[1])
        latest.on_next(messages[2])

        while latest.is_locked():
            pass  # wait to become unlocked

        latest.on_next(messages[3])
        latest.on_next(messages[4])
        latest.on_next(messages[5])

        while latest.is_locked():
            pass  # wait to become unlocked

        mock_observer.on_next_mock.assert_has_calls(
            [call(messages[0]), call(messages[2]), call(messages[3]), call(messages[5])]
        )

    def test_when_on_error_called_and_wrapped_is_processing_then_cache_latest_message_only(
        self
    ):
        mock_observer: MockObserver = MockObserver(include_sleeps=True)
        latest: LatestBackPressureStrategy = BackPressure.LATEST(mock_observer)
        errors = [
            {"id": 1, "payload": "OK"},
            {"id": 2, "payload": "OK"},
            {"id": 3, "payload": "OK"},
            {"id": 4, "payload": "OK"},
            {"id": 5, "payload": "OK"},
            {"id": 6, "payload": "OK"},
        ]

        latest.on_error(errors[0])
        latest.on_error(errors[1])
        latest.on_error(errors[2])

        while latest.is_locked():
            pass  # wait to become unlocked

        latest.on_error(errors[3])
        latest.on_error(errors[4])
        latest.on_error(errors[5])

        while latest.is_locked():
            pass  # wait to become unlocked

        mock_observer.on_error_mock.assert_has_calls(
            [call(errors[0]), call(errors[2]), call(errors[3]), call(errors[5])]
        )
