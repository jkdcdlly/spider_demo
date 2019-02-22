# -*- coding: utf-8 -*-
import scrapy

import spider_demo.items as items
import datetime
from spider_demo import emailSender


class IReadWeekSpider(scrapy.Spider):
    name = 'ireadweek'
    allowed_domains = ['www.ireadweek.com']
    start_urls = ['http://www.ireadweek.com/']
    SITE_URL = 'http://www.ireadweek.com'

    def start_requests(self):
        """
        1、爬虫启动时发送邮件
        2、遍历分页
        :return:
        """
        params = {"startTime": datetime.datetime.now(), "name": self.name}
        subject = "爬虫启动状态汇报：name = {name}, startTime = {startTime}".format(**params)
        body = "细节：start successs! name = {name},at:{startTime}".format(**params)
        emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)  # 首页

    def parse(self, response):
        for i in range(1, 252):
            url = "http://www.ireadweek.com/index.php/index/{page_num}.html".format(page_num=i)
            # print(url)
            yield scrapy.Request(url, callback=self.parse_list)
            # break

    def parse_list(self, response):
        detail_urls = response.xpath('/html/body/div/div/ul/a/@href').extract()
        for detail_url in detail_urls:
            # print(detail_url)
            yield scrapy.Request("http://www.ireadweek.com" + detail_url, callback=self.parse_detail)
            # break

    def parse_detail(self, response):
        book_url = response.url
        book_title = response.xpath('//div[@class="hanghang-za-title"]/text()').extract_first()
        book_img = "http://www.ireadweek.com" + response.xpath(
            '/html/body/div/div/div[1]/div[2]/div[1]/img/@src').extract_first()
        # print(book_img)

        book_grade = 10
        book_score = 10
        book_rating = 100
        new_price = 0
        old_price = 10
        book_translator = ''
        book_author = response.xpath('/html/body/div/div/div[1]/div[2]/div[2]/p[1]/text()').extract_first().replace(
            "作者：", "")
        book_copyright = ''
        book_datePublished = ''
        book_catalogue = response.xpath('/html/body/div/div/div[1]/div[7]').extract_first()
        book_content = response.xpath('/html/body/div/div/div[1]/div[2]/div[2]/p[5]').extract_first()
        if len(book_content.strip()) == 7:
            book_content = response.xpath('/html/body/div/div/div[1]/div[2]/div[2]/p[6]').extract_first()

        keywords = response.xpath('/html/head/meta[@name="keywords"]/@content').extract_first()
        description = response.xpath('/html/head/meta[@name="description"]/@content').extract_first()
        classify = response.xpath('/html/body/div/div/div[1]/div[2]/div[2]/p[2]/text()').extract_first().replace(
            "分类：", "")
        down_url = response.xpath('/html/body/div/div/div[1]/div[3]/div[1]/a/@href').extract_first()
        item = items.IReadWeekItem()

        item['book_id'] = None
        item['book_url'] = book_url
        item['book_img'] = book_img
        item['book_title'] = book_title.replace("&", "+")
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
        item['down_url'] = down_url
        item['is_enable']=True
        yield item

    # alter table book_desc add column down_url varchar(100) default '';
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
        emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件

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
        emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件
