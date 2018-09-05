#-*- coding: utf-8 -*-
from scrapy.spider import Spider
import time
import json
from lxml.etree import HTML
import re
import sys
import scrapy
from news.items import NewsItem
reload(sys)
sys.setdefaultencoding('utf8')

class Nytimes(Spider):
    name = "niuyueshibao"
    base_url = "https://cn.nytimes.com"
    count = 0
    appname = "纽约时报中文网"
    allowed_domains = ["cn.nytimes.com"]
    start_urls = [
        'https://cn.nytimes.com/world/',   #国际
        'https://cn.nytimes.com/china/',   #中国
        'https://cn.nytimes.com/business/',  #商业与经济
        'https://cn.nytstyle.com/technology/',
    ]
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links_url = response.xpath('//ul[@class="autoList"]/li/div[1]/a/@href').extract()
        pic_url = response.xpath('//ul[@class="autoList"]/li/div[1]/a/img/@data-url').extract()
        title = response.xpath('//ul[@class="autoList"]/li/h3/a/text()').extract()
        writer = response.xpath('//ul[@class="autoList"]/li/h6').extract()
        summary = response.xpath('//ul[@class="autoList"]/li/p/text()').extract()
        if len(links_url) > 0:
            for i in range(0, len(links_url)):
                if '//' in links_url[i]:
                    url = 'http:'+links_url[i]
                else:
                    url = 'https://cn.nytimes.com'+links_url[i]
                try:
                    pic_url1 = pic_url[i]
                except:
                    pic_url1 = ''
                print title[i]
                yield scrapy.Request(url,meta={
                    'title': title[i],
                    'writer': writer[i],
                    'pic_url': pic_url1,
                    'summary': summary[i],
                    'home_url': response.url
                }, callback=self.parse_item, dont_filter=True)
        else:
            links_url = response.xpath('//ul[@class="well basic_list  first last"]/li/a/@href').extract()
            pic_url = response.xpath('//ul[@class="well basic_list  first last"]/li/a/img/@data-url').extract()
            title = response.xpath('//ul[@class="well basic_list  first last"]/li/a/@title').extract()
            writer = response.xpath('//ul[@class="well basic_list  first last"]/li/div').extract()
            summary = response.xpath('//ul[@class="well basic_list  first last"]/li/p/text()').extract()
            for i in range(0, len(links_url)):
                if '//' in links_url[i]:
                    url = 'http:' + links_url[i]
                else:
                    url = 'https://cn.nytimes.com' + links_url[i]
                try:
                    pic_url1 = pic_url[i]
                except:
                    pic_url1 = ''
                yield scrapy.Request(url, meta={
                    'title': title[i],
                    'writer': writer[i],
                    'pic_url': pic_url1,
                    'summary': summary[i],
                    'home_url': response.url
                }, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        title = response.meta['title']
        writer = response.meta['writer']
        pic_url = response.meta['pic_url']
        home_url = response.meta['home_url']
        describe = response.meta['summary']
        app_name = '纽约时报中文网'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        try:
            content = response.xpath('//div[@class="article-left col-lg-8"]').extract()[0]
            selator = HTML(content)
            content = selator.xpath('//text()')
            content = ''.join(content)
            content = content.replace('\t', '').replace('\n', '').replace('\r', '')
        except:
            content = response.xpath('//section[@class="article-body"]').extract()
            selator = HTML(content[0])
            content = selator.xpath('//text()')
            content = ''.join(content)
            content = content.replace('\t', '').replace('\n', '').replace('\r', '')
        writer = re.findall('>(.*?)<', writer)
        writerdata = ''
        for i in range(0, len(writer)):
            writerdata += writer[i]
        author = writerdata
        try:
            pic_more_url = response.xpath('//figure[@class="article-span-photo"]/img/@src').extract()
            pic_more_url = pic_more_url[0]
        except:
            pic_more_url = ''
        try:
            pubTime = response.xpath('//div[@class="byline"]/time/@datetime').extract()
            pubTime = pubTime[0]
        except:
            pubTime = '2018-01-01'
        if 'world' in home_url:
            category = u'国际'.encode('utf-8')
        elif 'china' in home_url:
            category = u'中国'.encode('utf-8')
        elif 'business' in home_url:
            category = u'商业与经济'.encode('utf-8')
        elif 'technology' in home_url:
            category = u'科技'.encode('utf-8')
        elif 'education' in home_url:
            category = u'教育与职场'.encode('utf-8')
        elif 'culture' in home_url:
            category = u'文化'.encode('utf-8')
        else:
            category = u'最新文章'.encode('utf-8')
        publishedDate = pubTime
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
        item['content'] = content
        item['home_url'] = home_url
        item['publishedDate'] = publishedDate
        item['crawlTime'] = crawlTime
        timeArray = time.strptime(pubTime, "%Y-%m-%d %H:%M:%S")
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            self.count = self.count + 1
            item['count'] = self.count
            yield item