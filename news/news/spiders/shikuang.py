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
class shikuang(Spider):
    name = "shikuang"
    ts = int(time.time())
    base_url = "https://my.cqtimes.cn/"
    # start_urls = [
    #     "https://my.cqtimes.cn/?m=mobile&c=index&a=newslist&ts=1507873678&uuid=377b5fb4e857f646c5630afdc9170617&version=2.2.8&sign=07e342fc8869d5b3755a13659ebba43c"
    # ]
    DOWNLOAD_DELAY = 0.5
    count = 0
    appname = "实况"
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    url = "https://my.cqtimes.cn/?m=mobile&c=index&a=newslist&ts={ts}&uuid=377b5fb4e857f646c5630afdc9170617&version=2.2.8&sign={sign}"
    # existing_title = TransportData.getData(appname)
    def start_requests(self):
        sign = "/?m=mobile&c=index&a=newslist&ts=" + str(self.ts) + "&uuid=377b5fb4e857f646c5630afdc9170617&version=2.2.8cqtimes"
        sign = self.md5(sign)
        event_id = ['15','51','225','221','163','220','242','245','16','252','256']
        event_value = ['推荐','热点','视频','社会','民生','休闲','搞笑','图片','订阅','娱乐','旅游']
        page = 1
        self.url = self.url.format(ts=self.ts, sign=sign)
        for i in range(0,len(event_id)):
            yield scrapy.FormRequest(
                self.url,
                formdata={
                    "version": "2.2.8",
                    "app_type": "weikuai",
                    "mac": "53cd97b8d97b75617eb03c10e0b31195",
                    "uuid": "377b5fb4e857f646c5630afdc9170617",
                    "issimulator": "1",
                    "uid": "",
                    "event_id": event_id[i],
                    "event_value": event_value[i],
                    "p": str(page),
                    "type": event_id[i],
                    "newstype_type": "1"
                },
                meta={"event_id": event_id[i],"event_value": event_value[i],"page":page},callback=self.parse_next)
    def parse_next(self,response):
        # print response.body
        acc_tit = []
        results = json.loads(response.body)
        results = results['post_first']
        for result in results:
            newsData = result['newsData']
            url = newsData['url']
            title = newsData['title']
            # print url
            # print title
            # print newsData

            if "addtime" in newsData.keys():
                publishedDate = newsData['addtime']
            elif "checktime" in newsData.keys():
                publishedDate = newsData['checktime']
            if 'img' in newsData.keys():
                pic_url = newsData['img']
            else:
                pic_url = ""
            pic_more_url = newsData['imglist']
            # pic_more_url = set(pic_more_url)
            if 'read' in newsData.keys():
                content = newsData['read']
            else:
                content = ""
            if int(publishedDate) > int(self.timeStamp):
                acc_tit.append(title)
                yield Request(url, meta={"title":title, "publishedDate":publishedDate, "pic_url":pic_url, "content":content,
                                        "pic_more_url":pic_more_url,"event_value":response.meta['event_value']}, callback=self.parse_news)
            if len(acc_tit) > 1:
                event_id = response.meta['event_id']
                event_value = response.meta['event_value']
                page = response.meta['page']
                page = page + 1
                # page = str(page)
                # page = page.encode('gdk')
                # print page
                yield scrapy.FormRequest(
                    self.url,
                    formdata={
                        "version": "2.2.8",
                        "app_type": "weikuai",
                        "mac": "53cd97b8d97b75617eb03c10e0b31195",
                        "uuid": "377b5fb4e857f646c5630afdc9170617",
                        "issimulator": "1",
                        "uid": "",
                        "event_id": event_id,
                        "event_value": event_value,
                        "p": str(page),
                        "type": event_id,
                        "newstype_type": "1"
                    },
                    meta={"event_id": event_id, "event_value": event_value, "page": page},callback=self.parse_next)
    def parse_news(self,response):
        title = response.meta['title']
        publishedDate = response.meta['publishedDate']
        pic_url = response.meta['pic_url']
        hxs = Selector(response)
        pic_more_url = response.meta['pic_more_url']
        pic_more_url = set(pic_more_url)
        author = hxs.xpath('//p[@class="art_txt sau"]/text()').extract()
        print author
        while "" in author:
            author.remove("")
        if author:
            author = author[1].encode('utf-8').replace("\t","").replace("\n","")
        else:
            author = ""
        category = response.meta['event_value']
        describe = ""
        content = response.meta['content']
        if content == "":
            content = hxs.xpath("//div[@class='article']//text()").extract()
            content = "".join(content)
        content = content.encode('utf-8')
        content = content.replace("\n","")
        home_url = self.base_url
        crawlTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        publishedDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(publishedDate)))
        if pic_url:
            pic_url = pic_url.encode('utf-8')
        if title:
            title = title.encode('utf-8')
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
        item['content'] = content
        item['home_url'] = home_url
        item['publishedDate'] = publishedDate
        item['crawlTime'] = crawlTime
        # yield item
        # TransportData.transport_data(self.appname, pic_url, pic_more_url, author, response.url, category, title,
        #                              describe, content, home_url, publishedDate, crawlTime)
        exsit_title = TransportData.getData("app_shikuang", title)
        if exsit_title:
            return
        else:
            yield item
            TransportData.transport_data("app_shikuang", title, publishedDate)


    def md5(self, str):
        import hashlib
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()