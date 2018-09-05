#-*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from urlparse import urljoin
import json
# from news.Configuration import Configuration
# from yidong.extensions.myExtension import MyExtension
# from yidong_pay.ResultTransferUtil import ResultTransferUtil
# from rpc.app.ttypes import AppWeb
# from rpc.app.ttypes import AppType
# from rpc.app.ttypes import OriginType
# from yidong_pay.DataResource import GetData
# from rpc.app.ttypes import AppComment
# from mySQLdataexport import *
import time
import re
from news.DataResource import TransportData
from news.items import NewsItem


class xiangang(Spider):
    name = 'xiangangxinwen'
    start_urls = [
        'http://orientaldaily.on.cc/rss/news.xml',
        'http://www.epochtimes.com/gb/n24hr.xml',
        'http://rss.sina.com.cn/news/china/focus15.xml',
        'https://www.hket.com/rss/hongkong'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        title = response.xpath('//item/title/text()').extract()
        desc = response.xpath('//item/description/text()').extract()
        links = response.xpath('//item/link/text()').extract()
        pubt = response.xpath('//item/pubDate/text()').extract()
        for i in range(len(links)):
            url = links[i].replace('\t','').replace('\n','').replace('\r','').replace(' ','')
            tit = title[i].replace('\t','').replace('\n','').replace('\r','').replace(' ','')
            describe = desc[i].replace('\t','').replace('\n','').replace('\r','').replace(' ','')
            publish = pubt[i].replace('\t','').replace('\n','').replace('\r','')
            publish = publish.split(', ')[1]
            t = publish.split(' ')
            t1 = t[0]
            t2 = t[1]
            t3 = t[2]
            t4 = t[3]
            t12 = t2
            if 'June' in t12:
                tt = '06'
            elif 'Jun' in t12:
                tt = '06'
            elif 'January' in t12:
                tt = '01'
            elif 'Jan' in t12:
                tt = '01'
            elif 'February' in t12:
                tt = '02'
            elif 'Feb' in t12:
                tt = '02'
            elif 'March' in t12:
                tt = '03'
            elif 'Mar' in t12:
                tt = '03'
            elif 'April' in t12:
                tt = '04'
            elif 'Apr' in t12:
                tt = '04'
            elif 'May' in t12:
                tt = '05'
            elif 'July' in t12:
                tt = '07'
            elif 'August' in t12:
                tt = '08'
            elif 'Aug' in t12:
                tt = '08'
            elif 'September' in t12:
                tt = '09'
            elif 'Sept' in t12:
                tt = '09'
            elif 'October' in t12:
                tt = '10'
            elif 'Oct' in t12:
                tt = '10'
            elif 'November' in t12:
                tt = '11'
            elif 'Nov' in t12:
                tt = '11'
            elif 'December' in t12:
                tt = '12'
            elif 'Dec' in t12:
                tt = '12'
            else:
                tt = '01'
            publish = t3 + '-' + tt + '-' + t1 + ' ' + t4
            print publish
            timeArray = time.strptime(publish, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            if timeStamp >= self.timeStamp:
                publish = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timeStamp)))
                yield Request(url, meta={
                    'publish': publish,
                    'title': tit,
                    'describe': describe
                }, callback=self.parse_item, dont_filter=True)


    def parse_item(self, response):
        publishedDate = response.meta['publish']
        title = response.meta['title']
        describe = response.meta['describe']
        app_name = 'HK News'
        author = ''
        pic_url = ''
        home_url = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_more_url = ''
        category = '最新'
        content = response.xpath('//p').extract()
        contentt = ''
        for i in range(len(content)):
            contentt += content[i]
        content = contentt.replace('\t', '').replace('\n', '').replace('\r', '')
        print "app名称", app_name
        print "主图片url", pic_url
        print "子图片url", pic_more_url
        print "作者", author
        print "详情页地址", response.url
        print "所属类型", category
        print "标题", title
        print "描述", describe
        print "内容", content
        print "主url", home_url
        print "发布时间", publishedDate
        print "爬取时间", crawlTime
        url = response.url
        item = NewsItem()
        item['app_name'] = app_name
        item['pic_url'] = pic_url
        item['pic_more_url'] = pic_more_url
        item['author'] = author
        item['url'] = url
        item['category'] = category
        item['title'] = title
        item['describe'] = describe
        item['content'] = content.replace('<p>','').replace('</p>')
        item['home_url'] = home_url
        item['publishedDate'] = publishedDate
        item['crawlTime'] = crawlTime
        self.count += 1
        item['count'] = self.count
        yield item



