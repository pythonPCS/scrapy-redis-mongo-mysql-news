#-*- coding: utf-8 -*-
from scrapy.spider import Spider
from urlparse import urljoin
from scrapy.selector import Selector
from scrapy.http import Request
import time
import json
from lxml import etree
import re
import sys
from news.DataResource import TransportData
import scrapy
from news.items import NewsItem
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf8')

class Shijieribao(Spider):
    name = "shijieribao"
    base_url = "https://www.worldjournal.com/?variant=zh-cn"
    count = 0
    appname = "世界日报"
    start_urls = [
        'https://www.worldjournal.com/topic/%E5%9C%8B%E9%9A%9B%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/?pno=1',#国际
        'https://www.worldjournal.com/topic/%E5%9C%8B%E9%9A%9B%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/?pno=2',#国际
        'https://www.worldjournal.com/topic/%E5%9C%8B%E9%9A%9B%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/?pno=3',#国际
        'https://www.worldjournal.com/topic/%E5%9C%8B%E9%9A%9B%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/?pno=4',#国际
        'https://www.worldjournal.com/topic/%E8%A6%81%E8%81%9E%E6%96%B0%E8%81%9E/?pno=1',#热门
        'https://www.worldjournal.com/topic/%E8%A6%81%E8%81%9E%E6%96%B0%E8%81%9E/?pno=2',#热门
        'https://www.worldjournal.com/topic/%E8%A6%81%E8%81%9E%E6%96%B0%E8%81%9E/?pno=3',#热门
        'https://www.worldjournal.com/topic/%E8%A6%81%E8%81%9E%E6%96%B0%E8%81%9E/?pno=4',#热门
        'https://www.worldjournal.com/topic/%E5%8F%B0%E7%81%A3%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/?pno=1',#两岸
        'https://www.worldjournal.com/topic/%E5%8F%B0%E7%81%A3%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/?pno=2',#两岸
        'https://www.worldjournal.com/topic/%E4%B8%AD%E5%9C%8B%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/?pno=3',#两岸
        'https://www.worldjournal.com/topic/%E4%B8%AD%E5%9C%8B%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD/?pno=4',#两岸
        'https://www.worldjournal.com/topic/%E7%A4%BE%E8%AB%96-2/?pno=1',#观点
        'https://www.worldjournal.com/topic/%E7%A4%BE%E8%AB%96-2/?pno=2',#观点
        'https://www.worldjournal.com/topic/%E7%A4%BE%E8%AB%96-2/?pno=3',#观点
        'https://www.worldjournal.com/topic/%E7%A4%BE%E8%AB%96-2/?pno=4',#观点
    ]
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-10', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links_url = response.xpath('//div[@class="post-content"]/h2/a/@href').extract()
        title = response.xpath('//div[@class="post-content"]/h2/a/text()').extract()
        publish = response.xpath('//div[@class="post-content"]/time/@datetime').extract()
        if len(links_url) > 0:
            for i in range(0,len(links_url)):
                url = links_url[i]
                tit = title[i]
                pub = publish[i]
                desc = ''
                yield Request(url,meta={
                    'title':tit,
                    'publish':pub,
                    'describe':desc,
                    'home_url':response.url
                },callback=self.parse_item)
        else:
            pass

    def parse_item(self,response):
        title = response.meta['title']
        publishedDate = response.meta['publish']
        publishedDate = response.xpath('//time[@class="date"]/@datetime').extract()[0]
        print publishedDate
        describe = response.meta['describe']
        home_url = response.meta['home_url']
        app_name = '世界日报'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        author = ''
        pic_url = ''
        content =response.xpath('//div[@class="post-content"]').extract()
        contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', contentt)
        contentdata = ''
        for i in range(0, len(content)):
            contentdata += content[i]
        content = contentdata
        try:
            pic_more_url =response.xpath('//div[@class="img-holder"]/a/img/@src').extract()
            pic_more_url1 = []
            if len(pic_more_url) > 0:
                for i in range(0, len(pic_more_url)):
                    pic_more_url1.append(pic_more_url[i])
                pic_more_url = str(set(pic_more_url1))
            else:
                pic_more_url = ''
        except:
            pic_more_url = ''
        if u'要聞新聞' in home_url:
            category = u'热门'.encode('utf-8')
        elif '%E5%9C%8B%E9%9A%9B%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD' in home_url:
            category = u'国际'.encode('utf-8')
        elif '%E5%8F%B0%E7%81%A3%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD' in home_url:
            category = u'两岸'.encode('utf-8')
        elif '%E4%B8%AD%E5%9C%8B%E6%96%B0%E8%81%9E%E7%B8%BD%E8%A6%BD' in home_url:
            category = u'两岸'.encode('utf-8')
        elif '%E7%A4%BE%E8%AB%96' in home_url:
            category = u'观点'.encode('utf-8')
        else:
            category = u'热门'.encode('utf-8')
        url = response.url
        self.count += 1
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            yield item

