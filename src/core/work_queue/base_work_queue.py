from abc import ABC, abstractmethod
from config import Config
class BaseWorkQueue(ABC):
    def __init__(self, queue_name):
        self.num_work_per_time = Config.queue["num_works_per_time"]
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