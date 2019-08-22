from abc import ABC, abstractmethod
class BaseWorkQueue(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def get_work(self):
        raise NotADirectoryError()
    @abstractmethod
    def add_work(self, message):
        raise NotADirectoryError()
    @abstractmethod
    def delete_work(self, id):
        raise NotADirectoryError()