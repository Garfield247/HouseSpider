# -*- coding: utf-8 -*-
import re
import scrapy
from HouseSpider.items import HousespiderItem

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    # allowed_domains = ['lainjia.com']
    start_urls = ['https://bj.lianjia.com/zufang/','https://sh.lianjia.com/zufang/', 'https://sz.lianjia.com/zufang/', 'https://gz.lianjia.com/zufang/']

    house_list_url = '{0}pg{1}'

    def parse(self, response):
        districts = {a.xpath("./text()").extract_first():response.urljoin(a.xpath("./@href").extract_first()) for a in  response.xpath("//div[@id='filter']/ul[2]/li/a")[1:]}
        print(districts)
        for district,url in districts.items():
            yield scrapy.Request(self.house_list_url.format(url, 1),callback=self.parse_list,meta={'district':district,'pg':1})

    def parse_list(self,response):
        district = response.meta['district']
        pg = response.meta['pg']
        info_urls = [ response.urljoin(url) for url in re.findall(r'href="(/zufang/.*?\d+.html)"', response.text)]
        print(info_urls)
        if len(info_urls) > 0:
            for info_url in info_urls:
                yield scrapy.Request(info_url, callback=self.parse_info, meta={'district': district})
            next_url = response.url.replace(str(pg),str(pg+1))
            yield scrapy.Request(next_url, callback=self.parse_list, meta={'district': district, 'pg': pg+1})

    def parse_info(self,response):
        district = response.meta['district']
        item = HousespiderItem()

        item['district'] = district
        item['city'] = re.findall(r'https://(.*?).lianjia.com/',response.url)[0]
        item['price'] = response.xpath("//div[@id='aside']/p[@class='content__aside--title']/span/text()").extract_first()
        item['tag'] = response.xpath("//div[@id='aside']/p[@class='content__aside--tags']/i/text()").extract()
        item['house'] = response.xpath("//i[@class='house']/../text()").extract_first()
        item['typ'] = response.xpath("//i[@class='typ']/../text()").extract_first()
        item['area'] = response.xpath("//i[@class='area']/../text()").extract_first()
        item['orient'] = response.xpath("//i[@class='orient']/../text()").extract_first()
        item['info'] = {info.split('：')[0]: info.split('：')[1] for info in response.xpath( "//div[@class='content__article__info']/ul/li[starts-with(@class,'fl')]/text()").extract() if '：' in info}
        # item['info'] = response.xpath("//div[@class='content__article__info']/ul/li[starts-with(@class,'fl')]/text()").extract()
        item['installation'] = {li.xpath("./i/../text()").extract_first():li.xpath('./@class').extract_first() for li in response.xpath("//ul[@class='content__article__info2']/li")[1:]}
        item['pub_date'] = response.xpath("//div[@class='content__subtitle']/text()").extract()[1]
        item['address'] = response.xpath("//p[@class='content__title']/text()").extract_first()
        yield item


