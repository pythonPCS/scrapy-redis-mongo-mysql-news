#coding=utf-8
import scrapy
import time
import json
import re
from news.items import NewsItem
from news.DataResource import TransportData
class dwtw(scrapy.Spider):
    name='dongwang'
    allowed_domains=['hk.on.cc']
    start_urls=[
        'http://hk.on.cc/cn/news/index.html',
        'http://hk.on.cc/int/news/index.html',
        'http://hk.on.cc/tw/news/index.html',
        'http://hk.on.cc/hk/news/index.html'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    base_url='http://hk.on.cc'

    def parse(self, response):
        links = response.xpath('//div[@class="focus clearfix"]/div[1]/a/@href').extract()
        pic_url = response.xpath('//div[@class="focus clearfix"]/div[1]/a/img/@src').extract()
        if len(links) == 0:
            for i in range(0, len(links)):
                url=self.base_url + links[i]
                try:
                    pic_url1 = self.base_url + pic_url[i]
                except:
                    pic_url1 = ''
                yield scrapy.Request(url, meta={
                    'pic_url':pic_url1,
                    'home_url':response.url
                }, callback=self.parse_item)
        links = response.xpath('//div[@class="focusItem"]/a/@href').extract()
        pic_url = response.xpath('//div[@class="focusItem"]/a/div/img/@src').extract()
        for i in range(0, len(links)):
            url = self.base_url + links[i]
            try:
                pic_url1 = self.base_url + pic_url[i]
            except:
                pic_url1 = ''
            yield scrapy.Request(url, meta={
                'pic_url': pic_url1,
                'home_url': response.url
            }, callback=self.parse_item)


    def parse_item(self,response):
        title = response.xpath('//h1/text()').extract()[0]
        pic_url=response.meta['pic_url']
        pubTime=response.xpath('//span[@class="datetime"]/text()').extract()[0]
        pubTime=pubTime.replace(u'年','-').replace(u'月','-').replace(' ','').replace(u'日',' ')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url=response.meta['home_url']
        app_name='东网'
        describe = ''
        content=response.xpath('//div[@class="breakingNewsContent"]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        if 'tw' in home_url:
            category = u'台湾新闻'.encode('utf-8')
        elif 'cn' in home_url:
            category = u'大陆新闻'.encode('utf-8')
        elif 'int' in home_url:
            category = u'国际新闻'.encode('utf-8')
        else:
            category = u'港澳新闻'.encode('utf-8')
        author=''
        pic_more_url=response.xpath('//div[@class="photo"]/img/@src').extract()
        pic_more_url1=''
        for i in range(0,len(pic_more_url)):
            pic_more_url1+=self.base_url + pic_more_url[i] +';'
        pic_more_url=pic_more_url1
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
        acceptable_title = []
        print pubTime
        timeArray = time.strptime(pubTime, "%Y-%m-%d %H:%M")
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            acceptable_title.append(title)
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            yield item