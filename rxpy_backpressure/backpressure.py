from rxpy_backpressure.drop import wrap_observer_with_drop_strategy
from rxpy_backpressure.latest import wrap_observer_with_latest_strategy


class BackPressure:
    """
        Latest strategy will remember the next most recent message to process and will call the observer with it when
        the observer has finished processing its current message.
    """
    LATEST = wrap_observer_with_latest_strategy

    """
        Drop strategy accepts a cache size, the strategy will remember the most recent messages and remove older 
        messages from the cache. The strategy guarantees that the oldest messages in the cache are passed to the 
        observer first.
        :param cache_size: int = 10 is default
    """
    DROP = wrap_observer_with_drop_strategy
