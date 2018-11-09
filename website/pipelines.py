# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from uuid import uuid1
from hashlib import md5
import time
from html import escape


class WebsitePipeline(object):

    def __init__(self):

        self.obj = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='new_im')
        self.cursor = self.obj.cursor()


    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        uuid = md5(str(uuid1()).encode('utf-8')).hexdigest()

        sql = """select id from article where author="{}" and title="{}" """.format(item['author'], item['title'])
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result:
            return item



        #cover_map = self.__img_upload(item['img_src'])
        cover_map = item['img_src']
        sql = """insert into article (uuid,title,author,cover_map,content,add_time) values('{0}',"{1}",'{2}','{3}','{4}','{5}')""".\
            format(uuid, item['title'], item['author'], cover_map, escape(str(item['content'])), item['release_date'])
        #print(sql)
        self.cursor.execute(sql)
        self.obj.commit()
        return item


    def __img_upload(self,img):
        import requests
        import base64
        import json
        from datetime import datetime
        if img:
            year = datetime.now().year
            month = datetime.now().month
            day = datetime.now().day
            extType = str.split(img, '.')

            files = {'system_mmmb': requests.get(img).content}
            fname = md5(str(time.time()).encode('utf-8')).hexdigest()

            postData = {
                'access_token': 'qdrcbex5wrhy1kl0vp0w9sd54akq0b1z',
                'attach_dir': "/jic/files/mmmb/article/img/{}/{}".format(year, str(month)+str(day)),
                'file_name': fname + '.' + extType[-1]

            }
            headers = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
            }
            imgUrl = 'http://img.chain-bar.com/jic/upload_system_img.html'
            r = requests.post(imgUrl)
            print(str(base64.b64decode(r.text), encoding='utf-8'))
            r = requests.post(imgUrl, headers=headers, files=files, data=postData)
            c = r.content.decode('utf-8', errors='replace')
            print(c)
            result = str(base64.b64decode(c), encoding='utf-8')
            result = json.loads(result)
            if result['success']:
                fileUrl = 'http://img.chain-bar.com/' + postData['attach_dir'] + '/' + postData['file_name']
            else:
                fileUrl = ''
            return fileUrl
        else:
            return ''

    def close_spider(self, spider):
        self.obj.close()


class FlashPipeline(object):
    def __init__(self):

        self.obj = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='new_im')
        self.cursor = self.obj.cursor()


    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        sql = """select id from news_flash where content="{}" """.format(item['content'])
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result:
            return item
        uuid = md5(str(uuid1()).encode('utf-8')).hexdigest()
        sql = """insert into news_flash (content,add_time,uuid,website) values('{0}',"{1}",'{2}','{3}')""".\
            format(item['content'], item['release_date'], uuid, item['website'])
        #print(sql)
        self.cursor.execute(sql)
        self.obj.commit()
        return item




    def close_spider(self, spider):
        self.obj.close()
