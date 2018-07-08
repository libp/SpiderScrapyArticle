# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import logging

from datetime import datetime
from scrapy.http import Request
import time
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from w3lib.util import to_bytes


class Z2Pipeline(ImagesPipeline):
    logging.basicConfig(
        level=logging.INFO,
        format=
        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='cataline.log',
        filemode='w')

    def file_path(self, request, response=None, info=None):
        url = request.url
        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()
        item = request.meta['item']
        logging.warn(item['name'])
        # folder = datetime.now().strftime('%Y%m%d%H%M%S%f')[0:-3]
        folder = item['name']
        return '%s/%s.jpg' % (folder,image_guid)
        # return 'fulls/%s.jpg' % (image_guid)

    def get_media_requests(self, item, info):
        logging.debug('img_urls:%s' % item['image_urls'])
        for image_url in item['image_urls']:
            logging.info('image_url：%s'%image_url)
            yield Request(image_url,meta={'item': item,'referer': ''})

    def item_completed(self, results, item, info):
        logging.debug("download results:%s"%results)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        return item