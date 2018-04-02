# -*- coding: utf-8 -*-
import scrapy
import requests
from ..items import  CsdnItem

class CsdnblogSpider(scrapy.Spider):
    name = 'CSDNBlog'
    allowed_domains = ['blog.csdn.net']
    start_urls = ['https://blog.csdn.net/itcastcpp/article/list/1']

    def parse(self, response):
        print('-------------------------------')
        # 解析网页，获取 列表
        url_list = response.xpath('//li[@class= "blog-unit"]/a/@href').extract()
        for url in url_list:
            # 将网页 以迭代方式 赋予 函数 parse——connect
            yield scrapy.Request(url,callback=self.parse_content)
        pass
    def parse_content(self,response):
        print('++++++++++++++++++++++++++++++')
        # 将筛选出的信息 存入item类
        item = CsdnItem()
        item['title']=''.join(response.xpath("//article/h1/text()").extract())
        item['content'] = ''.join(response.xpath("//article//div[@class='markdown_views']//text()").extract()).strip(
        ).replace('"','').replace("'","")
        # 获解析网页的url
        item['link'] = response.url

        # 执行完这一步 会通过 setting 里的 ITEM_PIPELINES 调用 相应函数
        # 函数根据 函数后面数字 由小到大 依次执行。

        # middlewares 在本项目中 只执行 随机设置 网站头信息和 随机端口
        yield item


