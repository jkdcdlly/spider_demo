# -*- coding: utf-8 -*-
import scrapy
import spider_demo.items as items
#
# class DemoSpider(scrapy.Spider):
#     name = 'demo'
#     allowed_domains = ['www.ownedcore.com']
#     start_urls = ['https://www.ownedcore.com/forums/showthread.php?t=672976']
#
#     def parse(self, response):
#         mate_desc = response.xpath("//meta[@name='description']/@content").extract_first()
#         print("-----------------", mate_desc)
#         mate_key = response.xpath("//meta[@name='keywords']/@content").extract_first()
#         print("-----------------", mate_key)


# -*- coding: utf-8 -*-
from scrapy import Spider, Request
# from scrapy_splash import SplashRequest

import importlib,sys
#sys.setdefaultencoding('utf-8')
importlib.reload(sys)

# sys.stdout = open('demo01.txt', 'w')

print("1=" * 40)
class TestSpider(Spider):
    name = "test123"
    allowed_domains = ["jd.com"]
    start_urls = [
        "http://www.jd.com/"
    ]

    def parse(self, response):
        print("3=" * 40)