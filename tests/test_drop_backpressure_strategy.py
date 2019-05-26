from unittest import TestCase
from unittest.mock import call

from rxpy_backpressure.backpressure import BackPressure
from rxpy_backpressure.drop import DropBackPressureStrategy
from rxpy_backpressure.observer import Observer
from tests.mocks.mock_observer import MockObserver


class TestDropBackPressureStrategy(TestCase):

    def test_when_on_complete_called_then_defer_to_wrapped_observer(self):
        mock_observer: MockObserver = MockObserver()
        drop: Observer = DropBackPressureStrategy(mock_observer, cache_size=1)

        drop.on_completed()
        mock_observer.on_completed_mock.assert_called_once()

    def test_when_on_error_called_then_defer_to_wrapped_observer(self):
        mock_observer: MockObserver = MockObserver()
        drop: Observer = DropBackPressureStrategy(mock_observer, cache_size=1)
        error: Exception = Exception("Some error happened")

        drop.on_error(error)
        mock_observer.on_error_mock.assert_called_once_with(error)

    def test_when_on_next_called_and_wrapped_is_not_processing_then_call_wrapped(self):
        mock_observer: MockObserver = MockObserver()
        drop: Observer = DropBackPressureStrategy(mock_observer, cache_size=1)
        message: dict = {'id': 1, 'payload': "OK"}

        drop.on_next(message)
        mock_observer.on_next_mock.assert_called_once_with(message)

    """
        Integration style tests to check that the asynchronous behaviour of this strategy
        works as expected.
    """
    def test_when_on_next_called_and_wrapped_is_processing_then_drop_messages_when_cache_is_full(self):
        mock_observer: MockObserver = MockObserver(include_sleeps=True)
        drop: DropBackPressureStrategy = BackPressure.DROP(mock_observer, cache_size=3)
        messages = [
            {'id': 1, 'payload': "OK"},
            {'id': 2, 'payload': "OK"},
            {'id': 3, 'payload': "OK"},
            {'id': 4, 'payload': "OK"},
            {'id': 5, 'payload': "OK"},
            {'id': 6, 'payload': "OK"},
            {'id': 7, 'payload': "OK"},
            {'id': 8, 'payload': "OK"},
            {'id': 9, 'payload': "OK"},
            {'id': 10, 'payload': "OK"},
            {'id': 11, 'payload': "OK"},
            {'id': 12, 'payload': "OK"}
        ]

        drop.on_next(messages[0])
        drop.on_next(messages[1])
        drop.on_next(messages[2])
        drop.on_next(messages[3])
        drop.on_next(messages[4])
        drop.on_next(messages[5])

        while drop.is_locked():
            pass  # wait to become unlocked

        drop.on_next(messages[6])
        drop.on_next(messages[7])
        drop.on_next(messages[8])
        drop.on_next(messages[9])
        drop.on_next(messages[10])
        drop.on_next(messages[11])

        while drop.is_locked():
            pass  # wait to become unlocked

        mock_observer.on_next_mock.assert_has_calls([
            call(messages[0]), call(messages[3]), call(messages[4]), call(messages[5]),
            call(messages[6]), call(messages[9]), call(messages[10]), call(messages[11]),
        ])

    def test_when_on_error_called_and_wrapped_is_processing_then_drop_messages_when_cache_is_full(self):
        mock_observer: MockObserver = MockObserver(include_sleeps=True)
        drop: DropBackPressureStrategy = BackPressure.DROP(mock_observer, cache_size=3)
        messages = [
            {'id': 1, 'payload': "OK"},
            {'id': 2, 'payload': "OK"},
            {'id': 3, 'payload': "OK"},
            {'id': 4, 'payload': "OK"},
            {'id': 5, 'payload': "OK"},
            {'id': 6, 'payload': "OK"},
            {'id': 7, 'payload': "OK"},
            {'id': 8, 'payload': "OK"},
            {'id': 9, 'payload': "OK"},
            {'id': 10, 'payload': "OK"},
            {'id': 11, 'payload': "OK"},
            {'id': 12, 'payload': "OK"}
        ]

        drop.on_error(messages[0])
        drop.on_error(messages[1])
        drop.on_error(messages[2])
        drop.on_error(messages[3])
        drop.on_error(messages[4])
        drop.on_error(messages[5])

        while drop.is_locked():
            pass  # wait to become unlocked

        drop.on_error(messages[6])
        drop.on_error(messages[7])
        drop.on_error(messages[8])
        drop.on_error(messages[9])
        drop.on_error(messages[10])
        drop.on_error(messages[11])

        while drop.is_locked():
            pass  # wait to become unlocked

        mock_observer.on_error_mock.assert_has_calls([
            call(messages[0]), call(messages[3]), call(messages[4]), call(messages[5]),
            call(messages[6]), call(messages[9]), call(messages[10]), call(messages[11]),
        ])
