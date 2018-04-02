# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CsdnPipeline(object):


    # 
    def __init__(self):
        self.file = open('CSDNBlog.txt','ab+')
    def process_item(self, item, spider):

        self.file.write((str(item)+'\n').encode('utf-8'))
        self.file.flush()
        return item

    def __del__(self):
        self.file.close()
