from pifetcher.core import FetcherFactory
from os import path, chdir
import sys
lib_path = path.join(path.dirname(path.realpath(__file__)), '../')
cur_path = path.dirname(path.abspath(__file__))
sys.path.append(lib_path)
chdir(cur_path)
from pifetcher.core import Config

def test_fetch ():
    Config.use('pifetcherConfig.json')
    f = FetcherFactory.get_fetcher_by_name('amazon')
    f.load_html_by_url('https://www.amazon.com/gp/product/B01HOS31B0?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=VJQJJSGTMRT23K2K6S8T')
    obj, success = f.parse()
    f.close()
    assert obj["price"] is not None