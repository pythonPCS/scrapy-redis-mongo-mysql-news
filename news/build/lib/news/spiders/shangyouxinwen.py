#-*- coding: utf-8 -*-
from scrapy.spider import Spider
from urlparse import urljoin
from scrapy.selector import Selector
from scrapy.http import Request
import time
import json
#from selenium import selenium
import re
import sys
from news.DataResource import TransportData
import scrapy
from news.items import NewsItem
reload(sys)
sys.setdefaultencoding('utf8')
class shangyou(Spider):
    name = "shangyouxinwen"
    base_url = "http://www.cqcb.com"
    start_urls = [
        "https://www.cqcb.com/headline/index.json?udid=862620027634098&appkey=1c496fbce1a47b049a1704ea8160c15b",
        "https://www.cqcb.com/hot/index.json?udid=862620027634098&appkey=1c496fbce1a47b049a1704ea8160c15b",
        "https://www.cqcb.com/reading/index.json?udid=862620027634098&appkey=1c496fbce1a47b049a1704ea8160c15b",
        "https://www.cqcb.com/science/index.json?udid=862620027634098&appkey=1c496fbce1a47b049a1704ea8160c15b",
        "https://www.cqcb.com/finance/index.json?udid=862620027634098&appkey=1c496fbce1a47b049a1704ea8160c15b",
    ]
    DOWNLOAD_DELAY = 0
    count = 0
    appname = "上游新闻"
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str,"%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        results = json.loads(response.body)
        pagenum = int(results['pagenum'])
        thispage = int(results['thispage'])
        if 'hot' in response.url:
            pagetitle = u'头条'.encode('utf-8')
        elif 'headline' in response.url:
            pagetitle = u'推荐'.encode('utf-8')
        elif 'finance' in response.url:
            pagetitle = u'金融'.encode('utf-8')
        elif 'science' in response.url:
            pagetitle = u'科学'.encode('utf-8')
        else:
            pagetitle = u'推荐'.encode('utf-8')
        newslists = results['newslist']
        acceptable_title = []
        for newslist in newslists:
            title = newslist['title']
            titleurl = newslist['titleurl']
            titleurl = urljoin(self.base_url,titleurl)
            pic_url = newslist['titlepic']
            publishedDate = newslist['newstime']
            author = newslist['befrom']
            b = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
            b = int(time.mktime(b))
            if b > self.timeStamp:
                acceptable_title.append(title)
                yield Request(titleurl, meta={"title": title, "pic_url": pic_url, "publishedDate": publishedDate,
                                              "author": author, "category": pagetitle},
                              callback=self.parse_news)
        if pagenum > thispage:
            if thispage == 1:
                next_page = re.sub("index.json", "index_2.json",response.url)
            else:
                next_page = re.sub("index_\d*.json","index_"+str(thispage + 1) +".json",response.url)
            yield Request(next_page,callback=self.parse)

    def parse_news(self,response):
        describe = ""
        title = response.meta['title']
        pic_url = response.meta['pic_url']
        publishedDate = response.meta['publishedDate']
        author = response.meta['author']
        category = response.meta['category']
        crawlTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        home_url = self.base_url
        hxs = Selector(response)
        content = hxs.xpath('//div[@class="article_text"]//text()').extract()
        content = "".join(content)
        content = content.replace("\n","").replace(" ","")
        pic_more_url = hxs.xpath('//div[@class="article_text"]//img/@src').extract()
        pic_more_url = pic_more_url
        self.count = self.count + 1
        url = response.url
        if pic_url:
            pic_url = pic_url.encode("utf-8")
        if pic_more_url:
            for i in range(0, len(pic_more_url)):
                pic_more_url[i] = pic_more_url[i].encode('utf-8')
            pic_more_url = set(pic_more_url)
        if author:
            author = author.encode('utf-8')
        if category:
            category = author.encode('utf-8')
        if title:
            title = title.encode('utf-8')
        if describe:
            describe = describe.encode('utf-8')
        if content:
            content = content.encode('utf-8')
        if publishedDate:
            publishedDate = publishedDate.encode('utf-8')
        if crawlTime:
            crawlTime = crawlTime.encode('utf-8')
        pic_more_url = set(pic_more_url)
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
        yield item