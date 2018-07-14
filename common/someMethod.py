# -*- coding: utf-8 -*-
import os
import re
import time

import datetime

import logging
import threadpool

from z2.sql import Sql

logging.basicConfig(
    level=logging.INFO,
    format=
    '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='cataline.log',
    filemode='w')


def getTime():
    t = time.time()
    print (t)  # 原始时间数据
    print (int(t))  # 秒级时间戳
    print (int(round(t * 1000)))  # 毫秒级时间戳

    nowTime = lambda: int(round(t * 1000))
    print (nowTime());  # 毫秒级时间戳，基于lambda

    print (datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[0:-3])  # 日期格式化

def getAra():

    href='http://www.umei.cc/p/gaoqing/rihan/125300.htm'
    com_id = re.match(".*/(\d+)", href)

    print com_id.group(1)

    src='http://i1.umei.cc/uploads/tu/201803/9999/d0a7773d45.jpg'
    name = src.split('/')[-1]
    print name

    print "{0}{0}".format("py")

    href_id = 'http://www.umei.cc/p/gaoqing/rihan/20120327030302_17.htm'
    id = href_id.split('/')[-1][0:-4].split('_')[-1]
    id2 = re.match(".*/(\d+)_(\d+)", href_id)
    print id
    print id2.group(2)

    src = 'http://i1.umei.cc/uploads/tu/201803/9999/d0a7773d45.jpg'
    postfix = src.split('/')[-1].split('.')[-1]
    print postfix

    # 第一种含中文的字符串中提取数字的方法
    # logging.debug(re.findall(r"\d+\.?\d*", Pages.get_text())[0])

    # 第二种
    # logging.debug(Pages.get_text()[1:-3])

    # 第三种
    # logging.debug(filter(str.isdigit, Pages.get_text().encode('gbk')))

    dir = 'http://www.umei.cc/p/gaoqing/rihan/20120327030302_17.htm'
    dir = dir.split('/')[-2]
    print dir

def sayhello(str):
    print "Hello ",str
    time.sleep(2)

def learnThreadPool():
    name_list = ['xiaozi', 'aa', 'bb', 'cc']
    start_time = time.time()
    pool = threadpool.ThreadPool(100)
    requests = threadpool.makeRequests(sayhello, name_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    print '%d second' % (time.time() - start_time)


def judgeRepeat():
    """
    会更新数据库deleted字段，如果本地有数据库也有，将其表示为1
    本方法为一次性方法，update_count不可随意执行
    :return:
    """
    path = "C:/Test01/xxx/"
    parents = os.listdir(path)
    for parent in parents:
        count = Sql.update_count(parent)
        logging.info(count)
        if(count<1):
            logging.info(parent)


def updateImgCount(path):
    """
    更新本地文件的名字，按找数量从1开始排序
    更新数据库中imgcount的大小
    :return:
    """
    parents = os.listdir(path)
    for parent in parents:
        child = os.path.join(path, parent)
        parents = os.listdir(child)
        count = len(parents)
        result = Sql.select_imgs(parent)[2]
        if(count==result):
            # print 'that is right'
            logging.debug('that is right')
        else:
            Sql.update_img_count(parent,count)
            # print parent,count
            logging.info('that is right')
            child = os.path.join(path, parent)
            rename_img(child)


def rename_img(path):
    """
    对图片排序后改名
    :param path:
    :return:
    """
    imgs = os.listdir(path)
    spilt_num_postfix = []
    num = []
    for img in imgs: spilt_num_postfix.append(img.split('.'))
    for n in spilt_num_postfix: num.append(int(n[0]))
    num.sort()
    new = 1
    for i in num:
        os.rename(path + '/' + str(i) + '.jpg', path + '/' + str(new) + '.jpg')
        new += 1


if __name__ == "__main__":
    # judgeRepeat()


    path = "C:/Test01/rihan/"
    updateImgCount(path)
