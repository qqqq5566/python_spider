import scrapy
from ..items import FlashItem
import time
from datetime import datetime
from json import loads
import pymysql
class LianmishuSqider(scrapy.Spider):
    name = "lianmishu"

    start_urls = ['http://lianmishu.com/']
    #指定管道
    custom_settings = {
        'ITEM_PIPELINES': {
            'website.pipelines.FlashPipeline': 2,
        }
    }
    def __init__(self,name=None, **kwargs):
        super(LianmishuSqider, self).__init__(name, **kwargs)
        self.select_mysql()

    def select_mysql(self):
        #获取拉取的最大值
        #避免链接数据库报错
        try:
            obj = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='new_im', cursorclass=pymysql.cursors.DictCursor)
            cursor = obj.cursor()
            sql = """select * from news_flash where website='http://lianmishu.com/' order by add_time DESC """
            cursor.execute(sql)
            result = cursor.fetchone()
            obj.close()
            if result:
                self.low_time = result['add_time']
                timeArray = time.localtime(self.low_time)
                self.end_ime = time.strftime("%Y%m%d%H%M%S", timeArray)
            else:
                self.end_ime = 0
                self.year = datetime.now().year
                self.month = datetime.now().month
                self.day = datetime.now().day
                t = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
                self.low_time = int(time.mktime(time.strptime(t, '%Y-%m-%d')))
        except:
            self.end_ime = 0
            self.year = datetime.now().year
            self.month = datetime.now().month
            self.day = datetime.now().day
            t = str(self.year) + '-' + str(self.month) + '-' + str(self.day)
            self.low_time = int(time.mktime(time.strptime(t, '%Y-%m-%d')))

    def parse(self, response):
        time_list = response.css('#flashpMain ul li::attr("data-time")').extract()  #时间
        content_list = response.css('#flashpMain ul li .text::text').extract() #内容
        title_list = response.css('#flashpMain ul li .title::text').extract()
        item = FlashItem()
        for t, title, content in zip(time_list, title_list, content_list):
            item['release_date'] = int(time.mktime(time.strptime(t, '%Y%m%d%H%M%S')))
            self.end_ime = t
            if self.low_time > item['release_date']:  #如果lowe_time大于发布时间，停止爬虫
                break
            item['content'] = title+content
            item['website'] = "http://lianmishu.com/"
            yield item
        release_date = int(time.mktime(time.strptime(self.end_ime, '%Y%m%d%H%M%S')))

        # 如果lowe_time大于发布时间，继续下一页
        if self.low_time < release_date:
            next_url = 'http://lianmishu.com/wapi/kuaixun/list/?&type=down&pagesize=15&sourceid=-1&time='+self.end_ime
            yield scrapy.Request(next_url, callback=self.parse_json, method='GET', dont_filter=True)


    def parse_json(self, response):
        result = loads(response.body)
        item = FlashItem()
        if result['status']:
            for data in result['data']:
                release_date = int(time.mktime(time.strptime(data['time'], '%Y%m%d%H%M%S')))
                self.end_ime = data['time']
                if self.low_time > release_date:
                    break
                item['release_date'] = release_date
                item['content'] = data['content']
                item['website'] = "http://lianmishu.com/"
                yield item
            release_date = int(time.mktime(time.strptime(self.end_ime, '%Y%m%d%H%M%S')))
            if self.low_time < release_date:
                next_url = 'http://lianmishu.com/wapi/kuaixun/list/?&type=down&pagesize=15&sourceid=-1&time=' + self.end_ime
                yield scrapy.Request(next_url, callback=self.parse_json, method='GET', dont_filter=True)