# rxpy-backpressure
Back pressure strategies for use with RxPy

## Goals
This projects goal is to provide a simple api that allows the addition of backpressure strategies with RxPy. 

## Project Roadmap
- [X] Support Latest strategy
- [X] Develop a small application to show the use of the library
- [ ] Support Drop strategy
- [ ] Support Buffer strategy
- [ ] Support Error Strategy

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

## Considerations
This project supports python 3.6+ as as [rxpy](https://github.com/ReactiveX/RxPY)
3.0.0+ is support this is not support ealier versions. If there is a 
case to support previous versions this will be considered however the 
typing introduced in python 3.6 is very nice to produce a self documenting API. 
