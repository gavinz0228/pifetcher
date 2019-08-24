from work_queue.sqs_work_queue import SqsWorkQueue

queue_types = ['AWSSimpleQueueService']
queue_implementations = [SqsWorkQueue]

class WorkQueueFactory:
    @staticmethod
    def get_work_queue(queue_type, queue_name):
        qidx = queue_types.index(queue_type)
        queue = queue_implementations[qidx]
        print(queue)
        return queue(queue_name = queue_name)