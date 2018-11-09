import scrapy
from ..items import WebsiteItem
import copy
import time
class BitcoinmagazineSpider(scrapy.Spider):
    name = 'bitcoinmagazine'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    start_urls = ['https://bitcoinmagazine.com/authors/jimmy-aki/']

    def __init__(self):
        self.myDict = {}

    def parse(self, response):
        title_list = response.css('.search-result--card .search-result--title::text').extract()
        img_list = response.css('.search-result--card .search-result-card--image::attr("style")').extract()
        url_list = response.css('.search-result--card .col-lg-8>a::attr("href")').extract()
        desc_list = response.css('.search-result--card  .search-result--content-wrapper::text').extract()
        t_list = response.css('.search-result--card .search-result--date::text').extract()
        item = WebsiteItem()
        for title, img, url, desc, t in zip(title_list, img_list, url_list, desc_list, t_list):
            #print(title, img, url, desc, t)
            item['title'] = title
            item['img_src'] = img[22:-2]
            item['desc'] = desc
            #item['release_date'] = int(time.mktime(time.strptime(t,'%Y-%m-%dT%H:%M:%S+00:00')))
            item['author'] = 'jimmy-aki'

            yield scrapy.Request('https://bitcoinmagazine.com'+url, callback=self.parse_content, meta={'item': copy.deepcopy(item)}, dont_filter=True)



    def parse_content(self, response):
        content = response.css('.rich-text').extract()
        t = response.css('time::attr("datetime")').extract()
        item = response.meta['item']
        item['content'] = content[0]
        item['release_date'] = t[0]
        yield copy.deepcopy(item)