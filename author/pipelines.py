# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class ImgDownloadPipeline(ImagesPipeline) :
    def get_media_requests(self, item, info):
        yield Request(item['Img'],meta={'item':item})
    def file_path(self,request,response=None,info=None):
        item = request.meta['item']
        #image_guid = request.url.split('?')[0].split('/')[-1].split('.')[-1]
        filename = u'full/{0[Username]}.jpg'.format(item)
        return filename

class AuthorPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def _conditional_insert(self, tx, item):
        sql = "insert into jianshu_author(id,username,profile,src,img,sex,attention,fans,article,word_num,like_num,created_date)" +\
              " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now()) " +\
              "on duplicate key update username=%s,profile=%s,src=%s,img=%s,sex=%s,attention=%s,fans=%s,article=%s,word_num=%s,like_num=%s,created_date=now() "
        params = (item['Id'], item['Username'], item['Profile'], item['Src'], item['Img'], item['Sex'],item['Attention'],item['Fans'],item['Article'],item['WordNum'],item['LikeNum'],
                  item['Username'], item['Profile'], item['Src'], item['Img'], item['Sex'],item['Attention'],item['Fans'],item['Article'],item['WordNum'],item['LikeNum'])
        tx.execute(sql, params)

    def _handle_error(self, failure, item, spider):
        print(failure)
