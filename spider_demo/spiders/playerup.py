# -*- coding: utf-8 -*-
import uuid
import scrapy
import spider_demo.items as items
from spider_demo import emailSender
import datetime


class PeasAndCrayons(scrapy.Spider):
    name = 'playerup'  # 爬虫名称
    allowed_domains = ['www.playerup.com']  # 域名
    start_urls = ['https://www.playerup.com/']  # 开始URL

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
        """
        抓取首页
        :param response:
        :return:
        """
        title_items = response.xpath('//*[@id="main-marketplaces.1"]/ol/li/div/div/h3/a')
        title_items.extend(response.xpath('//*[@id="featured-marketplaces.960"]/ol/li/div/div/h3/a'))
        for i in range(0, len(title_items) - 1):
            if 2 < i < 11:
                title_item = title_items[i]
                title = title_item.xpath("text()").extract_first()
                href = title_item.xpath("@href").extract_first()
                meta = {"title1": title}
                # print("parse===========================>>>>>>>>>>>", self.start_urls[0] + href)
                yield scrapy.Request(self.start_urls[0] + href, callback=self.parse_cate_page, meta=meta)
                # break

    def parse_cate_page(self, response):
        """
        爬虫分类页
        :param response:
        :return:
        """
        title1 = response.meta["title1"]
        title_items = response.xpath('//*[@id="forums"]/li/div/div/h3/a')
        for title_item in title_items:
            title = title_item.xpath("text()").extract_first()
            href = title_item.xpath("@href").extract_first()
            meta = {"title1": title1, "title2": title}
            # print("parse_cate_page===========================>>>>>>>>>>>", self.start_urls[0] + href)
            yield scrapy.Request(self.start_urls[0] + href, callback=self.parse_page_num, meta=meta)
            # break

    def parse_page_num(self, response):
        """
        爬虫列表分页
        :param response:
        :return:
        """
        url = response.url
        page_text = response.xpath(
            '//*[@id="content"]//div[@class="pageNavLinkGroup fc_top_pagenav"]//span/text()').extract_first()
        page_num = 1
        if page_text is not None:
            text_arr = page_text.split(" ")
            page_num = int(text_arr[3])
        # print("页数为:--------", page_num)
        for i in range(1, page_num + 1):
            href = "{url}page-{page_num}".format(url=url, page_num=i)
            # print("parse_page_num===========================>>>>>>>>>>>", href)
            yield scrapy.Request(href, callback=self.parse_list_page, meta=response.meta)
            # break

    def parse_list_page(self, response):
        """
        爬虫列表页
        :param response:
        :return:
        """
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>进入parse_list_page>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        title1 = response.meta["title1"]
        title2 = response.meta["title2"]
        # title_items = response.xpath('//*[@id="content"]//ol//li/div[2]/div/h3/a[5]')
        title_items = response.xpath('//*[@id="content"]//ol//li//a[@class="PreviewTooltip"]')
        # print(">>>>>>>>>>>parse_list_page===========================", len(title_items))
        for title_item in title_items:
            title = title_item.xpath("text()").extract_first()
            href = title_item.xpath("@href").extract_first()
            meta = {"title1": title1, "title2": title2, "title3": title}
            # print("parse_list_page===========================>>>>>>>>>>>", self.start_urls[0] + href)
            yield scrapy.Request(self.start_urls[0] + href, callback=self.parse_detail_page, meta=meta)
            # break

    def parse_detail_page(self, response):
        """
        抓取详情页
        :param response:
        :return:
        """
        item = items.PlayerUp()
        item["cate1_title"] = response.meta["title1"]
        item["cate2_title"] = response.meta["title2"]
        item["detail_title"] = response.meta["title3"]
        item["detail_url"] = response.url
        mate_desc = response.xpath("//meta[@name='description']/@content").extract_first()
        mate_key = response.xpath("//meta[@name='keywords']/@content").extract_first()
        item["mate_desc"] = '' if mate_desc is None else mate_desc
        item["mate_key"] = '' if mate_key is None else mate_key
        item["detail"] = response.xpath('//*[@id="messageList"]').extract_first()
        yield item

    def closed(self, reason):
        """
        爬取结束的时候发送邮件
        :param reason:
        :return:
        """
        params = {"finishTime": datetime.datetime.now(), "reason": reason}
        subject = "爬虫结束状态汇报：name = baidu, finishedTime = {finishTime}".format(finishTime=datetime.datetime.now())
        body = "细节：reason = {reason}, successs! at:{finishTime}".format(**params)
        emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件

    def error(self, failure):
        """
        爬取错误的时候发送邮件
        :param failure:
        :return:
        """
        params = {"finishTime": datetime.datetime.now(), "failure": failure}
        subject = "爬虫结束状态汇报：name = baidu, finishedTime = {finishTime}".format(finishTime=datetime.datetime.now())
        body = "细节：failure = {failure}, failure! at:{finishTime}".format(**params)
        emailSender.EmailSender().send_email(subject=subject, body=body)  # 发送邮件
