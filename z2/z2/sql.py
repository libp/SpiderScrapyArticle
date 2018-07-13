import MySQLdb
from z1 import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_DB = settings.MYSQL_DB
MYSQL_CHARSET = settings.MYSQL_CHARSET

cnx = MySQLdb.connect(host=MYSQL_HOSTS, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DB, charset=MYSQL_CHARSET)
cur = cnx.cursor()

class Sql:

    @classmethod
    def insert_img(cls,num, imgcount, title, category,description,tag):
        sql = "insert into tbl_nichuiniu_img (num,imgcount,title,category,description,tag) " \
                           "values (%s,%s,%s,%s,%s,%s)"

        cur.execute(sql, (num, imgcount, title,category,description,tag))
        cnx.commit()

    @classmethod
    def insert_tag(cls, tagName, ImgNum):
        sql = "insert into tbl_nichuiniu_img_tags (tagName,ImgNum) " \
              "values (%s,%s)"

        cur.execute(sql, (tagName, ImgNum))
        cnx.commit()

    @classmethod
    def select_count(cls, ImgNum):
        sql = 'SELECT COUNT(*) from tbl_nichuiniu_img where Num =%(ImgNum)s;'
        value = {
            'ImgNum': ImgNum
        }
        cur.execute(sql, value)
        return cur.fetchone()

    @classmethod
    def id_name(cls, xs_name):
        sql = 'SELECT id FROM dd_name WHERE xs_name=%(xs_name)s'
        value = {
            'xs_name': xs_name
        }
        cur.execute(sql, value)
        for name_id in cur:
            return name_id[0]

    @classmethod
    def select_name(cls, name_id):
        sql = "SELECT EXISTS(SELECT 1 FROM dd_name WHERE name_id=%(name_id)s)"
        value = {
            'name_id': name_id
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]

    @classmethod
    def sclect_chapter(cls, url):
        sql = "SELECT EXISTS(SELECT 1 FROM dd_chaptername WHERE url=%(url)s)"
        value = {
            'url': url
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]