import json
import boto3
import time
import uuid


def start_process(event, context):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='datafetch.fifo')
    content = {
        "type": "BatchStart",
        "batchId": str(uuid.uuid4()),
        "content": {}}
    queue.send_message(
        MessageBody=json.dumps(content),
        MessageGroupId="FetchWork",
        MessageDeduplicationId=str(time.time()).replace(".", ""))

    return {
        "statusCode": 200,
        "body": {}
    }
