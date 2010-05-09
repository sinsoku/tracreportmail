#!/usr/local/bin/python
# -*- encoding: utf-8 -*-

import os
import xmlrpclib
from urllib import splituser, splitpasswd
from urllib2 import urlparse
import socket
import md5
import random

"""
import urllib2
toplevelurl='x68000.q-e-d.net'
theurl='x68000.q-e-d.net/~68user/net/sample/http-auth-digest/secret.html'
protocol='http://'
username='hoge'
password='fuga'
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, toplevelurl, username, password)
authhandler = urllib2.HTTPDigestAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
pagehandle = opener.open(protocol + theurl)
"""

class CustomTransport(xmlrpclib.Transport):
  proxy_keys = dict(HTTP_PROXY='http',HTTPS_PROXY='https')
  #_use_datetime = True
  def __init__(self, proxies={}, local=False):
    xmlrpclib.Transport.__init__(self)
    self.proxies = dict((      (self.proxy_keys[k],v)      for k,v in os.environ.items()      if k in self.proxy_keys    ))
    self.proxies.update(proxies)
    self.local = local
    self.auth = ''
    self.nc = 0

  def make_connection(self, host):
    self.user_pass, self.realhost = splituser(host)
    import httplib
    proto, proxy, p1,p2,p3,p4 = urlparse.urlparse(self.proxies.get('http', ''))
    if proxy and not self.local:
      return httplib.HTTP(proxy)
    else:
      return httplib.HTTP(self.realhost)

  def send_request(self, connection, handler, request_body):
    #connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler))
    connection.putrequest("POST", handler)

  def request(self, host, handler, request_body, verbose=0):
    for count in range(3):
      try:
        return xmlrpclib.Transport.request(self, host, handler, request_body, verbose)
      except xmlrpclib.ProtocolError, ex:
        if ex.errcode==401:
          auth, params = ex.headers['WWW-Authenticate'].split(' ', 1)
          self.uri = handler
          self.auth = auth.lower()
          self.params = dict([
            [n.strip() for n in i.split('=',1)]            for i in params.split(',')])
    raise ex

  def send_host(self, connection, host):
    connection.putheader('Host', self.realhost)
    if self.auth=='basic':
      if self.user_pass:
        import base64
        user_pass = base64.encodestring(self.user_pass).strip()
        connection.putheader('Authorization', 'Basic %s' % user_pass)
    elif self.auth=='digest':
      if self.user_pass:
        self.nc += 1
        username, password = self.user_pass.split(':')
        uri = self.uri
        realm = self.params['realm'].strip('"')
        nonce = self.params['nonce'].strip('"')
        qop = self.params['qop'].strip('"')
        a1 = md5.new('%(username)s:%(realm)s:%(password)s' % locals()).hexdigest()
        a2 = md5.new('POST:%(uri)s' % locals()).hexdigest()
        nc = '%08d' % self.nc
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        cnonce = ''.join([random.choice(chars) for i in range(16)])
        response = md5.new('%(a1)s:%(nonce)s:%(nc)s:%(cnonce)s:%(qop)s:%(a2)s' % locals()).hexdigest()
        print >>open('log.txt','a'), locals()
        params = []
        params.append('username=%s' % username)
        params.append('realm="%s"' % realm)
        params.append('nonce="%s"' % nonce)
        params.append('uri=%s' % uri)
        params.append('algorithm=%s' % self.params['algorithm'])
        params.append('qop=%s' % qop)
        params.append('nc=%s' % nc)
        params.append('cnonce="%s"' % cnonce)
        params.append('response="%s"' % response)
        for i in params:
          print >>open('log.txt','a'), i
        connection.putheader('Authorization', 'Digest %s' % ', '.join(params))

class XmlRpcServer(xmlrpclib.ServerProxy):
  def __init__(self, url, user='', password='', local=False):
    protocol,domain,path, d1,params,d3 = urlparse.urlparse(url)
    if params:
      params = '?'+params
    user_pass = ''
    if user:
      user_pass = ':'.join([user,password]) + '@'
    href = '%(protocol)s://%(user_pass)s%(domain)s%(path)s%(params)s' % locals()
    xmlrpclib.ServerProxy.__init__(
      self, href, transport=CustomTransport(local=local), allow_none=True)

if __name__=='__main__':
  server = XmlRpcServer('http://example.org/RPC2','hoge','fuga')
  print server.system.listMethods()
