# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

import spider_demo.items as items


class SpiderDemoPipeline(object):
    def __init__(self, mysql_host, mysql_user, mysql_passwd, mysql_db):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_passwd = mysql_passwd
        self.mysql_db = mysql_db
        # 打开数据库连接

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),  # 从 settings.py 提取
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_passwd=crawler.settings.get('MYSQL_PASSWD'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(self.mysql_host, self.mysql_user, self.mysql_passwd, self.mysql_db,
                                    charset='utf8mb4', )
        # 使用 cursor() 方法创建一个游标对象 cursor
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
        placeholders = ', '.join(['%s'] * len(item.keys()))

        insert_sql = "replace into {0} ({1}) values ({2})".format(table, cols, placeholders)

        print(insert_sql)
        self.cur.execute(insert_sql, tuple(item.values()))

        self.conn.commit()

        return item
