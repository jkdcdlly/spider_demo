# -*- coding: utf-8 -*-
import uuid
import scrapy
import spider_demo.items as items
from spider_demo import emailSender
import datetime


class Bakerbynature(scrapy.Spider):
    name = 'bakerbynature'  # 爬虫名称
    allowed_domains = ['bakerbynature.com']  # 域名
    start_urls = ['https://bakerbynature.com/recipe-index/']  # 开始URL
    # url_model = "https://bakerbynature.com/category/{category}/page/{page_num}"  # 分页

    # # 列表页
    # items_xpath = '//main[@id="main"]//article'  # items
    # items_a_xpath = "div[1]/a/@href"  # a 链接
    #
    # # 详情页
    # post_title_xpath = '//main//h1[@class="entry-title"]//text()'  # title
    # post_cate_xpath = '//main/article/div[1]//text()'  # cate
    # post_img_xpath = '//main//div[@class="entry-content"]//img/@src'  # img
    # post_content_xpath = '//main//div[@class="entry-content"]'  # content

    def start_requests(self):
        """
        该方法不用动
        1、爬虫启动时发送邮件
        2、遍历分页
        :return:
        """
        params = {"startTime": datetime.datetime.now(), "name": self.name}
        subject = "爬虫启动状态汇报：name = {name}, startTime = {startTime}".format(**params)
        body = "细节：start successs! name = {name},at:{startTime}".format(**params)
        emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        """
        抓取所有分类的链接
        :param response:
        :return:
        """
        # 从这里开始写
        cate_xpath = '//*[@id="categories-3"]/div/ul//a'
        item_list = response.xpath(cate_xpath)
        url_list = item_list.xpath("@href").extract()
        text_list = item_list.xpath("text()").extract()
        for i in range(0, len(url_list) - 1):
            url = url_list[i]
            text = text_list[i]
            print(text," : ",url)
            yield scrapy.Request(url, callback=self.parse_page, meta={"cate": text})

    def parse_page(self, response):
        """
        抓取所有文章的链接
        :param response:
        :return:
        """
        page_url_xpath = '//*[@id="genesis-content"]/article/header/h2/a/@href'
        url_list = response.xpath(page_url_xpath).extract()
        for url in url_list:
            # print("url : ",url)
            yield scrapy.Request(url, callback=self.parse_post, meta={"cate": response.meta['cate']})
        next_xpath = '//*[@class="pagination-next"]/a/@href'
        next_url = response.xpath(next_xpath).extract_first()
        if next_url is not None:
            # print("next_url : ",next_url)
            yield scrapy.Request(next_url, callback=self.parse_page, meta={"cate": response.meta['cate']})

    def parse_post(self, response):
        """
        抓取详情页
        :param response:
        :return:
        """
        item = items.Recipes()
        item["origin_url"] = response.url
        item["title"] = response.xpath('//*[@id="genesis-content"]/article/header/h1/text()').extract_first()
        item["cate"] = response.meta['cate']
        item["imgs"] = ",".join(response.xpath('//*[@id="genesis-content"]/article/div//img/@src').extract())
        item["content"] = response.xpath('//*[@id="genesis-content"]/article/div').extract_first()
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
    emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件


def error(failure):
    """
    爬取错误的时候发送邮件
    :param failure:
    :return:
    """
    params = {"finishTime": datetime.datetime.now(), "failure": failure}
    subject = "爬虫结束状态汇报：name = baidu, finishedTime = {finishTime}".format(finishTime=datetime.datetime.now())
    body = "细节：failure = {failure}, failure! at:{finishTime}".format(**params)
    emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件
