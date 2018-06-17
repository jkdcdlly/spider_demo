# -*- coding: utf-8 -*-
import scrapy
import spider_demo.items as items

class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['www.ownedcore.com']
    start_urls = ['https://www.ownedcore.com/forums/showthread.php?t=672976']

    def parse(self, response):
        mate_desc = response.xpath("//meta[@name='description']/@content").extract_first()
        print("-----------------", mate_desc)
        mate_key = response.xpath("//meta[@name='keywords']/@content").extract_first()
        print("-----------------", mate_key)
