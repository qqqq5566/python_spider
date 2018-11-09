# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebsiteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    img_src = scrapy.Field()
    release_date = scrapy.Field()  #时间
    content = scrapy.Field()
    author = scrapy.Field()


class FlashItem(scrapy.Item):
    release_date = scrapy.Field()  # 时间
    content = scrapy.Field()
    website = scrapy.Field()