from pifetcher.core import Logger
from pifetcher.work_queue import SqsWorkQueue, LocalWorkQueue

queue_lookup = {}
queue_lookup['AWSSimpleQueueService'] = SqsWorkQueue
queue_lookup['LocalWorkQueue'] = LocalWorkQueue

class WorkQueueFactory:
    @staticmethod
    def get_work_queue(queue_type, queue_name):
        queue = queue_lookup[queue_type]
        return queue(queue_name=queue_name)
