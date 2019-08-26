# pifetcher
A scalable headless data fetching library written with python and message queue service to enable quickly and easily parsing web data in a distributive way.

##
To install
```
pip install pifetcher
```

## PYPI Link  [https://pypi.org/project/pifetcher/](https://pypi.org/project/pifetcher/)

## dependencies:
- selenium
- BeautifulSoup4
- boto3 (optional but by default)
- ChromeDriver for chrome 76(by default)
- Chrome executable v 76(by default)

## how to use:

1. set up work queue component on the host computer(aws simple queue service by default), such as credentials, regions
[AWS BOTO3 initial set up docs](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

2. configure a fetcher by creating a field mapping config file, for example:
create a mapping config file for fetching amazon.com item pricing data

```
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
3. create a pifetcherConfig.json file, and add the fetcher mapping file that previously created to fetcher -> mappingConfigs with its name and file path 

```{
    "browser":{
        "browser_options":["--window-size=1920,1080", "--disable-extensions", "--proxy-server='direct://'", "--proxy-bypass-list=*", "--start-maximized","--ignore-certificate-errors", "--headless"],
        "win-driver_path":"chromedriver-win-76.exe",
        "win-binary_location": "",
        "mac-driver_path":"chromedriver-mac-76",
        "mac-binary_location": ""

    },
    "queue":
    {
        "num_works_per_time": 1,
        "queue_type":"AWSSimpleQueueService",
        "queue_name":"datafetch.fifo"
    },
    "logger":
    {
        "output":"console"
    },
    "fetcher":
    {
        "mappingConfigs":{
            "amazon":"amazon.json"
        }
        
    }
}
```
4.  to use the fetcher worker
- import the fetcher worker class and config class 
```
from pifetcher.core import Config
from pifetcher.core import FetchWorker
```
- load the pifetherConfig.json to the Config class
```
Config.use('pifetcherConfig.json')
```

- implement event function with your own logic
on_save_result : this will be called when a data object has been successfully parsed
on_empty_result_error: this will be called after parsing an empty object, you may want to stop/ pause the process to investigate the problem before continuing parsing
on_start_process_signal: this will be called when the worker received a start process signaal , you may implement your logic of adding fetching tasks to the queue here

example:
```
class TestWorker(FetchWorker):
    def on_save_result(self, results):
        print(results)
    def on_empty_result_error(self):
        self.stop()
    def on_start_process_signal(self):
        work = {}
        work['url'] = 'a amazon url'
        work['fetcher_name'] = 'amazon'
        self.add_works([work])
```
5. Run the worker and, send a StartProcess Signal to the queue to start the process

- start the worker to receive and process works
```
tw = TestWorker()
tw.do_works()
```

- to send a start signal to the queue
```
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='datafetch.fifo')
    content = {"type":"StartProcess","content":{}}
    queue.send_message(MessageBody=json.dumps(content), MessageGroupId = "FetchWork", MessageDeduplicationId = str(time.time()))
    
``` 

Command to exit all chromedriver in windows
```
taskkill /f /im chromedriver-win-76.exe
```

### To do list items:
- use better strategy to reduce number of requests a worker has to send
- simplify initial setup process

### Completed items

- put all constants in config the config file (checked)
- complete the type conversions for different data types (checked)
- add message type (work initiation message type) (checked)
- logging (checked)
- data fetching with use of aws sqs