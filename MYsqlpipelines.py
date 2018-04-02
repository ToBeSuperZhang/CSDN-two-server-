# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import os
from scrapy.utils.project import get_project_settings


class CsdnPipeline(object):

    # mysql
    # 自动调用
    def __init__(self):
        # 这句话相当于 from 。setting import DATABASE
        setting = get_project_settings()
        # 获取 登录信息
        self.database = setting['DATABASE']
        # 调用链接函数
        self.mysql_connect()
        pass

    def mysql_connect(self):
        # 链接数据库
        self.con = pymysql.connect(
            host=self.database['host'],
            port=self.database["port"],
            user=self.database["user"],
            password=self.database["password"],
            db=self.database["db"],
            charset=self.database["charset"]
        )
        # 执行
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        # 调用存储函数
        self.item_store(item)
        return item

    def item_store(self, item):
        # 开启sql语句
        sql = """
        insert into CSDN(title,content,link) VALUES ('%s','%s','%s')
        """ % (item['title'], item['content'], item['link'])
        # 执行sql语句
        self.cur.execute(sql)
        # 必须使用这个命令才能真正存储到数据库，不执行则暂时存储在内存
        self.con.commit()

    # 自动调  关闭数据库
    def __del__(self):
        self.cur.close()
        self.con.close()
