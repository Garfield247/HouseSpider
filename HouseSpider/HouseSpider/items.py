# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HousespiderItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    tag = scrapy.Field()
    house = scrapy.Field()
    typ = scrapy.Field()
    area = scrapy.Field()
    orient = scrapy.Field()
    info = scrapy.Field()
    installation = scrapy.Field()
    pub_date = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    city = scrapy.Field()
