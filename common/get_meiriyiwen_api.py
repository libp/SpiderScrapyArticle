# -*- coding: utf-8 -*-
import httplib
import json

import logging

from datetime import date
import requests

from z1.sql import Sql

logging.basicConfig(
        level=logging.INFO,
        format=
        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='cataline.log',
        filemode='w')



def get_api(article_id):
    try:
        article_url = "https://interface.meiriyiwen.com/article/day?dev=1&date="+article_id
        logging.info(article_url)
        res = requests.get(article_url, verify=False)
        setting = res.json()
        title =  setting['data']['title']
        author =  setting['data']['author']
        article =  setting['data']['content']
        source = 'meiriyiwen'
        catagroery = 'z1'
        Sql.insert_dd_name(title, author, article,article_url, article_id,source,catagroery)

    except  Exception as e:
        logging.error(article_url+' request failure')
        logging.error(e)

def begin_req():
    # from 20110306 begin
    begin_num = 734202
    today = date.today()
    article_id = date.fromordinal(begin_num).isoformat()

    while cmp(str(today),str(article_id))!=0:
        get_api(article_id.replace('-', ''))
        begin_num += 1
        article_id = date.fromordinal(begin_num).isoformat()

if __name__ == '__main__':
    begin_req()