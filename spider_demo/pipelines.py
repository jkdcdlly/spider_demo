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
        self.conn = pymysql.connect(self.mysql_host, self.mysql_user, self.mysql_passwd, self.mysql_db,
                                    charset='utf8mb4', )
        self.cur = self.conn.cursor()

        # 打开数据库连接

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),  # 从 settings.py 提取
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_passwd=crawler.settings.get('MYSQL_PASSWD'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # print("========================================================")
        if isinstance(item, items.Recipes):
            table = "recipes"
        elif isinstance(item, items.SchoolInfo):
            table = "school_info"
        elif isinstance(item, items.PlayerUp):
            table = "player_up"
        elif isinstance(item, items.DuoKanItem):
            table = "book_desc"
        else:
            table = ""

        cols = ', '.join(item.keys())
        values = ', '.join(['%s'] * len(item.keys()))
        insert_sql = "replace into {table} ({cols}) values ({values})".format(table=table, cols=cols, values=values)
        # print(insert_sql)
        self.cur.execute(insert_sql, tuple(item.values()))
        self.conn.commit()
        return item
