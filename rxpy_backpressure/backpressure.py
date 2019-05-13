from rxpy_backpressure.latest import wrap_observer_with_latest_backpressure_strategy


class BackPressure:
    """
        Convenience API to make it easy for the implementation to change without affecting consumers
    """
    LATEST = wrap_observer_with_latest_backpressure_strategy
