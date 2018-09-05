#-*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from urlparse import urljoin
import scrapy
import json
from news.DataResource import TransportData

import time
import re
from news.items import NewsItem
class Shangguan(Spider):
    name = "shangguanxinwen"
    app_name="上观新闻"
    allowed_domains = ["services.shobserver.com"]
    base_url = ""
    count = 0
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str,"%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    # existing_title = TransportData.getData('uc头条')
    def start_requests(self):
        k = ['sectionid', 'subsectionid', 'section', 'sign', 'times']
        v = [
            ('1', '1,2,3', '政情', '9eec20d8e2f6bcafec80252fd5373dae', '1505287208975'),
            ('2', '13,14,15', '财经', '3c9446daa0373678c415f31340dabec0', '1505366899027'),
            ('35', '22,23,24', '区情', '0286ba8f3271622916cc73463636d33e', '1505366947969'),
            ('22', '29,30,31', '城事', '9a7079741240fb51b5a12369673324fc', '1505366950899'),
            ('4', '40,41,42', '文化', '09abef27619d3df33528559dbe08fa3a', '1505366953125'),
            ('21', '53,82,54', '天下', '456b6880eaa1e85a581c9e93aba9430c', '1505366955628'),
            ('40', '64,65,66', '互动', 'd27adb160731de03d62044379778e4c1', '1505366957610'),
            ('41', '95,96,97', '视觉', '8ce834e61847f77e42be05dfd89e959b', '1505366959761')
        ]
        dicts = [dict(zip(k, values)) for values in v]
        for i in range(len(dicts)):
            pages = dicts[i]
            url = "http://services.shobserver.com/news/get/sectionidWithNidPtime?platform=2&pagesize=10&subsectionid=%s&versionCode=440&page=1&sign=%s&sectionid=%s&times=%s"%\
              (pages.get("subsectionid"),pages.get("sign"),pages.get("sectionid"),pages.get("times"))
            yield  Request(
                    url,
                    meta={"sectionname":pages.get("section"),
                          "sectionid":pages.get("sectionid"),
                          "subsectionid":pages.get("subsectionid"),
                          "sign":pages.get("sign"),
                          "times":pages.get("times"),
                          "page":1},
                    callback=self.parse
                )

    def parse(self, response):
        # 构造各种分类的网址
        results = json.loads(response.body)
        object = results["object"]
        newsList=object["newsList"]
        totalpage = object["totalpage"]
        total = object["total"]
        sectionname=response.meta["sectionname"]
        acceptable_title = []

        for i in range(len(newsList)):
            title = newsList[i]["title"]
            if title:
                title = title.encode('utf-8')
            else:
                title = ''

            # if title not in self.existing_title:
            acceptable_title.append(title)
            # summary = newsList[i]["summary"]
            id = newsList[i]["id"]
            # writer=newsList[i]["writerName"]
            writer= ''
            Link="http://services.shobserver.com/news/viewNewsDetail?id=%s&versionCode=440&platform=2&uid=0"%id
            yield Request(
                url=Link,
                meta={"title": title,'summary':'',"writer":writer,"Link":Link,"type":sectionname},
                callback=self.content_parse
            )

        # 下一页
        sectionid=response.meta["sectionid"]
        subsectionid=response.meta["subsectionid"]
        sign=response.meta["sign"]
        times=response.meta["times"]
        page=response.meta["page"]
        page += 1
        # if page<=totalpage:
        if page <= 50 :
            url = "http://services.shobserver.com/news/get/sectionidWithNidPtime?platform=2&pagesize=10&subsectionid=%s&versionCode=440&page=%s&sign=%s&sectionid=%s&times=%s" % (
                    subsectionid,page,sign, sectionid, times)

            yield Request(
                url,
                meta={"sectionname": sectionname,
                        "sectionid": sectionid,
                        "subsectionid":subsectionid,
                        "sign": sign,
                        "times": times,
                        "page":page},
                    callback=self.parse
                )


    def content_parse(self, response):
        import time
        app_name = "上观新闻"
        title=response.meta['title']
        summary=response.meta['summary']
        content_url=response.meta['Link']
        content_type=response.meta['type']
        writer=response.meta['writer']
        viewCount=0
        home_url="http://services.shobserver.com/news/get/homepage"
        crawlTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        hxs = Selector(response)
        picmore_url=hxs.xpath('//img/@src').extract()
        if picmore_url:
            pic_url = picmore_url[0].encode('utf-8')
            picmore_url = set(picmore_url)
        else:
            picmore_url = set()
            pic_url = ''
        content = hxs.xpath('//div[@class="news-content"]//text()').extract()
        if content:
            content = "".join(content)
            content = (re.sub(r'\s+', '', content)).strip()
            content = content.encode("utf-8")
        else:
            content = ''

        pubTime= hxs.xpath('//span[@class="news-attr publish-time"]//text()').extract()
        if pubTime:
            pubTime = pubTime[0].encode('utf-8')

        else:
            pubTime = ''
        # print pubTime
        try:
            a = time.strptime(pubTime, "%Y-%m-%d %H:%M:%S")
        except:
            a = time.strptime(pubTime, "%Y-%m-%d %H:%M")

        # 转换成时间戳
        a = time.mktime(a)
        # print self.timeStamp
        if int(a) > int(self.timeStamp):
            self.count = self.count + 1
            print self.count
            print app_name
            print pic_url
            print picmore_url
            print writer
            print content_url
            print content_type
            print viewCount
            print title
            print summary
            print content
            print home_url
            print pubTime
            print crawlTime

            author = writer
            if author:
                author = author.encode('utf-8')
            else:
                author = ""
            category = content_type
            describe = summary
            describe = describe.encode('utf-8')
            publishedDate = pubTime + ':00'
            pic_more_url = picmore_url
            url = response.url
            item = NewsItem()
            item['app_name'] = app_name
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
            # if author:
            #     author = author.encode('utf-8')
            # else:
            #     author = ""
            # TransportData.transport_data(app_name, pic_url, pic_more_url, author, response.url, category, title,
            #                              describe, content, home_url, publishedDate, crawlTime)

            exsit_title = TransportData.getData("app_shangguanxinwen", title)
            if exsit_title:
                return
            else:
                yield item
                TransportData.transport_data("app_shangguanxinwen", title, publishedDate)
