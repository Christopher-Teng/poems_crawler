# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import re

import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from .processors import modify_title


class ZhscCrawlerPipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        """
        将item中title字段的值修改为原title的值加上content中第一个以换行符结尾的诗句
        """
        adapter = ItemAdapter(item)
        if adapter['title'] is None or adapter['content'] is None:
            # 如果title或者content的值为空，则使用DropItem这个异常来跳出当前数据项的处理
            raise DropItem()
        adapter['title'] = modify_title(adapter['title'], adapter['content'])
        self.logger.debug(u'标题已成功经过修改，格式为：原标题 —— 诗文内容第一行 -- %(title)s', {'title': adapter['title']})
        spider.crawler.stats.inc_value('title_modify/modified', spider=spider)
        return item


class MongoDBPipeline:
    """
    将爬取数据存入MongoDB
    """
    def __init__(self, host='127.0.0.1', port=27017,username='',password='',auth_source='', db_name='zhsc_crawler', col_name='poems'):
        self.host = host
        self.port = port
        self.username=username
        self.password=password
        self.auth_source=auth_source
        self.db_name = db_name
        self.col_name = col_name
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        # 从配置文件中获取MongoDB的相关配置信息
        _host = crawler.settings.get('MONGO_HOST', '127.0.0.1')
        _port = crawler.settings.getint('MONGO_PORT', 27017)
        _username=crawler.settings.get('MONGO_USERNAME','root')
        _password=crawler.settings.get('MONGO_PASSWORD','123456')
        _auth_source=crawler.settings.get('MONGO_AUTHSOURCE','admin')
        _db_name = crawler.settings.get('MONGO_DB', 'zhsc_crawler')
        _col_name = crawler.settings.get('MONGO_COLLECTION', 'poems')
        return cls(_host, _port,_username,_password,_auth_source, _db_name, _col_name)

    def open_spider(self, spider):
        # 启动蜘蛛时连接数据库
        self.connection = pymongo.MongoClient(host=self.host, port=self.port,username=self.username,password=self.password,authSource=self.auth_source)
        self.db = self.connection[self.db_name]
        self.collection = self.db[self.col_name]

    def close_spider(self, spider):
        # 关闭蜘蛛时关闭连接
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.collection.insert_one(dict(item))
        self.logger.debug(u'数据已插入MongoDB！ %(title)s -- %(times)s -- %(author)s',
                          {'title': adapter['title'], 'times': adapter['times'], 'author': adapter['author']})
        spider.crawler.stats.inc_value('mongodb/inserted', spider=spider)
        return item
