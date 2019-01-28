# -*- coding: utf-8 -*-
import uuid
import scrapy
import spider_demo.items as items
from spider_demo import EmailSender
import datetime


class PeasAndCrayons(scrapy.Spider):
    name = 'peasandcrayons'  # 爬虫名称
    allowed_domains = ['peasandcrayons.com']  # 域名
    start_urls = ['https://peasandcrayons.com/recipes']  # 开始URL
    url_model = "https://peasandcrayons.com/recipes/page/{page_num}"  # 分页

    # 列表页
    items_xpath = '//main[@id="main"]//article'  # items
    items_a_xpath = "div[1]/a/@href"  # a 链接

    # 详情页
    post_title_xpath = '//main//h1[@class="entry-title"]//text()'  # title
    post_cate_xpath = '//main/article/div[1]//text()'  # cate
    post_img_xpath = '//main//div[@class="entry-content"]//img/@src'  # img
    post_content_xpath = '//main//div[@class="entry-content"]'  # content

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
        for i in range(0, 45):
            paging_url = self.url_model.format(page_num=str(i + 1))
            meta = {"paging_url": paging_url}
            yield scrapy.Request(url=paging_url, callback=self.parse, meta=meta)

    def parse(self, response):
        """
        抓取列表页
        :param response:
        :return:
        """
        for item in response.xpath(self.items_xpath):
            a = item.xpath(self.items_a_xpath).extract_first()
            yield scrapy.Request(a, callback=self.parse_post)

    def parse_post(self, response):
        """
        抓取详情页
        :param response:
        :return:
        """
        item = items.Recipes()
        item["origin_url"] = response.url
        item["title"] = response.xpath(self.post_title_xpath).extract_first()
        item["cate"] = response.xpath(self.post_cate_xpath).extract_first()
        item["imgs"] = ",".join(response.xpath(self.post_img_xpath).extract())
        item["content"] = response.xpath(self.post_content_xpath).extract_first()
        # item["mate_desc"] = response.xpath("//meta[@name='description']/@content").extract_first()
        yield item


def closed(reason):
    """
    爬取结束的时候发送邮件
    :param reason:
    :return:
    """
    params = {"finishTime": datetime.datetime.now(), "reason": reason}
    subject = "爬虫结束状态汇报：name = baidu, finishedTime = {finishTime}".format(finishTime=datetime.datetime.now())
    body = "细节：reason = {reason}, successs! at:{finishTime}".format(**params)
    EmailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件


def error(failure):
    """
    爬取错误的时候发送邮件
    :param failure:
    :return:
    """
    params = {"finishTime": datetime.datetime.now(), "failure": failure}
    subject = "爬虫结束状态汇报：name = baidu, finishedTime = {finishTime}".format(finishTime=datetime.datetime.now())
    body = "细节：failure = {failure}, failure! at:{finishTime}".format(**params)
    EmailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件
