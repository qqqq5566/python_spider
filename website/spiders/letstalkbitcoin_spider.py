import scrapy
from ..items import WebsiteItem
import copy
import time
class LetstalkbitcoinSpider(scrapy.Spider):
    name = 'letstalkbitcoin'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    start_urls = ['https://letstalkbitcoin.com/profile/user/fergish?t=blog&page=1#activity']


    def parse(self, response):
        title_list = response.css('#blog-activity .blog-list .post-title a::text').extract()
        img_list = response.css('#blog-activity .blog-list .blog-image img::attr("src")').extract()
        url_list = response.css('#blog-activity .blog-list .post-title a::attr("href")').extract()
        desc_list = response.css('#blog-activity .blog-list .blog-excerpt>p::text').extract()
        t_list = response.css('#blog-activity .blog-list .blog-date::text').extract()
        item = WebsiteItem()
        #print(url_list)
        for title, img, url, desc, t in zip(title_list, img_list, url_list, desc_list, t_list):
            #print(title, img, url, desc, t[1:-1])
            item['title'] = title
            item['img_src'] = img
            item['desc'] = desc
            item['release_date'] = int(time.time())
            item['author'] = 'fergish'

            yield scrapy.Request(url, callback=self.parse_content, meta={'item': copy.deepcopy(item)}, dont_filter=True)

        next_page = response.css('#blog-activity .paging a::text').extract()
        next_url = response.css('#blog-activity .paging a::attr("href")').extract()
        current_url = response.url
        cur_str = str.split(current_url, '?')
        cur_page = response.css('#blog-activity .paging a.current::text').extract()[0]
        total_page = len(next_page)
        if int(cur_page) < int(total_page):
            index = int(cur_page)
            yield scrapy.Request(cur_str[0]+next_url[index], callback=self.parse)


    def parse_content(self, response):
        content = response.css('.blog-content').extract()
        #print(content)
        item = response.meta['item']
        item['content'] = content[0]
        yield copy.deepcopy(item)