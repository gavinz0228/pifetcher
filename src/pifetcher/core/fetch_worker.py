import time
import uuid
from os import path
from abc import ABC, abstractmethod
from pifetcher.core import Logger, Config
from pifetcher.work_queue import WorkQueueFactory
from pifetcher.data_fetchers import FetcherFactory
class FetchWorker(ABC):
    ACTIVE_STATUS = 'ACTIVE'
    IDLE_STATUS = 'IDLE'
    def __init__(self):
        self.check_config_init()
        self.work_queue = WorkQueueFactory.get_work_queue(Config.queue['queue_type'], Config.queue['queue_name'])
        self.has_stop = False
        self.polling_interval_on_active = Config.queue["polling_interval_on_active"]
        self.polling_interval_on_idle = Config.queue["polling_interval_on_idle"]
        self.worker_status = FetchWorker.ACTIVE_STATUS

    def check_config_init(self):
        if not Config.initialized:
            raise ValueError("please call pifetcher.core.Config.use to use a config file before using the worker.")

    def log(self, message):
        print(message)

    def add_works(self, works):
        messages = [ {"type":"FetchWork", "content": w} for w in works]
        self.work_queue.add_work(messages)

    def send_start_signal(self):
        batch_id = str(uuid.uuid4())
        content = {"type":"BatchStart", "batchId": batch_id,"content":{}}
        self.work_queue.add_work([content])
        return batch_id

    def send_finish_signal(self, batch_id):
        content = {"type":"BatchFinish", "batchId": batch_id,"content":{}}
        self.work_queue.add_work([content])

    @abstractmethod
    def on_save_result(self, result, work):
        raise NotImplementedError()

    @abstractmethod
    def on_empty_result_error(self):
        pass
    
    @abstractmethod
    def on_batch_finish(self, batchId):
        pass

    @abstractmethod
    def on_batch_start(self, batch_id):
        pass

    def perform_fetch(self, work):

        fetcher = FetcherFactory.get_fetcher_by_name(work['fetcher_name'])
        fetcher.load_html_by_url(work['url'])
        result, success = fetcher.parse()

        Logger.debug( "parsed object" + str(success))
        if success:
            self.on_save_result(result, work)
            return True
        else:
            Logger.info("no data was parse from the page. ")
            self.on_empty_result_error()
            return False

    def process_message(self, message, handle):
        Logger.debug(message)
        #perform work
        if message['type'] == 'FetchWork':
            success = self.perform_fetch(message['content'])
            if success:
                self.work_queue.delete_work(handle)

        elif message['type'] == 'BatchStart':
            self.on_batch_start(message["batchId"])
            #at this point, all the works for this batch should have been added to the queue
            #now, append a batch finish signal to the queue
            self.send_finish_signal(message["batchId"])
            self.work_queue.delete_work(handle)

        elif message['type'] == 'BatchFinish':
            self.on_batch_finish(message["batchId"])
            self.work_queue.delete_work(handle)

        elif message['type'] == 'ResumeProcess':
            self.has_stop = False
            self.work_queue.delete_work(handle)  
        else:
            Logger.warning('message type not recognized')  


    def get_messages(self):
        return self.work_queue.get_work()

    def stop(self):
        Logger.info("Received stop signal, stop worker.")
        self.has_stop = True

    def do_works(self):
        while True:
            if self.worker_status == FetchWorker.IDLE_STATUS:
                time.sleep(self.polling_interval_on_idle)
            elif self.worker_status == FetchWorker.ACTIVE_STATUS:
                time.sleep(self.polling_interval_on_active)
            else:
                time.sleep(self.polling_interval_on_idle)

            if not self.has_stop:
                Logger.info("searching for work.")
                messages, handles = self.get_messages()
                if not messages:
                    Logger.info("no work found, entering idle mode")
                    self.worker_status = FetchWorker.IDLE_STATUS
                    continue
                    
                self.worker_status = FetchWorker.ACTIVE_STATUS
                for i in range(len(messages)):
                    Logger.debug(messages[i])
                    Logger.debug(handles[i])
                    self.process_message(messages[i], handles[i])

                    




