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
#         # post_items = response.xpath("//div[@id='forumbits']/div[@class='forumbitBody']/ol/li")
#
#         post_items = response.xpath("//div[contains(@class,'forumrow')]")
#         print(len(post_items), "========================================")
#         for post_item_body in post_items:
#             item = items.OwnedCoreHomeItem()
#             item["title"] = post_item_body.xpath("div[1]/div/div/div/h2/a/text()").extract_first()
#             item["text"] = post_item_body.xpath("div[1]/div/div/p/text()").extract_first()
#             item["url"] = post_item_body.xpath("div[1]/div/div/div/h2/a/@href").extract_first()
#             posts = post_item_body.xpath("ul[2]/li/span/text()").extract_first()
#             item["posts"] = (0 if posts is None else int(posts.replace(',', '')))
#             threads = post_item_body.xpath("ul[1]/li/span/text()").extract_first()
#             item["threads"] = (0 if threads is None else int(threads.replace(',', '')))
#             item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, item["url"]))
#             yield item
#             # self.page_index += 1
#             # if self.page_index <= 20:
#             #     next_page_url = "https://www.cnblogs.com/cate/mysql/" + str(self.page_index)
#             # else:
#             #     next_page_url = None
#             #
#             # if next_page_url is not None:
#             yield scrapy.Request(item["url"], callback=self.parse_list)
#
#             # break
#
#     #
#     def parse_list(self, response):
#         post_items = response.xpath("""//*[starts-with(@id,'thread_title_')]""")
#         list_item = items.OwnedCoreListItem()
#         for post_item_body in post_items:
#             list_item["url"] = post_item_body.xpath("@href").extract_first()
#             list_item["title"] = post_item_body.xpath("text()").extract_first()
#             list_item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, list_item["url"]))
#             list_item["trade_id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, response.url))
#             yield list_item
