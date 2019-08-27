from os import path
import sys
lib_path = path.join(path.dirname(path.realpath(__file__)), '../')
print(lib_path)
sys.path.append(lib_path)

from pifetcher.core import Config
from pifetcher.core import FetchWorker

class TestWorker(FetchWorker):
    def on_save_result(self, result, work):
        print(result)
    def on_empty_result_error(self):
        self.stop()
    def on_start_process_signal(self):
        work = {}
        work['url'] = 'https://www.amazon.com/gp/product/B01HOS31B0?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=VJQJJSGTMRT23K2K6S8T'
        work['fetcher_name'] = 'amazon'
        self.add_works([work])
    
if __name__ == "__main__":
    from os import getcwd

    #print(getcwd())
    from pifetcher.core import FetcherFactory
    Config.use('pifetcherConfig.json')
    def test_do_work():
        tw = TestWorker()
        tw.do_works()
    def test_all():
        work = {}
        work['url'] = 'https://www.amazon.com/gp/product/B01HOS31B0?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=VJQJJSGTMRT23K2K6S8T'
        work['fetcher_name'] = 'amazon'
        tw = TestWorker()
        tw.add_works([work])
        tw.do_works()
    def test_fetcher():
        f = FetcherFactory.get_fetcher_by_name('amazon')
        f.load_html_by_url('https://www.amazon.com/gp/product/B01HOS31B0?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=VJQJJSGTMRT23K2K6S8T')
        obj = f.parse()
        print(obj)
    
    test_all()
