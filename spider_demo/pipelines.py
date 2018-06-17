# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html




# class SpiderDemoPipeline(object):
#     def open_spider(self, spider):
#         import redis  # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库
#         pool = redis.ConnectionPool(host='140.143.22.203', port=6379, decode_responses=True, password="redis_foobared",
#                                     db=0)
#         self.r = redis.Redis(connection_pool=pool)
#
#         # self.fp = open("data.list", "w")
#
#     def close_spider(self, spider):
#         pass
#         # self.fp.close()
#
#     def process_item(self, item, spider):
#         self.r.lpush("ownedcore_home",
#                      "\u0001".join([
#                          item["article_title"],
#                          item["article_href"],
#                          item["article_summary"],
#                          ('0' if item["threads_num"] == None else item["threads_num"]),
#                          ('0' if item["posts_num"] == None else item["posts_num"])
#                      ])
#
#                      )
#         # self.fp.write("[ " + item["article_title"] + " ]\t")
#         # self.fp.write("[ " + item["article_href"] + " ]\t")
#         # # self.fp.write("[ "+ item["article_title2"] + " ]\t")
#         # self.fp.write("[ " + item["article_summary"] + " ]\t")
#         #self.fp.write("[ " + ('0' if item["threads_num"] == None else item["threads_num"]) + " ]\t")
#         #self.fp.write("[ " + ('0' if item["threads_num"] == None else item["posts_num"]) + " ]\t")
#         # self.fp.write("\n")
#
#         return item


import sqlite3

import spider_demo.items as items


class SpiderDemoPipeline(object):
    def __init__(self, sqlite_file, sqlite_table):
        self.sqlite_file = sqlite_file
        self.sqlite_table = sqlite_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file=crawler.settings.get('SQLITE_FILE'),  # 从 settings.py 提取
            sqlite_table=crawler.settings.get('SQLITE_TABLE', 'items')
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, items.OwnedCoreHomeItem):
            table = "polls_trade"
        elif isinstance(item, items.OwnedCoreListItem):
            table = "polls_wonlist"
        elif isinstance(item, items.HomeItem):
            table = "polls_posthome"
        elif isinstance(item, items.ListItem):
            table = "polls_postlist"
        elif isinstance(item, items.DetailItem):
            table = "polls_postdetail"
        cols = ', '.join(item.keys())
        placeholders = ', '.join(['?'] * len(item.keys()))

        insert_sql = "replace into {0} ({1}) values ({2})".format(table, cols, placeholders)

        print(insert_sql)
        self.cur.execute(insert_sql, tuple(item.values()))

        self.conn.commit()

        return item
