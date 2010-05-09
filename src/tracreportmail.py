#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- coding: utf-8 -*-
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

def create_message(from_addr, to_addrs, subject, body, encoding):
    # 'text/plain; charset="encoding"'というMIME文書を作ります
    msg = MIMEText(body.encode(encoding), 'plain', encoding)
    msg['Subject'] = Header(subject.encode(encoding), encoding)
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    msg['Date'] = formatdate()
    return msg

def send(from_addr, to_addrs, msg):
    # SMTPの引数を省略した場合はlocalhost:25
    s = smtplib.SMTP()
    s.sendmail(from_addr, to_addrs, msg.as_string())
    s.close()

def send_via_gmail(from_addr, to_addrs, msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('yourname@gmail.com', 'password')
    s.sendmail(from_addr, to_addrs, msg.as_string())
    s.close()

def create_tasks(server, query):
    tasks = []
    
    ids = server.ticket.query(query)
    for id in ids:
        ticket = server.ticket.get(id)
        task = ticket[3] # ticket[3]はチケットのフィールド値
        
        # idとcommentはticket[3]に含まれていないため、追加する
        task['id'] = id
        for changes in server.ticket.changeLog(id):
            if changes[2] == 'comment':
                task['comment'] = changes[4].encode('utf-8')
        
        tasks.append(task)
    
    return tasks

def read_templete():
    body = u""

    return body

if __name__ == '__main__':
    from_addr = 'spam@example.com'
    to_addrs = ['egg@examplex.com']
    msg = create_message(from_addr, to_addrs, u'テスト', u'本文', 'ISO-2022-JP')
    send(from_addr, to_addrs, msg)
    send_via_gmail(from_addr, to_addrs, msg)

