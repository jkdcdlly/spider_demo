# -*- coding: utf-8 -*-
import uuid
import scrapy
import spider_demo.items as items
from spider_demo import emailSender
import datetime


# def is_blank(x):
#     x = x.replace("\t", "")
#     x = x.replace("\n", "")
#     x = x.replace("\r", "")
#     x = x.replace(" ", "")
#     return x.strip() != ''


class BjdchGov(scrapy.Spider):
    name = 'bjdchgov'  # 爬虫名称
    allowed_domains = ['http://www.bjdch.gov.cn']  # 域名
    start_urls = ['http://www.bjdch.gov.cn/n3952/n382278/n382598/n382975/n384881/index.html']  # 开始URL

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
        列表及链接
        :param response:
        :return:
        """
        # 从这里开始写
        list_xpath = '//*[@id="comp_468290"]/div/div/ul//a'
        item_list = response.xpath(list_xpath)
        for item in item_list:
            url = "http://www.bjdch.gov.cn" + item.xpath("@href").extract_first().split("../../../../..")[1]
            text = item.xpath("text()").extract_first()
            print(url)
            yield scrapy.Request(url, callback=self.parse_post, meta={"cate": text})

    def parse_post(self, response):
        """
        抓取详情页
        :param response:
        :return:
        """
        print("=====================================")
        trs = response.xpath('//*[@id="tax_content"]/table/tbody/tr')

        print(trs[0].xpath('td//text()').extract())
        item = items.SchoolInfo()
        item["school_name"] = "".join(trs[0].xpath('td//text()').extract())
        item["xiaozhang"] = "".join(trs[1].xpath('td//text()').extract())
        item["email"] = "".join(trs[2].xpath('td//text()').extract())
        item["site"] = "".join(trs[3].xpath('td//text()').extract())
        item["cate"] = "".join(trs[4].xpath('td//text()').extract())
        item["type"] = "".join(trs[5].xpath('td//text()').extract())
        item["address"] = "".join(trs[6].xpath('td//text()').extract())
        item["zip"] = "".join(trs[7].xpath('td//text()').extract())
        item["phone"] = "".join(trs[8].xpath('td//text()').extract())
        item["fax"] = "".join(trs[9].xpath('td//text()').extract())
        item["info"] = "".join(trs[10].xpath('td//text()').extract())
        item["mark"] = "".join(trs[11].xpath('td//text()').extract())

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
