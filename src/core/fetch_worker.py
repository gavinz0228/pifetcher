
import time
from abc import ABC, abstractmethod
from fetcher_factory import FetcherFactory
from logger import Logger
from work_queue.work_queue_factory import WorkQueueFactory
from config import Config

class FetchWorker(ABC):
    def __init__(self):
        self.work_queue = WorkQueueFactory.get_work_queue(Config.queue['queue_type'], Config.queue['queue_name'])
        self.has_stop = False

    def log(self, message):
        print(message)

    def add_works(self, urls):
        self.work_queue.add_work(urls)

    @abstractmethod
    def on_save_result(self, results):
        raise NotImplementedError()

    @abstractmethod
    def on_empty_result_error(self):
        pass

    @abstractmethod
    def on_add_work_signal(self):
        pass
    

    def perform_fetch(self):
        num_fetched = 0
        messages, handles = self.work_queue.get_work()
        if not messages:
            Logger.info("no task")
            return
        for i in range(len(messages)):
            Logger.debug(messages[i])
            #perform work
            fetcher = FetcherFactory.get_fetcher_by_name(messages[i]['fetcher_name'])
            fetcher.load_html_by_url(messages[i]['url'])
            result, parsed_data = fetcher.parse()
            Logger.debug( "parsed object" + str(parsed_data))
            if parsed_data:
                self.on_save_result(result)
                num_fetched += 1
                self.work_queue.delete_work(handles[i])  
            else:
                Logger.info("no data was parse from the page. ")
                self.on_empty_result_error()

        return num_fetched
    def stop(self):
        Logger.info("Received stop signal, stop worker.")
        self.has_stop = True

    def do_works(self):
        while True:
            time.sleep(0.5)

            if not self.has_stop:
                Logger.info("searching for work.")

                num_fetched = self.perform_fetch()
                Logger.info(str(num_fetched) + " work(s) done.")

                if not num_fetched:
                    Logger.info("no work found.")
                    




