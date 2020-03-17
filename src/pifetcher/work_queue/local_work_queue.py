import json
import uuid
import multiprocessing
from pifetcher.work_queue import BaseWorkQueue

class LocalWorkQueue(BaseWorkQueue):
    def __init__(self, *args, **kwargs):
        super(LocalWorkQueue, self).__init__(*args, **kwargs)
        self.work_queue = multiprocessing.Queue()

    def get_work(self):
        if self.work_queue.empty():
            return None, None
        else:
            return [self.work_queue.get()], [None]

    def add_work(self, message):
        if isinstance(message, list):
            for mes in message:
                self.work_queue.put(mes)
        else:
            self.work_queue.put(message)

    def delete_work(self, handle):
        pass
