

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import os

class CsdnPipeline(object):

    # sqlite
    # 自动启动函数
    def __init__(self):
        # 创建数据库
        self.setupDB()
        # 创建表单
        self.createSQLDB()

    def setupDB(self):
        # 创建sqllite数据库
        self.con = sqlite3.connect(os.getcwd()+'/CSDNsql')
        # 创建数据库指针， 所有命令需要通过指针执行
        self.cur = self.con.cursor()

    def createSQLDB(self):
        # 删除表单
        self.dropTable()
        # 创建表单
        self.createTable()
        pass

    def dropTable(self):
        # sql 语句  如果存在表单删除
        sql = """
        DROP TABLE if EXISTS CSDN
        """
        # 执行语句
        self.cur.execute(sql)
        pass

    def createTable(self):
        # sql 语句 创建表单
        sql = """
        create table CSDN(
        id INTEGER PRIMARY KEY NOT NULL ,
        title MESSAGE_TEXT ,
        content MESSAGE_TEXT ,
        link MESSAGE_TEXT 
        )
        """
        # 执行sql语句
        self.cur.execute(sql)
        pass



    def process_item(self,item,spider):
        # 启动数据保存函数
        self.item_store(item)

        return item

    def item_store(self,item):
        # sql 存储命令
        sql = """
        insert into CSDN(title,content,link) VALUES ('%s','%s','%s')
        """%(item['title'],item['content'],item['link'])
        # 执行sql语句  但是存储在内存中
        self.cur.execute(sql)
        # 执行这一步才会真正存储到数据库
        self.con.commit()
        # self.closeDB()
        pass
    # 关闭数据库
    def __del__(self):
        # 关闭
        self.cur.close()
        self.con.close()
        pass

