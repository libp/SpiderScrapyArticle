import re


def getAra():

    href='http://www.umei.cc/p/gaoqing/rihan/125300.htm'
    com_id = re.match(".*/(\d+)", href)

    print com_id.group(1)

    src='http://i1.umei.cc/uploads/tu/201803/9999/d0a7773d45.jpg'
    name = src.split('/')[-1]
    print name

    print "{0}{0}".format("py")

getAra()