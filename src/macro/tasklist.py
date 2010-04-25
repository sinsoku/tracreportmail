#!/usr/bin/env python
# -*- coding:utf-8 -*-
import codecs
import xml_rpc
from macro import Macro

class TaskList(Macro):
    def execute(self, args):
        tasklist = u''
        
        # task.txtからタスク一覧の書式を取得
        file = 'task.txt'
        f = codecs.open(file, "r", "utf-8")
        format = f.read()
        
        # XML-RPCでチケットを取得
        url = 'http://localhost/trac/TracTest/login/xmlrpc'
        user, password = 'admin', 'admin'
        server = xml_rpc.XmlRpcServer(url, user, password)
        
        ids = server.ticket.query(args)
        
        # 全チケットに対してタスク一覧を作成し、
        # tasklistに連結していく。
        for id in ids:
            # チケット情報を取得
            ticket = server.ticket.get(id)[3]
            ticket['id'] = str(id)
            ticket['comment'] = 'a'
            for changes in server.ticket.changeLog(id):
                if changes[2] == 'comment':
                    ticket['comment'] = changes[4].encode('utf-8')
            
            # タスク一覧の書式にチケット情報を設定
            tasklist += format % ticket
        
        return tasklist
        