# -*- coding: utf-8 -*-
import scrapy

import spider_demo.items as items
import datetime
from spider_demo import EmailSender


class DuoKanBookSpider(scrapy.Spider):
    name = 'duokan'
    allowed_domains = ['www.duokan.com']
    start_urls = ['http://www.duokan.com/']
    SITE_URL = 'http://www.duokan.com'

    def start_requests(self):
        """
        1、爬虫启动时发送邮件
        2、遍历分页
        :return:
        """
        params = {"startTime": datetime.datetime.now(), "name": self.name}
        subject = "爬虫启动状态汇报：name = {name}, startTime = {startTime}".format(**params)
        body = "细节：start successs! name = {name},at:{startTime}".format(**params)
        EmailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)  # 首页

    def parse(self, response):

        # self.log(' ============================================start duokan ...... ...... ...... ......')
        itms = response.xpath('//*[@id="page-duokan-com"]/div/div[1]/div[2]/div/ul/li')

        for itm in itms:
            itm_href = itm.xpath('a/@href').extract_first()
            itm_cate = itm.xpath('a/span[1]/text()').extract_first()
            yield scrapy.Request(self.SITE_URL + itm_href, callback=self.parse_list, meta={
                "itm_cate": itm_cate
            })
            break

    #
    def parse_list(self, response):
        data = response.xpath('//*[@id="book_list"]/text()').extract_first()
        import demjson
        json_arr = demjson.decode(data)
        for js in json_arr:
            yield scrapy.Request(self.SITE_URL + js['url'], callback=self.parse_detail)
            # print(js['title'])
            # print(js['price'])
            # print(js['old_price'])
            # print(js['cover'])
            # print(js['url'])
            # print(js['authors'])
            # break
            # 是否还有下一页，如果有的话，则继续

            # next_pages = response.xpath('//*[@class="next "]/@href').extract_first()
            # if next_pages:
            #     next_page = self.SITE_URL + next_pages
            #     self.log('page_url: %s' % next_page)
            #     yield scrapy.Request(next_page, callback=self.parse_list)

    def parse_detail(self, response):
        book_url = response.url
        book_desc = response.xpath('//*[@id="page-duokan-com"]/div[1]/div[1]/div[2]/div[1]/div')
        book_title = book_desc.xpath('div[1]/div[2]/h3/text()').extract_first()
        book_img = book_desc.xpath('div[1]/div[1]/a/img/@src').extract_first()
        book_grade = book_desc.xpath('div[1]/div[2]/div[1]/div/@class').extract_first()
        book_score = book_desc.xpath('div[1]/div[2]/div[1]/em//text()').extract_first()
        book_rating = book_desc.xpath('div[1]/div[2]/div[1]/span/span/text()').extract_first()
        new_price = book_desc.xpath('div[1]/div[2]/div[2]/div[2]/div[1]/em/text()').extract_first()
        old_price = book_desc.xpath('div[1]/div[2]/div[2]/div[2]/div[1]/i[1]/del/text()').extract_first()
        book_datas = book_desc.xpath('div[1]/div[2]/div[2]/div[1]/table/tr').extract()
        book_translator = ''
        book_author = ''
        book_copyright = ''
        book_datePublished = ''
        if len(book_datas) == 3:
            book_author = book_desc.xpath('div[1]/div[2]/div[2]/div[1]/table/tr[1]/td[2]/a/text()').extract_first()
            book_copyright = book_desc.xpath('div[1]/div[2]/div[2]/div[1]/table/tr[2]/td[2]/a/text()').extract_first()
            book_datePublished = book_desc.xpath('div[1]/div[2]/div[2]/div[1]/table/tr[3]/td[2]/text()').extract_first()
        elif len(book_datas) == 4:
            book_author = book_desc.xpath('div[1]/div[2]/div[2]/div[1]/table/tr[1]/td[2]/a/text()').extract_first()
            book_translator = book_desc.xpath(
                'div[1]/div[2]/div[2]/div[1]/table/tr[2]/td[2]/span/text()').extract_first()
            book_copyright = book_desc.xpath('div[1]/div[2]/div[2]/div[1]/table/tr[3]/td[2]/a/text()').extract_first()
            book_datePublished = book_desc.xpath('div[1]/div[2]/div[2]/div[1]/table/tr[4]/td[2]/text()').extract_first()
        book_catalogue = book_desc.xpath('div[2]/section[2]/article/ol').extract_first()
        book_content = "".join(response.xpath('//*[@id="book-content"]/p/text()').extract())

        keywords = response.xpath('/html/head/meta[@name="keywords"]/@content').extract_first()
        description = response.xpath('/html/head/meta[@name="description"]/@content').extract_first()
        classify = response.xpath('//*[@id="dkclassify"]/text()').extract_first()
        item = items.DuoKanItem()
        item['book_id'] = None
        item['book_url'] = book_url
        item['book_img'] = book_img
        item['book_title'] = book_title
        item['book_author'] = book_author
        item['book_translator'] = book_translator
        item['book_copyright'] = book_copyright
        item['book_datePublished'] = book_datePublished
        item['book_grade'] = book_grade
        item['book_score'] = book_score
        item['book_rating'] = book_rating
        item['new_price'] = new_price
        item['old_price'] = old_price
        item['book_content'] = book_content
        item['book_catalogue'] = book_catalogue
        item['keywords'] = keywords
        item['description'] = description
        item['classify'] = classify.strip()
        yield item

        def closed(self, reason):
            """
            爬取结束的时候发送邮件
            :param reason:
            :return:
            """
            params = {"finishTime": datetime.datetime.now(), "reason": reason}
            subject = "爬虫结束状态汇报：name = {name}, finishedTime = {finishTime}".format(name=self.name,
                                                                                   finishTime=datetime.datetime.now())
            body = "细节：reason = {reason}, successs! at:{finishTime}".format(**params)
            EmailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件

        def error(self, failure):
            """
            爬取错误的时候发送邮件
            :param failure:
            :return:
            """
            params = {"finishTime": datetime.datetime.now(), "failure": failure}
            subject = "爬虫结束状态汇报：name = {name}, finishedTime = {finishTime}".format(name=self.name,
                                                                                   finishTime=datetime.datetime.now())
            body = "细节：failure = {failure}, failure! at:{finishTime}".format(**params)
            EmailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件
