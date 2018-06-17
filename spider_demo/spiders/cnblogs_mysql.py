# -*- coding: utf-8 -*-

import scrapy

import sys


# reload(sys)
# sys.setdefaultencoding("utf8")


class CnblogsMySQL(scrapy.Spider):
    # 爬虫的名字，必须有这个变量
    name = 'cnblogs_mysql'

    page_index = 1

    # 初始地址，必须有这个变量
    start_urls = ["https://www.ownedcore.com/forums/mmo-trading-market/"]

    def parse(self, response):

        post_items = response.xpath(
            "//div[@id='wrapper']/div[@id='main']/div[@id='post_list']/div[@class='post_item']/div[@class='post_item_body']"
        )

        for post_item_body in post_items:
            yield {
                'article_title':
                    post_item_body.xpath("h3/a/text()").extract_first().strip(),
                'article_summary':
                    post_item_body.xpath("p[@class='post_item_summary']/text()").extract_first().strip(),
                'post_date':
                    post_item_body.xpath("div[@class='post_item_foot']/text()").extract()[1].strip(),
                'article_view':
                    post_item_body.xpath(
                        "div[@class='post_item_foot']/span[@class='article_view']/a/text()"
                    ).extract_first().strip()
            }

        self.page_index += 1
        if self.page_index <= 20:
            next_page_url = "https://www.cnblogs.com/cate/mysql/" + str(self.page_index)
        else:
            next_page_url = None

        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
