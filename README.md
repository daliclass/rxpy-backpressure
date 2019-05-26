# rxpy-backpressure
Back pressure strategies for use with RxPy

## Goals
This projects goal is to provide a simple api that allows the addition of backpressure strategies with RxPy. 

## Getting Started
To get started pull the code from pypi with a ```pip install rxpy_backpressure``` the project can be found [here](https://pypi.org/project/rxpy-backpressure/)

### API Examples

Example of usage of the API with rxpy 1.6

```
from rxpy_backpressure import BackPressure

image_observable
    .observe_on(scheduler)
    .subscribe(BackPressure.LATEST(observer))
```

Example of usage of the API with rxpy ~3

```
from rxpy_backpressure import BackPressure

image_observable
    .subscribe(BackPressure.LATEST(observer), scheduler)

```

If you would like to quickly get started with the library a runnable
example can be found here [rxpy-backpressure-example](https://github.com/daliclass/rxpy-backpressure-example)

### Strategies

#### Latest
Latest strategy will remember the next most recent message to process 
and will call the observer with it when the observer has finished 
processing its current message.

#### Drop
Drop strategy accepts a cache_size, the strategy will remember the most 
recent messages and remove older messages from the cache. The strategy 
guarantees that the oldest messages in the cache are passed to the 
observer first.

#### Buffer
Buffer strategy has a unbounded cache and will pass all messages to its 
consumer in the order it received them beware of Memory leaks due to a 
build up of messages. 

## Considerations
This project supports python 3.6+ as [rxpy](https://github.com/ReactiveX/RxPY)
3.0.0+ does not support earlier versions. If there is a case to support 
previous versions this can be discussed however the typing introduced in 
python 3.6 is very nice. 
