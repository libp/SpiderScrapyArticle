# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from z1.items import Z1Item
from z1.sql import Sql


class Z1Pipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, Z1Item):
            article_url = item['article_url']
            article_id = item['article_id']
            title = item['title']
            author = item['author']
            article = item['article']
            source = 'meiriyiwen'
            catagroery = 'z1'
            Sql.insert_dd_name(title, author, article,article_url, article_id,source,catagroery)
        return item