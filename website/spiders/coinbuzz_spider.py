import scrapy
from ..items import WebsiteItem
import copy
import time
class CoinbuzzSpider(scrapy.Spider):
    name = 'coinbuzz'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    start_urls = ['http://www.coinbuzz.com/author/alexander-cordova/page/1/']


    def __init__(self):
        self.total_page = 1
        self.page = 1

    def parse(self, response):
        title_list = response.css('#content .post-one-column .post-title a::text').extract()
        img_list = response.css('#content .post-one-column figure img::attr("src")').extract()
        url_list = response.css('#content .post-one-column .post-title a::attr("href")').extract()
        desc_list = response.css('#content .post-one-column .post-excerpt>p::text').extract()
        t_list = response.css('#content .post-one-column time::attr("datetime")').extract()
        item = WebsiteItem()
        for title, img, url, desc, t in zip(title_list, img_list, url_list, desc_list, t_list):
            print(title, img, url, desc, t)
            item['title'] = title
            item['img_src'] = img
            item['desc'] = desc
            item['release_date'] = int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
            item['author'] = 'alexander-cordova'

            yield scrapy.Request(url, callback=self.parse_content, meta={'item': copy.deepcopy(item)}, dont_filter=True)

        next_page = response.css('#pagination .page_item::text').extract()
        # next_url = response.css('#blog-activity .paging a::attr("href")').extract()
        # current_url = response.url
        cur_page = response.css('#pagination > span.page-item.current::text').extract()[0]
        if self.page == 1:
            t_page = response.css('#pagination > a:last-child::attr("data-page")').extract()
            if t_page:
                self.total_page = t_page[0]
            else:
                self.total_page = len(next_page)
            self.page += 1
        next_url = "http://www.coinbuzz.com/author/alexander-cordova/page/"
        if int(cur_page) < int(self.total_page):
            index = int(cur_page) + 1
            yield scrapy.Request(next_url + str(index) + '/', callback=self.parse)


    def parse_content(self, response):
        content = response.css('.article-content').extract()
        #print(content)
        item = response.meta['item']
        item['content'] = content[0]
        yield copy.deepcopy(item)