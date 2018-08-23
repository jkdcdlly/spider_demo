# -*- coding: utf-8 -*-
import uuid
import scrapy
import spider_demo.items as items
from spider_demo import emailSender
import datetime
from scrapy.mail import MailSender


class epicnpcSpider(scrapy.Spider):
    name = 'epicnpc'
    allowed_domains = ['www.epicnpc.com']
    start_urls = ['https://www.epicnpc.com/forumlist.php']

    def start_requests(self):
        emailSenderClient = emailSender.emailSender()
        toSendEmailLst = ['chenzl@bbtree.com']
        params = {"startTime": datetime.datetime.now(), "name": "epicnpc"}
        subject = "爬虫启动状态汇报：name = {name}, startTime = {startTime}".format(**params)
        body = "细节：start successs! name = {name},at:{startTime}".format(**params)
        emailSenderClient.sendEmail(toSendEmailLst, subject, body)  # 发送邮件
        yield scrapy.Request(url="https://www.epicnpc.com/forumlist.php", callback=self.parse)

    # def start_requests(self):
    #     mailer = MailSender()
    #     mailer.send(to=["chenzl@bbtree.com"], subject="Some subject", body="Some body")
    # 解析首页
    def parse(self, response):
        links = response.xpath('//*[@id="charnav"]//a/@href').extract()
        for link in links:  # 循环 a-z
            yield scrapy.Request(self.trim_url(link), callback=self.parse_2)

    def parse_2(self, response):
        links = response.xpath('//*[@id="forumlist_alphabet_wrapper"]//a')
        for link in links:  # 循环游戏名
            game_name = link.xpath("text()").extract_first()
            url = link.xpath("@href").extract_first()
            yield scrapy.Request(self.trim_url(url), callback=self.parse_3, meta={
                "game_name": game_name
            })

    def parse_3(self, response):
        threads = response.xpath('//*[@id="threads"]//h3[@class="threadtitle"]/a')
        item = items.ListItem()
        for thread in threads:
            url = thread.xpath("@href").extract_first()
            item["url"] = self.trim_url(url)
            item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, item["url"]))
            item["title"] = thread.xpath("text()").extract_first()
            item["game_name"] = response.meta['game_name']
            item["trade_type"] = "Account Trade"

            yield item
            yield scrapy.Request(item["url"], callback=self.parse_detail, meta={
                "title": item["title"],
                "game_name": response.meta['game_name']
            })

    def parse_detail(self, response):
        item = items.DetailItem()
        url = response.url
        item["url"] = self.trim_url(url)  # 不用改
        item["id"] = str(uuid.uuid3(uuid.NAMESPACE_DNS, item["url"]))  # 不用改
        item["title"] = response.meta["title"]  # 不用改
        mate_desc = response.xpath("//meta[@name='description']/@content").extract_first()  # 不用改
        item["mate_desc"] = '' if mate_desc is None else mate_desc  # 不用改
        mate_key = response.xpath("//meta[@name='keywords']/@content").extract_first()  # 不用改
        item["mate_key"] = '' if mate_key is None else mate_key  # 不用改
        item["postList_id"] = item["id"]  # 不用改
        item["game_name"] = response.meta['game_name']  # 不用改
        item["trade_type"] = "Account Trade"  # 不用改
        table = response.xpath('//div[contains(@id,"post_message_")]')[0]
        item["post_detail"] = table.extract()
        yield item

    def closed(self, reason):  # 爬取结束的时候发送邮件
        emailSenderClient = emailSender.emailSender()
        toSendEmailLst = ['chenzl@bbtree.com']
        params = {"finishTime": datetime.datetime.now(), "reason": reason}
        subject = "爬虫结束状态汇报：name = baidu, finishedTime = {finishTime}".format(finishTime=datetime.datetime.now())
        body = "细节：reason = {reason}, successs! at:{finishTime}".format(**params)
        emailSenderClient.sendEmail(toSendEmailLst, subject, body)

    def error(self, failure):
        emailSenderClient = emailSender.emailSender()
        toSendEmailLst = ['chenzl@bbtree.com']
        params = {"finishTime": datetime.datetime.now(), "failure": failure}
        subject = "爬虫结束状态汇报：name = baidu, finishedTime = {finishTime}".format(finishTime=datetime.datetime.now())
        body = "细节：failure = {failure}, failure! at:{finishTime}".format(**params)
        emailSenderClient.sendEmail(toSendEmailLst, subject, body)

    def trim_url(self, url):
        if not url.startswith("https://www.epicnpc.com/"):
            url = 'https://www.epicnpc.com/' + url
        bodys = url.split("?")
        if len(bodys) < 2:
            return url
        params = []
        for param in bodys[1].split("&"):
            if param.startswith("s="):
                continue
            params.append(param)
        return bodys[0] + "?" + "&".join(params)
