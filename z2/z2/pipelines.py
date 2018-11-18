# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import logging

from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from z2.sql import Sql


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
        postfix = url.split('/')[-1].split('.')[-1]
        item = request.meta['item']
        imageName = item['url'].split('/')[-1][0:-4].split('_')[-1]
        category = item['url'].split('/')[-2]
        folder = item['name']
        return '%s/%s/%s.%s' % (category,folder,imageName,postfix)

    def get_media_requests(self, item, info):
        # logging.debug('img_urls:%s' % item['image_urls'])
        for image_url in item['image_urls']:
            # logging.info('image_url：%s'%image_url)
            self.insert_img(item)
            yield Request(image_url,meta={'item': item,'referer': ''})

    def item_completed(self, results, item, info):
        logging.debug("download results:%s"%results)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        return item

    def insert_img(self,item):
        category = item['url'].split('/')[-2]
        folder = item['name']

        if (item['id'] == 1):
            logging.info("****************operate database****************")
            Sql.insert_img(folder, item['pageCounts'], item['title'], category, item['desc'], ','.join(item['tags']))
            for tag in item['tags']:
                Sql.insert_tag(tag, folder)
