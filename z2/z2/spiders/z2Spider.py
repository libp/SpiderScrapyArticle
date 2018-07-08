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

logging.basicConfig(
    level=logging.INFO,
    format=
    '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='cataline.log',
    filemode='w')

class Spider(CrawlSpider):
    name = 'z2'
    host = 'http://www.umei.cc/'
    img_urls = []
    allowed_domains = ["www.umei.cc"]
    start_urls = ['http://www.umei.cc/p/gaoqing/rihan/']
    # rules = (
    #     Rule(LinkExtractor(allow=('http://www.umei.cc/p/gaoqing/rihan/\d{1,6}.htm',), deny=('http://www.umei.cc/p/gaoqing/rihan/\d{1,6}_\d{1,6}.htm')),
    #          callback='parse_z2_key', follow=True),
    # )

    def start_requests(self):
        yield Request(url='http://www.umei.cc/p/gaoqing/rihan/',
                      callback=self.parse_z2_key)

    def parse_z2_key(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        content = soup.find("div", attrs={'class': 'TypeList'})
        # logging.debug(content)
        for link in content.findAll("a", attrs={'href': re.compile( r'(.*)(/rihan/)(\d{1,6})(.htm)'), 'class': 'TypeBigPics'}):
            logging.debug(link['href'])
            yield Request(url=link['href'],
                          callback=self.parse_z2_info)
            # break

    def parse_z2_info(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        # 去除html注释
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()

        # 过滤script标签
        [s.extract() for s in soup('script')]

        # 过滤b标签
        [s.extract() for s in soup('b')]


        ArticleDesc = soup.find("p", attrs={'class': 'ArticleDesc'})
        logging.debug(ArticleDesc.get_text())

        Pages = soup.find("div", attrs={'class': 'NewPages'}).find('li')
        pageCounts = filter(str.isdigit, Pages.get_text().encode('gbk'))
        # 第一种含中文的字符串中提取数字的方法
        # logging.debug(re.findall(r"\d+\.?\d*", Pages.get_text())[0])

        # 第二种
        # logging.debug(Pages.get_text()[1:-3])

        # 第三种
        logging.debug(filter(str.isdigit, Pages.get_text().encode('gbk')))

        img = soup.find("div", attrs={'class': 'ImageBody'}).find('img')
        url = img.attrs['src']
        self.img_urls.append(url)
        logging.debug(self.img_urls)


        sourceUrl = response.url[0:-4]
        # logging.debug(sourceUrl)
        for i in xrange(1, int(pageCounts) + 1):
            nextUrl = sourceUrl + '_' + str(i) + '.htm'
            # logging.debug(nextUrl)
            yield Request(url=nextUrl,callback=self.parse_z2_single_img, priority = 10000)



    def parse_z2_single_img(self, response):
        item = Z2Item()
        img_urls= []
        soup = BeautifulSoup(response.body, "lxml")
        item['name'] = re.match(".*/(\d+)", response.url).group(1)
        logging.debug(item['name'])
        img = soup.find("div", attrs={'class': 'ImageBody'}).find('img')
        url = img.attrs['src']
        img_urls.append(url)
        item['image_urls'] = img_urls
        yield item
        # logging.debug(self.img_urls)






