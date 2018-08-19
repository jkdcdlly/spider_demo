# -*- coding: utf-8 -*-
import scrapy
import spider_demo.items as items
import hashlib
from datetime import datetime
import uuid


class OwnedcoreSpider(scrapy.Spider):
    name = 'ownedcore'
    allowed_domains = ['www.ownedcore.com']
    start_urls = ['https://www.ownedcore.com/forums/mmo-trading-market/']

    def parse(self, response):
        post_items = response.xpath("//div[contains(@class,'forumrow')]")
        for post_item_body in post_items:
            item = items.HomeItem()
            title = post_item_body.xpath("div[1]/div/div/div/h2/a/text()").extract_first()
            item["title"] = title
            item["url"] = post_item_body.xpath("div[1]/div/div/div/h2/a/@href").extract_first()
            item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, item["url"]))
            # item["create_time"] = datetime.now()
            yield item
            yield scrapy.Request(item["url"], callback=self.parse_list, meta={
                "title": item["title"],
                "game_name": title.split("Buy Sell Trade")[0]
            })

    #
    def parse_list(self, response):
        post_items = response.xpath("""//*[starts-with(@id,'thread_title_')]""")
        item = items.ListItem()
        for post_item_body in post_items:
            item["url"] = post_item_body.xpath("@href").extract_first()
            item["title"] = post_item_body.xpath("text()").extract_first()
            item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, item["url"]))
            item["game_name"] = response.meta['game_name']
            item["trade_type"] = "Account Trade"
            # item["create_time"] = datetime.now()
            yield item
            yield scrapy.Request(item["url"], callback=self.parse_detail, meta={
                "title": item["title"],
                "game_name": response.meta['game_name']
            })

    def parse_detail(self, response):
        item = items.DetailItem()
        item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, response.url))
        item["url"] = response.url
        item["title"] = response.meta["title"]
        mate_desc = response.xpath("//meta[@name='description']/@content").extract_first()
        item["mate_desc"] = '' if mate_desc is None else mate_desc
        mate_key = response.xpath("//meta[@name='keywords']/@content").extract_first()
        item["mate_key"] = '' if mate_key is None else mate_key
        item["postList_id"] = item["id"]
        item["game_name"] = response.meta['game_name']
        item["trade_type"] = "Account Trade"
        # item["create_time"] = datetime.now()
        table = response.xpath('//div[contains(@id,"post_message_")]')[0]
        item["post_detail"] = table.extract()

        yield item
