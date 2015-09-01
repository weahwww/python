#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'weahwww'

import os
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from tornado.httpclient import HTTPClient
import smtplib
from email.mime.text import MIMEText


email_host = 'smtp.163.com' #发件邮箱SMTP
email_user = 'nanjingquxun'      #发件邮箱用户名
email_pwd = 'gkcceykhydusgkyz'      #发件邮箱密码
email_postfix = '163.com'   #发件邮箱后缀

#收件邮件地址
mailto_list = [
    '576296668@qq.com',     #熊冬根
    '2725686588@qq.com',    #羊笑佺
]


config = dict(
    username="pinpiao",
    password="123456",
    mobile='13913308819',
    diskspace=30,
    period=1 * 60 * 60 # 定时:小时 分钟 秒,默认1小时
)

return_values = {
    "00": "多个手机号请求发送成功",
    "02": "IP 限制",
    "03": "单个手机号请求发送成功",
    "04": "用户名错误",
    "05": "密码错误",
    "06": "编码错误",
    "07": "发送时间有误",
    "08": "参数错误",
    "09": "手机号码有误",
    "10": "扩展号码有误",
    "11": "余额不足",
    "-1": "服务器内部异常",
    "REJECT": "非法消息内容",
    }
success_code = "03"


def sendmail(mailto_list, sub, content):
    me = 'QXserver'+'<'+email_user+'@'+email_postfix+'>'
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(mailto_list)
    try:
        server = smtplib.SMTP(email_host)
        server.connect(email_host)
        server.login(email_user, email_pwd)
        server.sendmail(me, mailto_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        return False


def message_post(mobile, content):
    result = False
    resultStr = "未知的内部错误"

    # print("准备发送 mobile = {mobile}  data_plan={data_plan} expiry_time={expiry_time}".format(mobile=mobile, data_plan=data_plan,expiry_time=expiry_time))
    http_client = HTTPClient()
    try:
        body_template = "UserName={username}&UserPass={userpass}&Subid={subid}&Mobile={mobile}&Content={content}"
        body = body_template.format(username=config['username'], userpass=config['password'], subid="", mobile=mobile, content=content)
        response = http_client.fetch("http://114.215.130.61:8082/SendMT/SendMessage", method="POST", body=body)
        if response.code == 200:
            responselist = response.body.decode().strip().split(',')
            result_code = responselist[0]

            if result_code == success_code:
                result = True
                resultStr = "发送成功 mobile = {mobile}  id = {messageid}".format(mobile=mobile, messageid=responselist[1])
                print(resultStr)
            else:
                result = False
                if result_code in return_values:
                    resultStr = return_values[result_code]
                else:
                    resultStr += ("(" + result_code + ")")

                print("发送失败 mobile = {mobile}  errcode={code} errstr={errstr}".format(mobile=mobile, code=result_code,errstr=resultStr))

        else:
            resultStr += (",http返回码({0})".format(response.code) )
            print("Send message get a unknown http response code = {0}".format(response.code))

    except Exception as e:
        resultStr += " 出现了异常"
        print("Send message catch a exception:", e)
    finally:
        http_client.close()

def tick():
    # 用'df'命令获取磁盘'/'信息
    vfs = os.popen("df /").readlines()

    # 获取磁盘占用率并去除'%'
    data = vfs[1].split()[4].split("%")

    # 判断
    if int(data[0]) >= config['diskspace']:
        date_time = datetime.now()
        time = date_time.strftime('%y-%m-%d %I:%M:%S %p')
        data = data[0]
        content_template = "{time}，服务器空间不足，还剩百分之{data}"
        content = content_template.format(time=time, data=data)
        print(content)
        mobile = config['mobile']
        sendmail(mailto_list, '服务器磁盘空间不足', content)
        message_post(mobile, content)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=config['period'])
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()