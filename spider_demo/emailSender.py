# -*- coding: utf-8 -*-
# 添加文件 emailSender.py
import smtplib
from email.mime.text import MIMEText


class EmailSender(object):
    def __init__(self):
        self.smtp_host = "smtp.exmail.qq.com"  # 发送邮件的smtp服务器（从QQ邮箱中取得）
        self.smtp_user = "data@bbtree.com"  # 用于登录smtp服务器的用户名，也就是发送者的邮箱
        self.smtp_pwd = "Zhs@2018"  # 授权码，和用户名user一起，用于登录smtp， 非邮箱密码
        self.smtp_port = 465  # smtp服务器SSL端口号，默认是465
        self.sender = "data@bbtree.com"  # 发送方的邮箱

    def send_email(self, subject, body, to_list=None):
        """
        发送邮件
        :param to_list: 收件人的邮箱列表["465482631@qq.com", "77789713@qq.com"]
        :param subject: 邮件标题
        :param body: 邮件内容
        :return:
        """
        if to_list is None:
            to_list = ['chenzl@bbtree.com']
        message = MIMEText(body, 'plain', 'utf-8')  # 邮件内容，格式，编码
        message['From'] = self.sender  # 发件人
        message['To'] = ",".join(to_list)  # 收件人列表
        message['Subject'] = subject  # 邮件标题
        try:
            smtp_ssl_client = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)  # 实例化一个SMTP_SSL对象
            login_res = smtp_ssl_client.login(self.smtp_user, self.smtp_pwd)  # 登录smtp服务器
            print("登录结果：loginRes = {loginRes}".format(loginRes=login_res))
            if login_res and login_res[0] == 235:
                print("登录成功，code = {code}".format(code=login_res[0]))
                smtp_ssl_client.sendmail(self.sender, to_list, message.as_string())
                print("mail has been send successfully. message:{message}".format(message=message.as_string()))
            else:
                print("登陆失败，code = {code}".format(code=login_res[0]))
        except Exception as e:
            print("发送失败，Exception: e={e}".format(e=e))
