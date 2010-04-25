#!/usr/bin/env python
# -*- coding:utf-8 -*-
import codecs
import imp
import os
import smtplib
import sys
from email.Header import Header
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def makemail(from_addr, to_addrs, subject, body):
    """ 送信元、送信先(リスト)、件名、本文を渡してMessageオブジェクトを作る
    """
    msg = MIMEMultipart()                     # Messageオブジェクトを作る
    subject = subject.encode("iso-2022-jp")   # 件名をエンコードする
    msg["Subject"] = Header(subject,"iso-2022-jp")    # ヘッダに設定
    msg["From"] = from_addr                   # 送信元をヘッダに設定
    msg["To"] = ', '.join(to_addrs)           # 送信先をヘッダに設定
    mainpart = MIMEText("",_charset="iso-2022-jp")    # テキストのパートを作る
    mainpart.set_payload(body.encode("iso-2022-jp"))  # 本文を設定
    msg.attach(mainpart)                      # Messageオブジェクトに追加
    
    return msg

def makebody(file, macros):
    uf = codecs.open(file, "r", "utf-8")
    s = uf.read()
    
    # マクロのparse処理
    
    # マクロのインスタンス化
    # if macros[name] == 'module':
    #    ins = getattr(macros[MacroName.lower()], 'MacroName')()
    #    mocros[name] = ins
    
    # マクロの実行結果
    # result = macros[name].execute(args)
    
    # マクロの部分をresultで置換
    
    return s

def loadmacros():
    sys.path.append('./macro')
    macros = {}
    
    files = os.listdir('./macro')
    for file in files:
        name, ext = os.path.splitext(file)
        if ext == '.py':
            macros[name] = imp.load_source(name, file)

    return macros

def send(msg):
    host = "host.to.smtp"
    from_addr = "someone@mailhost.com"
    to_addrs = ["some@mail.addr", "some2@mail.addr"]
    
    s = smtplib.SMTP(host)
    s.sendmail(from_addr, to_addrs, msg.as_string())
    s.quit()

if __name__ == "__main__":
    from_addr = "someone@mailhost.com"
    to_addrs = ["some@mail.addr", "some2@mail.addr"]
    subject = u"日本語を含むmailの件名"
    
    macros = loadmacros()
    body = makebody('body.txt', macros)
    
    msg = makemail(from_addr, to_addrs, subject, body)
    
    send(msg)
