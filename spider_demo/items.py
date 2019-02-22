# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Recipes(scrapy.Item):
    origin_url = scrapy.Field()
    cate = scrapy.Field()
    title = scrapy.Field()
    imgs = scrapy.Field()
    content = scrapy.Field()


class SchoolInfo(scrapy.Item):
    school_name = scrapy.Field()
    xiaozhang = scrapy.Field()
    email = scrapy.Field()
    site = scrapy.Field()
    cate = scrapy.Field()
    type = scrapy.Field()
    address = scrapy.Field()
    zip = scrapy.Field()
    phone = scrapy.Field()
    fax = scrapy.Field()
    info = scrapy.Field()
    mark = scrapy.Field()


class PlayerUp(scrapy.Item):
    cate1_title = scrapy.Field()
    cate2_title = scrapy.Field()
    detail_title = scrapy.Field()
    detail_url = scrapy.Field()
    mate_desc = scrapy.Field()
    mate_key = scrapy.Field()
    detail = scrapy.Field()


class DuoKanItem(scrapy.Item):
    book_id = scrapy.Field()
    book_url = scrapy.Field()
    book_img = scrapy.Field()
    book_title = scrapy.Field()
    book_author = scrapy.Field()
    book_translator = scrapy.Field()
    book_copyright = scrapy.Field()
    book_datePublished = scrapy.Field()
    book_grade = scrapy.Field()
    book_score = scrapy.Field()
    book_rating = scrapy.Field()
    new_price = scrapy.Field()
    old_price = scrapy.Field()
    book_content = scrapy.Field()
    book_catalogue = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    classify = scrapy.Field()


class IReadWeekItem(scrapy.Item):
    book_id = scrapy.Field()
    book_url = scrapy.Field()
    book_img = scrapy.Field()
    book_title = scrapy.Field()
    book_author = scrapy.Field()
    book_translator = scrapy.Field()
    book_copyright = scrapy.Field()
    book_datePublished = scrapy.Field()
    book_grade = scrapy.Field()
    book_score = scrapy.Field()
    book_rating = scrapy.Field()
    new_price = scrapy.Field()
    old_price = scrapy.Field()
    book_content = scrapy.Field()
    book_catalogue = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    classify = scrapy.Field()
    down_url = scrapy.Field()
    is_enable = scrapy.Field()
