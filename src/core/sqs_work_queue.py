from base_work_queue import BaseWorkQueue
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
        print(response[0].receipt_handle)

        ids = [ m.reciept_handle for m in response]
        
        #ids = [ m.reciept_handle for m in messages]
        return messages, ids

    def add_work(self, message):
        response = self.work_queue.send_message(MessageBody=message, MessageGroupId = "fetch", MessageDeduplicationId = str(time.time()))
        print(response)

    def delete_work(self, id):
        self.work_queue.delete_message(ReceiptHandle = id)