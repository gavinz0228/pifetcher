import json
import boto3
import time
def start_process(event, context):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='datafetch.fifo')
    content = {"type":"StartProcess","content":{}}
    queue.send_message(MessageBody=json.dumps(content), MessageGroupId = "FetchWork", MessageDeduplicationId = str(time.time()).replace(".",""))
    
    return {
        "statusCode": 200,
        "body": {}
    }
