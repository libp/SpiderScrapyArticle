#coding:utf-8
import random
import re
import urllib2
from urllib import urlopen

import requests
import logging

import time
from bs4 import BeautifulSoup,Comment
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from z2.items import Z2Item
from scrapy.http import Request


class Spider(CrawlSpider):
    name = 'z2'
    host = 'http://www.umei.cc/p/gaoqing/xiuren_VIP/123401.htm'
    # start_urls = list(set(z2_TYPES))
    img_urls = []
    logging.getLogger("requests").setLevel(logging.WARNING)  # 将requests的日志级别设成WARNING
    logging.basicConfig(
        level=logging.INFO,
        format=
        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='cataline.log',
        filemode='w')

    def start_requests(self):
        '''
        如果请求的是一个随机地址，需要设置dont_filter=True，不过滤重复的请求
        :return:
        '''
        yield Request(url='http://www.umei.cc/p/gaoqing/xiuren_VIP/123401.htm',
                      callback=self.parse_z2_info)


    def parse_z2_info(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        img_urls = soup.findAll("img")
        item = Z2Item()
        for link in soup.findAll("img"):
            logging.info(link)
            url = link.attrs['src']
            self.img_urls.append(url)

        item['image_urls'] = self.img_urls
        yield item
    #
    #     # logging.info(soup)
    #     # yield z2Item









