# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class Z1Item(Item):
    #标题
    title = Field()
    #作者
    author = Field()
    #内容
    article = Field()
    #文章ID
    article_id = Field()
    #URL
    article_url = Field()
