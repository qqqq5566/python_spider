import scrapy
from ..items import WebsiteItem
import copy
import time
class CoinDeskSpider(scrapy.Spider):
    name = 'coindesk'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    start_urls = ['https://www.coindesk.com/author/ssinclair/']

    def __init__(self):
        self.myDict = {}

    def parse(self, response):
        title_list = response.css('#content h3 a::text').extract()
        img_list = response.css('#content .picture img::attr("src")').extract()
        url_list = response.css('#content h3 a::attr("href")').extract()
        desc_list = response.css('#content .post-info .desc::text').extract()
        t_list = response.css('#content time::attr("datetime")').extract()
        item = WebsiteItem()
        for title, img, url, desc, t in zip(title_list, img_list, url_list, desc_list, t_list):
            item['title'] = title
            item['img_src'] = img
            item['desc'] = desc
            item['release_date'] = int(time.mktime(time.strptime(t,'%Y-%m-%dT%H:%M:%S+00:00')))
            item['author'] = 'ssinclair'
            #print(item['title'])
            yield scrapy.Request(url, callback=self.parse_content, meta={'item': copy.deepcopy(item)}, dont_filter=True)



    def parse_content(self, response):
        content = response.css('.article-content-container').extract()
        item = response.meta['item']
        item['content'] = content[0]
        yield copy.deepcopy(item)