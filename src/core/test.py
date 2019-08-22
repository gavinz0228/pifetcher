from price_fetchers.amazon_price_tracker import AmazonPriceTracker

if __name__ == "__main__":
    url = 'https://www.amazon.com/gp/product/B01HOS31B0?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=VJQJJSGTMRT23K2K6S8T'
    pt = AmazonPriceTracker()
    pt.get(url)
    p = pt.get_price()
    print(p)