import scrapy
from ..items import WebsiteItem
import copy
import time
class EthnewsSpider(scrapy.Spider):
    name = 'ethnews'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    start_urls = ['https://www.ethnews.com/author/frederick-reese?page=1']


    def parse(self, response):
        title_list = response.css('.article-thumbnail__info__title a::text').extract()
        img_list = response.css('.article-thumbnail__cover img::attr("data-src")').extract()
        url_list = response.css('.article-thumbnail__info__title a::attr("href")').extract()
        desc_list = response.css('.article-thumbnail__info__summary::text').extract()
        t_list = response.css('.article-thumbnail__info__etc__date h6::attr("data-created-short")').extract()
        item = WebsiteItem()
        for title, img, url, desc, t in zip(title_list, img_list, url_list, desc_list, t_list):
            #print(title, img, url, desc, t)
            item['title'] = title
            item['img_src'] = img
            item['desc'] = desc
            item['release_date'] = int(time.mktime(time.strptime(t[0:-5], '%Y-%m-%dT%H:%M:%S')))
            item['author'] = 'frederick-reese'

            yield scrapy.Request('https://www.ethnews.com'+url, callback=self.parse_content, meta={'item': copy.deepcopy(item)}, dont_filter=True)

        next_page = response.css('.pagination__list__item--next::attr("href")').extract()

        if next_page:
            #print(222222222222222)
            yield scrapy.Request('https://www.ethnews.com'+next_page[0], callback=self.parse)


    def parse_content(self, response):
        content = response.css('.article__content').extract()
        item = response.meta['item']
        item['content'] = content[0]
        yield copy.deepcopy(item)