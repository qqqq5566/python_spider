import scrapy
from ..items import WebsiteItem
import copy
import time
class BitcoinsSpider(scrapy.Spider):
    name = '99bitcoins'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    start_urls = ['https://99bitcoins.com/author/ofirnhm-co-il/page/1/']

    def __init__(self):
        self.total_page = 1
        self.page = 1

    def parse(self, response):
        title_list = response.css('.row.b-row.listing.meta-above.grid-2 .post-title a::text').extract()
        img_list = response.css('.row.b-row.listing.meta-above.grid-2 img::attr("src")').extract()
        url_list = response.css('.row.b-row.listing.meta-above.grid-2 .post-title a::attr("href")').extract()
        desc_list = response.css('.row.b-row.listing.meta-above.grid-2 .excerpt p::text').extract()
        #t_list = response.css('.article-thumbnail__info__etc__date h6::attr("data-created-short")').extract()
        item = WebsiteItem()

        for title, img, url, desc, in zip(title_list, img_list, url_list, desc_list):
            print(title, img, url, desc)
            item['title'] = title
            item['img_src'] = img
            item['desc'] = desc
            #item['release_date'] = int(time.mktime(time.strptime(t[0:-5], '%Y-%m-%dT%H:%M:%S')))
            item['author'] = 'frederick-reese'

            yield scrapy.Request(url, callback=self.parse_content, meta={'item': copy.deepcopy(item)}, dont_filter=True)

        if self.page == 1:
            next_page = response.css('.main-pagination a.page-numbers::text').extract()
            #next_url = response.css('.main-pagination a.page-numbers::attr("href")').extract()
            self.total_page = next_page[-1]
            self.page += 1

        # current_url = response.url
        # cur_str = str.split(current_url, '?')
        cur_page = response.css('.main-pagination .current::text').extract()[0]
        # total_page = len(next_page)
        if int(cur_page) < int(self.total_page):
            index = int(cur_page)+1
            #print(index)
            yield scrapy.Request('https://99bitcoins.com/author/ofirnhm-co-il/page/{}/'.format(index), callback=self.parse)


    def parse_content(self, response):
        content = response.css('.post-content').extract()
        item = response.meta['item']
        item['content'] = content[0]
        t = response.css('time::attr("datetime")').extract()
        item['release_date'] = int(time.mktime(time.strptime(t[0], '%Y-%m-%dT%H:%M:%S+00:00')))
        yield copy.deepcopy(item)