from fetch_worker import FetchWorker

class TestWorker(FetchWorker):
    def save_result(self, results):
        print(results)
    def on_empty_result_error(self):
        self.stop()
        #self.resume()
    
if __name__ == "__main__":
    url = 'https://www.amazon.com/gp/product/B01HOS31B0?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=VJQJJSGTMRT23K2K6S8T'
    tw = TestWorker()
    tw.add_works([url])
    tw.do_works()