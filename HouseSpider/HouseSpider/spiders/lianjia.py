# -*- coding: utf-8 -*-
import scrapy


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lainjia.com']
    start_urls = ['http://lainjia.com/']

    def parse(self, response):
        pass
