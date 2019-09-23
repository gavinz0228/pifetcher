import time
import uuid
from abc import ABC, abstractmethod

from pifetcher.core import Logger, Config
from pifetcher.data_fetchers import FetcherFactory
from pifetcher.work_queue import WorkQueueFactory


class FetchWorker(ABC):
    ACTIVE_STATUS = 'ACTIVE'
    IDLE_STATUS = 'IDLE'

    def init(self, config_path):
        Config.use(config_path)
        self.check_config_init()
        self.work_queue = WorkQueueFactory.get_work_queue(Config.queue['queueType'], Config.queue['queueName'])
        self.has_stop = False
        self.polling_interval_on_active = Config.queue["pollingIntervalOnActive"]
        self.polling_interval_on_idle = Config.queue["pollingIntervalOnIdle"]
        self.worker_status = FetchWorker.ACTIVE_STATUS
        self.current_batch_id = None

    def check_config_init(self):
        if not Config.initialized:
            raise ValueError("please call pifetcher.core.Config.use to use a config file before using the worker.")

    def add_works(self, works):
        messages = [{"type": "FetchWork", 'batchId': self.current_batch_id, "content": w} for w in works]
        self.work_queue.add_work(messages)

    def send_start_signal(self):
        batch_id = str(uuid.uuid4())
        content = {"type": "BatchStart", 'batchId': batch_id, "content": {}}
        self.work_queue.add_work([content])
        return batch_id

    def send_finish_signal(self, batch_id):
        content = {"type": "BatchFinish", 'batchId': batch_id, "content": {}}
        self.work_queue.add_work([content])

    @abstractmethod
    def on_save_result(self, result, batch_id, work):
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

    def perform_fetch(self, work, batch_id):

        fetcher = FetcherFactory.get_fetcher_by_name(work['fetcherName'])
        fetcher.load_html_by_url(work['url'])
        result, success = fetcher.parse()

        Logger.info(f'parsed object {str(result)} , batchId {batch_id}')
        if success:
            self.on_save_result(result, batch_id, work)
            return True
        else:
            Logger.info("no data was parse from the page. ")
            self.on_empty_result_error()
            return False

    def process_message(self, message, handle):
        Logger.debug(message)
        # perform work
        if message['type'] == 'FetchWork':
            success = self.perform_fetch(message['content'], message['batchId'])
            if success:
                self.work_queue.delete_work(handle)

        elif message['type'] == 'BatchStart':
            self.current_batch_id = message['batchId']
            self.on_batch_start(message['batchId'])
            Logger.info(f'received BatchStart signal, batchId {message["batchId"]}')
            # at this point, all the works for this batch should have been added to the queue
            # now, append a batch finish signal to the queue
            self.send_finish_signal(message['batchId'])
            self.work_queue.delete_work(handle)

        elif message['type'] == 'BatchFinish':
            self.on_batch_finish(message['batchId'])
            self.work_queue.delete_work(handle)

        elif message['type'] == 'ResumeProcess':
            self.has_stop = False
            self.work_queue.delete_work(handle)
        else:
            Logger.warning(f'message type {message["type"]} not recognized')

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
