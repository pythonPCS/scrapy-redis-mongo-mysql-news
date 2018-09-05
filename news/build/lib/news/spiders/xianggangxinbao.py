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

class xinbao(Spider):
    name = 'xinbaomobile'
    start_urls = [
        'http://www1.hkej.com/dailynews/commentary',#时事评论
        'http://www1.hkej.com/dailynews/finnews',#财经新闻
        'http://www1.hkej.com/dailynews/politics',#政坛
        'http://www1.hkej.com/dailynews/views',#独眼香江
        'http://www1.hkej.com/dailynews/cntw',#两岸消息
        'http://www1.hkej.com/dailynews/international',#EJGlobal
        'http://www1.hkej.com/dailynews/headline',#即时要闻
        'http://www1.hkej.com/features/topic/tag/2018%E5%85%A9%E6%9C%83',#两会
    ]
    count = 0
    download_delay = 2
    # a = "2017-09-27 00:00:00"
    # timeArray = time.strptime(a,"%Y-%m-%d %H:%M:%S")
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        links = response.xpath('//div[@id="news-listing-wrapper"]/div/h2/a/@href').extract()
        title = response.xpath('//div[@id="news-listing-wrapper"]/div/h2/a/text()').extract()
        desc = response.xpath('//div[@id="news-listing-wrapper"]/div/p[2]/text()').extract()
        for i in range(1,100):
            try:
                url = links[i]
                if 'http' not in url:
                    url = 'http://www1.hkej.com' + url
                tit =title[i]
                # print url
                # print tit
                try:
                    describe = desc[i].replace('\t','').replace('\n','').replace('\r','')
                    # print describe
                except:
                    describe = ''
                    # print describe

                yield Request(url,meta={
                    'home_url':response.url,
                    'describe':describe
                },callback=self.parse_item)
            except:
                links = response.xpath('//ul[@class="fea_s_list"]/li/a/@href').extract()
                desc  = response.xpath('//ul[@class="fea_s_list"]/li/div[1]/a/text()').extract()
                for i in range(1,len(links)):
                    url = links[i]
                    if 'http' not in url:
                        url = 'http://www1.hkej.com' + url
                    try:
                        describe = desc[i].replace('\t', '').replace('\n', '').replace('\r', '')
                        # print describe
                    except:
                        describe = ''
                        # print describe
                    yield Request(url, meta={
                        'home_url': response.url,
                        'describe': describe
                    }, callback=self.parse_item)

    def parse_item(self,response):
        home_url = response.meta['home_url']
        app_name = '信报Mobile'
        title = response.xpath('//h1/text()').extract()[0]
        publishedDate = response.xpath('//p[@id="date"]/text()').extract()[0].replace(u'年','-').replace(u'月','-').replace(u'日',' ') + '00:00:00'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_url = ''
        describe = response.meta['describe']
        content = response.xpath('//div[@id="article-detail-wrapper"]').extract()
        contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', contentt)
        contentdata = ''
        for i in range(0, len(content)):
            contentdata += content[i]
        content = contentdata
        author = ''
        pic_more_url = ''
        if 'commentary' in home_url:
            category = u'時事評論'.encode('utf-8')
        elif 'finnews' in home_url:
            category = u'財經新聞'.encode('utf-8')
        elif 'politics' in home_url:
            category = u'政壇脈搏'.encode('utf-8')
        elif 'views' in home_url:
            category = u'獨眼香江'.encode('utf-8')
        elif 'cntw' in home_url:
            category = u'兩岸消息'.encode('utf-8')
        elif 'international' in home_url:
            category = u'EJGlobal'.encode('utf-8')
        elif '2018' in home_url:
            category = u'兩會會議'.encode('utf-8')
        else:
            category = u'即時新聞'.encode('utf-8')

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
        self.count = self.count + 1
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            yield item