#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- coding: utf-8 -*-
import smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate

def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def send(from_addr, to_addr, msg):
    # SMTPの引数を省略した場合はlocalhost:25
    s = smtplib.SMTP()
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.close()

def send_via_gmail(from_addr, to_addr, msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('yourname@gmail.com', 'password')
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.close()

if __name__ == '__main__':
    from_addr = 'spam@example.com'
    to_addr = 'egg@example.com'
    msg = create_message(from_addr, to_addr, 'test subject', 'test body')
    send(from_addr, to_addr, msg)
    send_via_gmail(from_addr, to_addr, msg)

