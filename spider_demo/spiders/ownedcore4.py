# # -*- coding: utf-8 -*-
# import scrapy
# import spider_demo.items as items
# import hashlib
#
# import uuid
#
#
# class OwnedcoreSpider(scrapy.Spider):
#     name = 'ownedcore'
#     allowed_domains = ['www.ownedcore.com']
#     start_urls = ['https://www.ownedcore.com/forums/mmo-trading-market/']
#
#     def parse(self, response):
#         #
#         post_items = response.xpath("//div[@id='forumbits']//a")
#         print(len(post_items),"================")
#         for post_item in post_items:
#             print(post_item)
#             item = items.HomeItem()
#             item["url"] = post_item.xpath("@href").extract_first()
#             item["title"] = post_item.xpath("text()").extract_first()
#             item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, item["url"]))
#             yield item
#             # yield scrapy.Request(item["url"], callback=self.parse_list)
#
#     def parse_list(self, response):
#         post_items = response.xpath("//div[@class=forumbits]//a")
#         for post_item in post_items:
#             item = items.ListItem()
#             item["url"] = post_item.xpath("@href").extract_first()
#             item["title"] = post_item.xpath("text()").extract_first()
#             item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, item["url"]))
#             yield item
#             yield scrapy.Request(item["url"], callback=self.parse_detail)
#
#     def parse_detail(self, response):
#         item = items.DetailItem()
#         item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, response.url))
#         item["mate_desc"] = response.xpath("//meta[@name='description']/@content").extract_first()
#         item["mate_key"] = response.xpath("//meta[@name='keywords']/@content").extract_first()
#         item["postList_id"] = item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, response.url))
#         yield item
