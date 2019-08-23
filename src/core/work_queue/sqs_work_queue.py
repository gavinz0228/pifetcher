from .base_work_queue import BaseWorkQueue
import time
import boto3

class SqsWorkQueue(BaseWorkQueue):
    def __init__(self):
        sqs = boto3.resource('sqs')
        self.work_queue = sqs.get_queue_by_name(QueueName='datafetch.fifo')

    def get_work(self):
        response = self.work_queue.receive_messages(MaxNumberOfMessages = 1, MessageAttributeNames=['All'])
        if not response:
            return [], [None]
        messages = [ m.body for m in response]
        handles = [m for m in response]
        return messages, handles

    def add_work(self, message):
        
        entries = [ { 'MessageBody': m, 'Id': str(i), 'MessageDeduplicationId': str(time.time()).replace(".",""), "MessageGroupId" : "FetchWork" } for i, m in enumerate(message)]
        response = self.work_queue.send_messages(Entries = entries)
        print(response)

    def delete_work(self, handle):
        handle.delete()