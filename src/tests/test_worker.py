from os import path
import sys
lib_path = path.join(path.dirname(path.realpath(__file__)), '../')
sys.path.append(lib_path)
from pifetcher.core import Config
from pifetcher.core import FetchWorker


class TestWorker(FetchWorker):

    def on_save_result(self, result, batch_id, work):
        print(result, batch_id, work)

    def on_empty_result_error(self):
        self.stop()

    def on_batch_start(self, batch_id):
        work1 = {}
        work1['url'] = 'https://www.amazon.com/gp/product/B01HOS31B0?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=VJQJJSGTMRT23K2K6S8T'
        work1['fetcherName'] = 'amazon'
        work2 = {}
        work2['url'] = 'https://www.amazon.com/dp/B07FJWLLDB'
        work2['fetcherName'] = 'amazon'
        self.add_works([work1, work2])

    def on_batch_finish(self, batch_id):
        print(f"all works with the batchId {batch_id} have been processed")

if __name__ == "__main__":


    from pifetcher.core import FetcherFactory
    Config.use('pifetcherConfig.json')

    def test_do_work():
        tw = TestWorker()
        tw.do_works()

    def test_all():
        tw = TestWorker()
        tw.send_start_signal()
        tw.do_works()

    def test_fetcher():
        f = FetcherFactory.get_fetcher_by_name('amazon')
        f.load_html_by_url('https://www.amazon.com/gp/product/B01HOS31B0?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=VJQJJSGTMRT23K2K6S8T')
        obj = f.parse()
        print(obj)

    test_all()
