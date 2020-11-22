# pifetcher
A scalable headless data fetching library written with python and message queue service to enable quickly and easily parsing web data in a distributive way.

## To install
```bash
pip install pifetcher
```

## PYPI Link  [https://pypi.org/project/pifetcher/](https://pypi.org/project/pifetcher/)

## dependencies:
- pyppeteer
- BeautifulSoup4
- boto3

## features:

- event-callback-based interaction between user defined logic and the pre-disigned fetch worker
- process works in batches, library user will be able to capture the event of a batch of works have been finished
- easy to use, only needs to inherit the FetchWorker class and implement the basic call back functions
- it's design to use message queue, enbles more than just one worker to perform data fetching in order to scale the application 

## how to use:


1. configure a fetcher by creating a field mapping config file, for example:
create a mapping config file for fetching amazon.com item pricing data

```javascript
{
    "price": {
        "type": "text",
        "selector": "#priceblock_ourprice",
        "attribute":".text"
    },
    "id": {
        "type": "text",
        "selector": "#ASIN",
        "attribute": "value"
    },
    "title": {
        "type": "text",
        "selector": "#productTitle",
        "attribute":".text"
    }
}
```
2. create a pifetcherConfig.json file, and add the fetcher mapping file that previously created to fetcher -> mappingConfigs with its name and file path 

numWorksPerTime : defines the number of messages it try to fetch from the queue per work cycle
pollingIntervalOnActive : time interval before fetching the next message when the worker status is active(meaning it fetched at least on message in the last worker cycle)
pollingIntervalOnIdle : time interval before fetching the next message when the worker status is active(meaning it fetched no message in the last worker cycle)

```javascript
{
  "driverType": "Pyppeteer",
  "queue": {
    "numWorksPerTime": 1,
    "queueType": "LocalWorkQueue",
    "queueName": "",
    "pollingIntervalOnActive": 0.5,
    "pollingIntervalOnIdle": 60
  },
  "logger": {
    "output": "console"
  },
  "fetcher": {
    "mappingConfigs": {
      "amazon": "amazon.json"
    }
  }
}
```
3.  to use the fetcher worker
- import the fetcher worker class and config class 
```python
from pifetcher.core import Config
from pifetcher.core import FetchWorker
```
- load the pifetherConfig.json to the Config class
```python
Config.use('pifetcherConfig.json')
```

- implement event function with your own logic
on_save_result : this will be called when a data object has been successfully parsed
on_empty_result_error: this will be called after parsing an empty object, you may want to stop/ pause the process to investigate the problem before continuing parsing
on_batch_start: this will be called when the worker received a batch start signal , you may implement your logic of adding fetching tasks to the queue here
on_batch_finish: this will be called when the worker received a batch finish signal
example:
```python
    def on_save_result(self, result, batch_id, work):
        print(result, batch_id, work)
    def on_empty_result_error(self):
        self.stop()
    def on_batch_start(self, batch_id):
        work = {}
        work['url'] = 'a amazon url'
        work['fetcherName'] = 'amazon'
        self.add_works([work])
    def on_batch_finish(self, batch_id):
        print(f"all works with the batchId {batch_id} have been processed")
```
4. Run the worker and, send a StartProcess Signal to the queue to start the process

- start the worker to receive and process works

```python
tw = TestWorker()
tw.do_works()
```

- to send a start signal to the queue
If you want to send out the start signal from one of the worker, you can call this function
```python
tw.send_start_signal()
```

# How to use a scalable message queue system like AWS Simple Queue Service

To set up work queue component on the host computer(aws simple queue service by default), such as credentials, regions
[AWS BOTO3 initial set up docs](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

If you want to start the batch process from another system, you can use the code below
```python
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='datafetch.fifo')
    content = {"type":"BatchStart","batchId": str(uuid.uuid4()),"content":{}}
    queue.send_message(MessageBody=json.dumps(content), MessageGroupId = "FetchWork", MessageDeduplicationId = str(time.time()).replace(".",""))
    
``` 

# How to optimized the number of polls the worker has to send to the queue

When no message was fetched in a worker cycle, it would enter the idle state. Under the idle state, it's supposed to wait a longer time interval before trying to fetch the next message. This sleep interval is defined in the config file at the location:
```javascript
        "pollingIntervalOnIdle": 60
```

After the worker received at least one mssage in a worker cycle, the worker status will be set as ACTIVE. Under this state, it's supposed to wait a shorter time interval before trying to fetch the next message. This sleep interval is defined in the config file at the location:
```javascript
        "pollingIntervalOnActive": 0.2,
```


### To do list items:
- simplify initial setup process

### Completed items:
- use better strategy to reduce number of requests a worker has to send
- put all constants in config the config file (checked)
- complete the type conversions for different data types (checked)
- add message type (work initiation message type) (checked)
- logging (checked)
- data fetching with use of aws sqs (checked)
- use a better scrapping library pyppeteer(checked)