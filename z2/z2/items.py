# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item

class Z2Item(Item):
    image_urls = Field()
    name = Field()
    url = Field()
    images = Field()
    desc = Field()
    pageCounts = Field()
    tags = Field()
    id = Field()
    title = Field()
    pass



