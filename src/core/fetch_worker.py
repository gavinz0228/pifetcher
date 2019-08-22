
import time
from sqs_work_queue import SqsWorkQueue

class FetchWorker:
    def __init__(self):
        self.work_queue = SqsWorkQueue()
    def log(self, message):
        print(message)

    def perform_fetch(self):
        response = self.work_queue.get_work()
        if not response:
            self.log("no task")
            return
        #print(response)
    
    def do_work(self):
        while True:
            time.sleep(1)
            self.log("searching for work")
            #self.work_queue.add_work('https://www.amazon.com/gp/product/B07V58CQGR?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=SDYZZDBFHKPPPKG36000&th=1')
            self.perform_fetch()

    
FetchWorker().do_work()