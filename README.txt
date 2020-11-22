# pifetcher
A scalable headless data fetching library written with python and message queue service to enable quickly and easily parsing web data in a distributive way.

## To install
```bash
pip install pifetcher
```

## PYPI Link  [https://pypi.org/project/pifetcher/]

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

Github: [https://github.com/gavinz0228/pifetcher]