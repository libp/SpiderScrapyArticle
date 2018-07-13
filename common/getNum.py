# -*- coding: utf-8 -*-
import re


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

getAra()