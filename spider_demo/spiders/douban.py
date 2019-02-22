# -*- coding: utf-8 -*-
import scrapy
import random
import spider_demo.items as items
import datetime
from spider_demo import emailSender


class DouBanBookSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-all']

    def start_requests(self):
        """
        1、爬虫启动时发送邮件
        2、遍历分页
        :return:
        """
        params = {"startTime": datetime.datetime.now(), "name": self.name}
        subject = "爬虫启动状态汇报：name = {name}, startTime = {startTime}".format(**params)
        body = "细节：start successs! name = {name},at:{startTime}".format(**params)
        # emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)  # 首页

    def parse(self, response):
        self.log(' ================' + str(response.request.headers['User-Agent']) + ' ================')
        lis_text = response.xpath('//*[@id="content"]/div/div[1]/div[2]/div/table/tbody/tr/td/a/text()').extract()
        lis_href = response.xpath('//*[@id="content"]/div/div[1]/div[2]/div/table/tbody/tr/td/a/@href').extract()
        for i in range(1, len(lis_text)):
            # print(' ================' + "https://book.douban.com" + lis_href[i] + ' ================')
            yield scrapy.Request("https://book.douban.com" + lis_href[i],
                                 callback=self.parse_list,
                                 meta={'classify': lis_text[i]}
                                 )
            # break

    #
    def parse_list(self, response):
        # print(' ================' + str(response.url) + ' ================')
        ahrefs = response.xpath('//*[@id="subject_list"]/ul/li/div[1]/a/@href').extract()
        for ahref in ahrefs:
            yield scrapy.Request(ahref, callback=self.parse_detail, meta={'classify': response.meta['classify']})
        next_page = response.xpath('//*[@id="subject_list"]/div[2]/span[@class="next"]/a/@href').extract_first()
        if next_page:
            next_page = "https://book.douban.com" + next_page
            self.log('page_url: %s' % next_page)
            yield scrapy.Request(next_page, callback=self.parse_list, meta={'classify': response.meta['classify']})

    def parse_detail(self, response):
        book_title = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract_first()
        book_author = response.xpath('//*[@id="info"]/a[1]/text()').extract_first()
        book_img = response.xpath('//*[@id="mainpic"]/a/img/@src').extract_first()
        book_content = response.xpath('//*[@id="link-report"]/div').extract_first()
        book_catalogue = response.xpath('//*[@id="dir_6709783_short"]/div').extract_first()
        keywords = response.xpath('/html/head/meta[@name="keywords"]/@content').extract_first()
        description = response.xpath('/html/head/meta[@name="description"]/@content').extract_first()
        classify = response.meta['classify']
        book_translator = ''
        book_copyright = ''
        if not book_copyright:
            book_copyright = ''
        book_datePublished = ''
        book_rating = ''
        new_price = '限时免费'
        old_price = random.randint(1, 100)
        book_score = response.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()').extract_first()
        try:
            book_grade = round(float(book_score))
        except:
            book_grade = 6

        item = items.DuoKanItem()
        item['book_id'] = None
        item['book_url'] = response.url
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
        # emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件

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
        # emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件
