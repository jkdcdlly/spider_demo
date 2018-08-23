# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderDemoItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
    threads = scrapy.Field()
    posts = scrapy.Field()


class OwnedCoreHomeItem(scrapy.Item):
    # id = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()
    threads = scrapy.Field()
    posts = scrapy.Field()


class OwnedCoreListItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()
    trade_id = scrapy.Field()


# postdetail
# posthome
# postlist

class HomeItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class polls_gameinfo(scrapy.Item):
    id = scrapy.Field()
    game_name = scrapy.Field()
    game_img_url = scrapy.Field()
    post_num = scrapy.Field()


class ListItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    game_name = scrapy.Field()
    trade_type = scrapy.Field()


class DetailItem(scrapy.Item):
    id = scrapy.Field()
    mate_desc = scrapy.Field()
    mate_key = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    postList_id = scrapy.Field()
    game_name = scrapy.Field()
    trade_type = scrapy.Field()
    post_detail = scrapy.Field()


class Schools(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    school_name = scrapy.Field()
    school_desc = scrapy.Field()
