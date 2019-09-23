from abc import ABC, abstractmethod

from pifetcher.core import Config


class BaseWorkQueue(ABC):
    def __init__(self, queue_name):
        self.num_work_per_time = Config.queue["numWorksPerTime"]
        pass

    @abstractmethod
    def get_work(self):
        raise NotImplementedError()

    @abstractmethod
    def add_work(self, message):
        raise NotImplementedError()

    @abstractmethod
    def delete_work(self, id):
        raise NotImplementedError()
