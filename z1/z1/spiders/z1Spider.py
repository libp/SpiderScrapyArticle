#coding:utf-8
import requests
import logging

from bs4 import BeautifulSoup,Comment
from scrapy.spiders import CrawlSpider
from z1.items import Z1Item
from z1.z1_type import z1_TYPES
from scrapy.http import Request


class Spider(CrawlSpider):
    name = 'z1'
    host = 'https://meiriyiwen.com'
    start_urls = list(set(z1_TYPES))
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
        for i in range(3):
            parms = self.start_urls[0]+'?'+str(i)
            print parms
            yield Request(url='https://meiriyiwen.com/%s' % parms,
                          callback=self.parse_z1_info)


    def parse_z1_info(self, response):
        z1Item = Z1Item()
        soup = BeautifulSoup(response.body, "lxml")
        z1Item['article_url'] = response.url
        # 获取文章ID
        z1Item['article_id'] = soup.select(".article_id")[0].get('value')
        z1Item['title'] = soup.select("#article_show h1")[0].get_text();
        z1Item['author'] = soup.select(".article_author")[0].get_text();
        content = soup.select(".article_text")[0].contents;
        z1Item['article'] = ""
        for child in content:
            if('meiriyiwen' in child):
                print "xxxxxxxxxxxxxxx"
                continue
            z1Item['article'] += str(child)
        logging.info(unicode(z1Item['article'], encoding="utf-8"),z1Item['article_id'])
        yield z1Item









    # def parse(self, response):
    #     print(response.text)
    def parse(self, response):

        soup = BeautifulSoup(response.body , "lxml")
        # 去除html注释
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()

        # 过滤JavaScript
        [s.extract() for s in soup('script')]

        # 获取标题
        title = soup.select("#article_show h1")[0].get_text();

        # 获取作者
        author = soup.select(".article_author")[0].get_text();

        # 获取内容
        content = soup.select(".article_text")[0].contents;
        # 最终入库的文章内容
        article = ""
        for child in content:
            article += str(child)

        print(article)
