# coding:utf-8

import tornado.wsgi
import sae
import hashlib
import time
from xml.etree import ElementTree as ET


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world! - Tornado")

class WeChatHandler(tornado.web.RequestHandler):
    def get(self):
        token = "TZ5x85EbCyeFbhZrHsJbw4YQjFusP6Q07xenAiq1aTKb2wxVh9Y9Au0JXpIWk__SjdNyp1QTtKaNfCj-EuqnwA"
        echostr = self.get_argument("echostr", "", True)
        timestamp = self.get_argument("timestamp", "", True)
        nonce = self.get_argument("nonce", "", True)
        signature = self.get_argument("signature", "", True)
        args = [token, timestamp,nonce]
        args.sort()
        if hashlib.sha1("".join(args)).hexdigest() == signature:
            if echostr:
                self.write(echostr)
	else:
	    self.write('fail')

    def post(self):
        body = self.request.body
        data = ET.fromstring(body)
        tousername = data.find('ToUserName').text
        fromusername = data.find('FromUserName').text
        createtime = data.find('CreateTime').text
        msgtype = data.find('MsgType').text
        content = data.find('Content').text
        msgid = data.find('MsgId').text
        result = 'welcome pixomondo pipeline test'
        if content.strip() in ('ls','pwd','w','uptime'):
             result = 'ni shi shui'
        textTpl = """<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[%s]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>"""
        out = textTpl % (fromusername, tousername, str(int(time.time())), msgtype, result)
        self.write(out)

app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/weixin", WeChatHandler),
])

application = sae.create_wsgi_app(app)


'''
just test
'''