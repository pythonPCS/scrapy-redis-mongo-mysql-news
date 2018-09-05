#coding=utf-8
import scrapy
import time
import json
import re
from news.items import NewsItem
from news.DataResource import TransportData
from scrapy.http import Request
import requests

class jiaohuidian(scrapy.Spider):
    name = 'jiaohuidianxinwen'
    start_urls = [
        'https://japi.xhby.net/api/articles?column_id=79f521279a394064b66341a5e2a34629&page=1&hide_top=0',#推荐ossJson
        'https://japi.xhby.net/api/articles?column_id=79f521279a394064b66341a5e2a34629&page=2&hide_top=0',#推荐
        'https://japi.xhby.net/api/articles?column_id=79f521279a394064b66341a5e2a34629&page=3&hide_top=0',#推荐
        'https://japi.xhby.net/api/articles?column_id=12&page=1&hide_top=0',#专题 ossJson
        'https://japi.xhby.net/api/articles?column_id=12&page=2&hide_top=0',#专题
        'https://japi.xhby.net/api/articles?column_id=12&page=3&hide_top=0',#专题
        'https://japi.xhby.net/api/jhd_article?page=1',#交汇号 699
        'https://japi.xhby.net/api/jhd_article?page=2',#交汇号
        'https://japi.xhby.net/api/jhd_article?page=3',#交汇号
        'https://japi.xhby.net/api/leaders_province?page=1',#政情
        'https://japi.xhby.net/api/leaders_province?page=2',#政情
        'https://japi.xhby.net/api/leaders_province?page=3',#政情
        'https://japi.xhby.net/api/service?page=1',#服务
        'https://japi.xhby.net/api/service?page=2',#服务
        'https://japi.xhby.net/api/service?page=3',#服务
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        data = json.loads(response.body)
        data = data['data']
        try:
            try:
                try:
                    try:
                        try:
                            try:
                                data = data['column']
                                # print data
                            except:
                                data = data['data']     #政情
                                # print data
                        except:
                            data = data['top_activity']  #服务
                            # print data
                    except:
                        data = data['article_top']       #交汇号，#推荐，#专题
                        # print data
                except:
                    data = data['article']['data']
                    # print data
            except:
                data = data['bottom_activity']['data']
                # print data
        except:
            data = data['order_column']['data']
            # print data

        publishedDate = ''
        for i in range(0,len(data)):
            try:
                title = data[i]['title']
                # print title
            except:
                title = data[i]['duty']
                # print title
            try:
                try:
                    links = data[i]['ossJson']
                    # print links
                except:
                    links = data[i]['web_url']
                    # print links
            except:
                id = data[i]['id']
                links = 'http://jnews.xhby.net/waparticles/699/' + id
                # print links
                try:
                    publishedDate = data[i]['created_at']
                except:
                    publishedDate = ''
            try:
                try:
                    pic_url = data[i]['pic0']
                except:
                    pic_url = data[i]['iconUrl']
            except:
                pic_url = ''
            try:
                describe = data[i]['description']
            except:
                describe = ''
            yield scrapy.Request(links,meta={
                'title':title,
                'describe':describe,
                'pic_url':pic_url,
                'home_url':response.url,
                'publishedDate':publishedDate
            },callback=self.parse_item)

    def parse_item(self,response):
        title = response.meta['title']
        describe = response.meta['describe']
        pic_url = response.meta['pic_url']
        home_url = response.meta['home_url']
        publishedDate = response.meta['publishedDate']
        app_name = '交汇点新闻'.encode('utf-8')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        try:
            data =json.loads(response.body)
            content = data['article']['content']
            pic_more_url = ''
            if content == '':
                content = data['article']['aAbstract']
                if content =='':
                    content = data['article']['attachment']
                    contentt = ''
                    for i in range(0,len(content)):
                        contentt += content[i]['attContent']
                    content = contentt
                    pic_more_url = data['article']['attachment']
                    pic_more_url1 = []
                    for i in range(0,len(pic_more_url)):
                        pic_more_url1.append(pic_more_url[i]['attPath'])
                    pic_more_url = str(set(pic_more_url1))

            publishedDate = data['article']['created_at']
            if pic_more_url =='':
                try:
                    pic_more_url = data['article']['contentImages']
                    pic_more_url1 = []
                    for i in range(0,len(pic_more_url)):
                        pic_more_url1.append(pic_more_url[i]['attPath'])
                    pic_more_url = str(set(pic_more_url1))
                except:
                    pic_more_url = ''
            author = data['article']['aEditor']

            if 'column_id=12&' in home_url:
                category = u'专题'.encode('utf-8')
            elif 'jhd_article?' in home_url:
                category = u'交汇号'.encode('utf-8')
            elif 'leaders_province' in home_url:
                category = u'政情'.encode('utf-8')
            elif 'service' in home_url:
                category = u'服务'.encode('utf-8')
            else:
                category = u'推荐'.encode('utf-8')
            if category ==u'专题':
                content = data['article']['aAbstract']
        except:
            content = response.xpath('//p').extract()
            contentt = ''
            for i in range(0, len(content)):
                contentt += content[i]
            content = contentt
            content = content.replace('\t','').replace('\n','').replace('\r','')
            content = re.findall('>(.*?)<',content)
            contentt = ''
            for i in range(0,len(content)):
                contentt += content[i]
            content = contentt
            pic_more_url = ''
            author = ''
            if 'column_id=12&' in home_url:
                category = u'专题'.encode('utf-8')
            elif 'jhd_article?' in home_url:
                category = u'交汇号'.encode('utf-8')
            elif 'leaders_province' in home_url:
                category = u'政情'.encode('utf-8')
            elif 'service' in home_url:
                category = u'服务'.encode('utf-8')
            else:
                category = u'推荐'.encode('utf-8')

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
        if publishedDate > self.timeStamp:
            yield item

