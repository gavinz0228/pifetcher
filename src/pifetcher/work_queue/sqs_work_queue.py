from pifetcher.work_queue import BaseWorkQueue
from pifetcher.core import Logger
import time
import boto3
import json

class SqsWorkQueue(BaseWorkQueue):
    def __init__(self, *args, **kwargs):
        super(SqsWorkQueue, self). __init__(*args, **kwargs)
        sqs = boto3.resource('sqs')
        self.work_queue = sqs.get_queue_by_name(QueueName=kwargs["queue_name"])

    def get_work(self):
        response = self.work_queue.receive_messages(MaxNumberOfMessages = self.num_work_per_time, MessageAttributeNames=['All'])
        if not response:
            return [], [None]
            
        messages = [ json.loads(m.body) for m in response]
        handles = [m for m in response]
        return messages, handles

    def add_work(self, message):
        
        entries = [ { 'MessageBody': json.dumps(m), 'Id': str(i), 'MessageDeduplicationId': str(time.time()).replace(".",""), "MessageGroupId" : "FetchWork" } for i, m in enumerate(message)]
        response = self.work_queue.send_messages(Entries = entries)
        Logger.debug(response)

    def delete_work(self, handle):
        handle.delete()