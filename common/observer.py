from abc import ABC, abstractmethod


class Observable(ABC):
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify(self, value):
        for o in self.__observers:
            o.update(value)


class Observer(ABC):
    @abstractmethod
    def update(self, value):
        pass
