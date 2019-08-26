import time
from os import path
from abc import ABC, abstractmethod
from pifetcher.core import Logger, Config
from pifetcher.work_queue import WorkQueueFactory
from pifetcher.data_fetchers import FetcherFactory
class FetchWorker(ABC):
    def __init__(self):
        self.check_config_init()
        self.work_queue = WorkQueueFactory.get_work_queue(Config.queue['queue_type'], Config.queue['queue_name'])
        self.has_stop = False

    def check_config_init(self):
        if not Config.initialized:
            raise ValueError("please call pifetcher.core.Config.use to use a config file before using the worker.")

    def log(self, message):
        print(message)

    def add_works(self, works):
        messages = [ {"type":"FetchWork", "content": w} for w in works]
        self.work_queue.add_work(messages)

    @abstractmethod
    def on_save_result(self, result, work):
        raise NotImplementedError()

    @abstractmethod
    def on_empty_result_error(self):
        pass

    @abstractmethod
    def on_start_process_signal(self):
        pass
    
    def perform_fetch(self, work):
        fetcher = FetcherFactory.get_fetcher_by_name(work['fetcher_name'])
        fetcher.load_html_by_url(work['url'])
        result, parsed_data = fetcher.parse()
        Logger.debug( "parsed object" + str(parsed_data))
        if parsed_data:
            self.on_save_result(result, work)
            return True
        else:
            return False

    def process_message(self, message, handle):
        #perform work
        if message['type'] == 'FetchWork':
            success = self.perform_fetch(message['content'])
            if not success:
                Logger.info("no data was parse from the page. ")
                self.on_empty_result_error()
            else:
                self.work_queue.delete_work(handle)
        elif message['type'] == 'StartProcess':
            self.on_start_process_signal()
            self.work_queue.delete_work(handle)
        elif message['type'] == 'ResumeProcess':
            self.has_stop = False
            self.work_queue.delete_work(handle)  
        else:
            Logger.warning('message type not recognized')


    def get_messages(self):
        return  self.work_queue.get_work()

    def stop(self):
        Logger.info("Received stop signal, stop worker.")
        self.has_stop = True

    def do_works(self):
        while True:
            time.sleep(0.5)
            if not self.has_stop:
                Logger.info("searching for work.")
                messages, handles = self.get_messages()
                if not messages:
                    Logger.info("no work found.")
                    continue

                for i in range(len(messages)):
                    Logger.debug(messages[i])
                    Logger.debug(handles[i])
                    self.process_message(messages[i], handles[i])

                    




