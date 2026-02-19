from abc import ABC, abstractmethod

class BaseSensor(ABC):

    @abstractmethod
    def read(self):
        pass