# rxpy-backpressure
Back pressure strategies for use with RxPy

## Goals
This projects goal is to provide a simple api that allows the addition of backpressure strategys with RxPy. 

## Project Roadmap
- [X] Support Latest strategy
- [ ] Develop a small application to show the use of the library
- [ ] Support Drop strategy
- [ ] Support Buffer strategy
- [ ] Support Error Strategy

## Getting Started
To get started pull the code from pypi with a ```pip install rxpy_backpressure``` the project can be found [here](https://pypi.org/project/rxpy-backpressure/)

### Initial API Example

A example of usage of the API

```
from rxpy_backpressure import BackPressure

image_observable
    .observe_on(scheduler)
    .subscribe(BackPressure.LATEST(observer))
```

## Considerations
This project supports python 3.6+ as as [rxpy](https://github.com/ReactiveX/RxPY)
3.0.0+ is support this is not support ealier versions. If there is a 
case to support previous versions this will be considered however the 
typing introduced in python 3.6 is very nice to produce a self documenting API. 
