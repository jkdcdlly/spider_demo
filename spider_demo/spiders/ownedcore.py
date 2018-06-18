# -*- coding: utf-8 -*-
import scrapy
import spider_demo.items as items
import hashlib

import uuid


class OwnedcoreSpider(scrapy.Spider):
    name = 'ownedcore'
    allowed_domains = ['www.ownedcore.com']
    start_urls = ['https://www.ownedcore.com/forums/mmo-trading-market/']

    def parse(self, response):
        post_items = response.xpath("//div[contains(@class,'forumrow')]")
        for post_item_body in post_items:
            item = items.HomeItem()
            item["title"] = post_item_body.xpath("div[1]/div/div/div/h2/a/text()").extract_first()
            item["url"] = post_item_body.xpath("div[1]/div/div/div/h2/a/@href").extract_first()
            item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, item["url"]))
            # yield item
            yield scrapy.Request(item["url"], callback=self.parse_list)

    #
    def parse_list(self, response):
        post_items = response.xpath("""//*[starts-with(@id,'thread_title_')]""")
        item = items.ListItem()
        for post_item_body in post_items:
            item["url"] = post_item_body.xpath("@href").extract_first()
            item["title"] = post_item_body.xpath("text()").extract_first()
            item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, item["url"]))
            # yield item
            yield scrapy.Request(item["url"], callback=self.parse_detail, meta={"title": item["title"]})

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
        yield item
