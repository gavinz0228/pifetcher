
import time
from abc import ABC, abstractmethod
from work_queue.sqs_work_queue import SqsWorkQueue
from fetcher_factory import FetcherFactory

class FetchWorker(ABC):
    def __init__(self):
        self.work_queue = SqsWorkQueue()
        self.has_stop = False

    def log(self, message):
        print(message)

    def add_works(self, urls):
        self.work_queue.add_work(urls)

    @abstractmethod
    def save_result(self, results):
        raise NotImplementedError()

    @abstractmethod
    def on_empty_result_error(self):
        pass

    def perform_fetch(self):
        num_fetched = 0
        messages, handles = self.work_queue.get_work()
        if not messages:
            self.log("no task")
            return
        for i in range(len(messages)):
            self.log(messages[i])
            #perform work
            fetcher = FetcherFactory.get_fetcher_by_name(messages[i]['fetcher_name'])
            fetcher.load_html_by_url(messages[i]['url'])
            result, parsed_data = fetcher.parse()
            print(result, parsed_data)
            if parsed_data:
                self.save_result(result)
                num_fetched += 1
                self.work_queue.delete_work(handles[i])  
            else:
                self.log("no data was parse from the page. ")
                self.on_empty_result_error()

        return num_fetched
    def stop(self):
        self.log("Received stop signal, stop worker.")
        self.has_stop = True

    def do_works(self):
        while True:
            time.sleep(0.5)
            self.log("searching for work")
            num_fetched = self.perform_fetch()
            self.log(str(num_fetched) + " work(s) done.")
            if self.has_stop:
                break



