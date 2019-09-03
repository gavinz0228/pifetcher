
from os import path, chdir, getcwd, pardir
import sys
cur_path = path.dirname(path.abspath(__file__))
lib_path = path.abspath(path.join(cur_path, pardir))
chdir(lib_path)
sys.path.append(lib_path)
print(cur_path, lib_path, getcwd())


from pifetcher.core import Config
from pifetcher.core import FetcherFactory

def test_fetch ():
    Config.use('pifetcherConfig.json')
    f = FetcherFactory.get_fetcher_by_name('amazon')
    f.load_html_by_url('https://www.amazon.com/gp/product/B01HOS31B0?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=VJQJJSGTMRT23K2K6S8T')
    obj, success = f.parse()
    f.close()
    assert obj["price"] is not None