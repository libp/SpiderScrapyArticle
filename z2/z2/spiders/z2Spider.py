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
from z1.sql import Sql

logging.basicConfig(
    level=logging.INFO,
    format=
    '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='cataline.log',
    filemode='w')

class Spider(CrawlSpider):
    name = 'z2'
    allowed_domains = ["www.umei.cc"]
    start_urls = ['http://www.umei.cc/']
    # rules = (
    #     Rule(LinkExtractor(allow=('http://www.umei.cc/p/gaoqing/rihan/\d+.htm',
    #                               'http://www.umei.cc/p/gaoqing/gangtai/\d+.htm',
    #                               'http://www.umei.cc/p/gaoqing/oumei/\d+.htm',
    #                               'http://www.umei.cc/p/gaoqing/xiuren_VIP/\d+.htm',
    #                               'http://www.umei.cc/p/gaoqing/cn/\d+.htm',
    #                               ), deny=('http://www.umei.cc/p/!gaoqing/*.htm')),
    #          callback='parse_z2_info', follow=True),
    # )

    def start_requests(self):
        for i in range(141):
            yield Request(url='http://www.umei.cc/p/gaoqing/rihan/%s.htm'%(str(i)),
                          callback=self.parse_z2_key)

    def parse_z2_key(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        content = soup.find("div", attrs={'class': 'TypeList'})
        # logging.debug(content)
        for li in content.findAll("li"):
            tags = []
            for tag in li.find_all('div')[1].find_all('a'):
                tags.append(tag.get_text())
            # logging.debug(tags)
            yield Request(url=li.a['href'],
                          callback=self.parse_z2_info,meta={'tags':tags})
            # break


        # for link in content.findAll("a", attrs={'href': re.compile(r'(.*)(\d+)(.htm)'),
        #                                         'class': 'TypeBigPics'}):
        #     logging.debug(link['href'])
        #     yield Request(url=link['href'],
        #                   callback=self.parse_z2_info)
        #     break

    def parse_z2_info(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        Pages = soup.find("div", attrs={'class': 'NewPages'}).find('li')
        pageCounts = filter(str.isdigit, Pages.get_text().encode('gbk'))

        sourceUrl = response.url[0:-4]
        for i in xrange(1, int(pageCounts) + 1):
            nextUrl = sourceUrl + '_' + str(i) + '.htm'
            yield  Request(url=nextUrl,callback=self.parse_z2_single_img,meta={'tags':response.meta['tags']})
            # break


    def parse_z2_single_img(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        [s.extract() for s in soup('b')]

        item = Z2Item()
        item['name'] = re.match(".*/(\d+)", response.url).group(1)
        item['url'] =  response.url

        id = response.url.split('/')[-1][0:-4].split('_')[-1]
        item['id'] = id
        if(int(id)==1):
            ArticleDesc = soup.find("p", attrs={'class': 'ArticleDesc'})
            item['desc'] = ArticleDesc.get_text()

            Pages = soup.find("div", attrs={'class': 'NewPages'}).find('li')
            pageCounts = filter(str.isdigit, Pages.get_text().encode('gbk'))
            item['pageCounts'] = pageCounts
            item['tags'] = response.meta['tags']

            item['title'] = soup.find("div",attrs={'class': 'ArticleTitle'}).get_text()

        img_urls = []
        img = soup.find("div", attrs={'class': 'ImageBody'}).find('img')
        img_urls.append(img.attrs['src'])
        item['image_urls'] = img_urls
        yield item






