# https://api-prod.wallstreetcn.com/apiv1/content/fabricate-articles?cursor=&accept=article%2Ctopic%2Cnewsroom%2Cnewsrooms%2Cad&channel=global&limit=25
#-*- coding: utf-8 -*-
from scrapy.spider import Spider
from urlparse import urljoin
from scrapy.selector import Selector
from scrapy.http import Request
import time
import json
import re
import sys
from news.DataResource import TransportData
import scrapy
from news.items import NewsItem
reload(sys)
sys.setdefaultencoding('utf8')
class dongfang(Spider):
    name = "dongfangtoutiao"
    start_urls = [
        "https://refreshnews.dftoutiao.com/toutiao_appnew02/newsgzip"
    ]
    DOWNLOAD_DELAY = 0
    count = 0
    appname = "东方头条"
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str,"%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    def parse(self, response):
        types = [
             "guoji",
            "caijing",
             "redian"
                 ]
        pgnum = 1
        idx = 0
        for type in types:
            yield scrapy.FormRequest(
                response.url,
                formdata={
                    "type": type,
                    "startkey": "null",
                    "newkey": "null",
                    "pgnum": str(pgnum),
                    "idx": str(idx),
                    "key": "37691bebb4a7706e",
                    "softtype": "TouTiao",
                    "softname": "DFTTAndroid",
                    "ime": "355456060868994",
                    "appqid": "dftt170925",
                    "apptypeid": "DFTT",
                    "ver": "1.8.2",
                    "os": "Android5.0.2",
                    "ttaccid": "null",
                    "appver": "010802",
                    "deviceid": "3b6b5070d0c2471d",
                    "position": "北京",
                    "iswifi": "wifi",
                    "channellabel": ""
                },
                meta={"type": type, "idx": idx, "pgnum": pgnum},
                callback=self.parse_next
            )
    def parse_next(self,response):
        type = response.meta['type']
        idx = response.meta['idx']
        pgnum = response.meta['pgnum']
        results = json.loads(response.body)
        endkey = results['endkey']
        newkey = results['newkey']
        if newkey:
            newkey = str(newkey)
        else:
            newkey = "null"
        results = results['data']
        if len(results) > 1:
            acceptable_title = []
            for result in results:
                category = response.meta['type']
                publishedDate = result['date']
                print publishedDate
                a = str(publishedDate)
                a = time.strptime(a, "%Y-%m-%d %H:%M")
                author = result['source']
                title = result['topic']
                url = result['url']
                t = int(time.mktime(a))
                if t > self.timeStamp :
                    publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
                    acceptable_title.append(title)
                    yield Request(url, meta={
                    "category": category,
                    "publishedDate": publishedDate,
                    "author": author,
                    "title": title}, callback=self.parse_news)
            pgnum = int(pgnum) + 1
            if type in ["redian"]:
                idx = int(idx) + 20
            else:
                idx = int(idx) + 15
            if len(acceptable_title) > 1:
                yield scrapy.FormRequest(
                    response.url,
                    formdata={
                        "type": type,
                        "startkey": endkey,
                        "newkey": newkey,
                        "pgnum": str(pgnum),
                        "idx": str(idx),
                        "key": "37691bebb4a7706e",
                        "softtype": "TouTiao",
                        "softname": "DFTTAndroid",
                        "ime": "355456060868994",
                        "appqid": "dftt170925",
                        "apptypeid": "DFTT",
                        "ver": "1.8.2",
                        "os": "Android5.0.2",
                        "ttaccid": "null",
                        "appver": "010802",
                        "deviceid": "3b6b5070d0c2471d",
                        "position": "北京",
                        "iswifi": "wifi",
                        "channellabel": ""
                    },
                    meta={"type": type, "idx": idx, "pgnum": pgnum},
                    callback=self.parse_next
                )
    def parse_news(self,response):
        hxs = Selector(response)
        list = hxs.xpath('//div[@class="ctg-content"]//a/@href').extract()
        if list:
            for i in list:
                yield Request(url= i, meta={
                    "publishedDate": response.meta["publishedDate"],
                                       "author":response.meta['author'],
                                       "title": response.meta['title'],
                                       "category": response.meta['category']},
                              callback=self.parse_news)
        describe = ""
        home_url = "http://mini.eastday.com"
        category = response.meta['category']
        author = response.meta['author']
        publishedDate = response.meta['publishedDate']
        crawlTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        pic_url = ""
        pic_more_url = hxs.xpath("//div[@id='content']//img/@src").extract()
        if pic_more_url:
            pic_more_url = set(pic_more_url)
        else:
            pic_more_url = set()
        content = hxs.xpath("//div[@id='content']//text()").extract()
        content = "".join(content)
        content = content.replace("\n","").replace(" ","")
        title1 = hxs.xpath("//div[@id='title']//text()").extract()
        title = ""
        title2 = hxs.xpath("//title/text()").extract()
        if title2:
            title = title2[0]
        elif title1:
            title = title1[0]
        title = title.replace("\n", "").replace(" ", "")
        self.count = self.count + 1
        print self.count
        print self.appname
        print pic_url
        print pic_more_url
        print author
        print response.url
        print category
        print title
        print describe
        print content
        print home_url
        print publishedDate
        print crawlTime
        url = response.url
        item = NewsItem()
        item['app_name'] = self.appname
        item['count'] = self.count
        item['pic_url'] = pic_url
        item['pic_more_url'] = pic_more_url
        item['author'] = author
        item['url'] = url
        item['category'] = category
        item['title'] = title
        item['describe'] = describe
        item['content'] = content.replace('\r','').replace('\n','')
        item['home_url'] = home_url
        item['publishedDate'] = publishedDate
        item['crawlTime'] = crawlTime
        if category=='lishi':
            item['category'] =u'历史'.encode('utf-8')
        elif category=='guoji':
            item['category'] =u'国际'.encode('utf-8')
        elif category=='caijing':
            item['category'] =u'财经'.encode('utf-8')
        elif category =='junshi':
            item['category'] =u'军事'.encode('utf-8')
        else:
            item['category'] =u'推荐'.encode('utf-8')
        numappName = self.readjson()
        if len(numappName) == 0:
            items = {
                'url':response.url
            }

            with open('dongfangtoutiao.json','a+') as fp:
                line = json.dumps(dict(items),ensure_ascii = False) + '\n'
                fp.write(line)
            yield item
        else:
            for i in range(len(numappName)):
                if numappName[i]['url'] == response.url:
                    return
            else:
                items = {
                    'url':response.url
                }
                with open('dongfangtoutiao.json','a+') as fp:
                    line = json.dumps(dict(items),ensure_ascii = False) + '\n'
                    fp.write(line)
                yield item

    def readjson(self):
        s = []
        file_object = open('dongfangtoutiao.json','r')
        try:
            while True:
                line = file_object.readline()
                data = json.loads(line)
                s.append(data)
        finally:
            return s

