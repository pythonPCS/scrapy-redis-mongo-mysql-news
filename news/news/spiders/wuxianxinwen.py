#coding=utf-8
import scrapy
import time
import json
import re
from news.items import NewsItem
from news.DataResource import TransportData
class wxxw(scrapy.Spider):
    name='wuxianxinwen'
    allowed_domains = ["tvb.com"]
    start_urls=[
        'http://news.tvb.com/list/focus/',  #要闻
        'http://news.tvb.com/list/instant/',#快讯
        'http://news.tvb.com/list/local/',  #港澳
        'http://news.tvb.com/list/greaterchina/',#两岸
        'http://news.tvb.com/list/world/', #国际
        'http://news.tvb.com/list/finance/',#财经
    ]
    base_url='http://news.tvb.com/'
    count = 0
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        home_url = response.url
        Url=[]
        title=[]
        links_url=response.xpath('//a[@class="title thumb"]/@href').extract()
        linke_title=response.xpath('//a[@class="title thumb"]/text()').extract()
        links_url1=response.xpath('//a[@class="title"]/@href').extract()
        linke_title1 =response.xpath('//a[@class="title"]/text()').extract()
        for i in range(0,len(links_url)):
            url=self.base_url+links_url[i]
            Url.append(url)
            title.append(linke_title[i])
        for i in range(0,len(links_url1)):
            url=self.base_url+links_url1[i]
            Url.append(url)
            title.append(linke_title1[i])
        for i in range(0,len(Url)):
            yield scrapy.Request(Url[i], meta={
                'home_url':home_url,
                'title':title[i]
            }, callback=self.parse_item)

    def parse_item(self,response):
        home_url=response.meta['home_url']
        publishtime =response.xpath('//span[@class = "time"]/text()').extract()
        content=response.xpath('//div[@id = "c1_afterplayer"]').extract()
        content=content[0].replace('\t','').replace('\n','').replace('\r','').replace(' ','')
        content=re.findall('>(.*?)<',content)
        contentdata=''
        for i in content:
            contentdata+=i
        content=contentdata
        title=response.meta['title'].replace('\t','').replace('\n','').replace('\r','').replace(' ','')
        app_name='无线新闻'
        pic_url='http://img.tvb.com/inews_web/web/generic_thumbnail.jpg'
        pic_more_url=''
        author=''
        pubTime=publishtime[0].replace('　','')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        describe=''
        if 'greaterchina' in response.url:
            category=u'两岸'.encode('utf-8')
        elif 'world' in response.url:
            category = u'国际'.encode('utf-8')
        elif 'finance' in response.url:
            category= u'财经'.encode('utf-8')
        elif 'sports' in response.url:
            category = u'体育'.encode('utf-8')
        elif 'parliament' in response.url:
            category = u'法庭'.encode('utf-8')
        elif 'focus' in response.url:
            category = u'要闻'.encode('utf-8')
        elif 'instant' in response.url:
            category = u'快讯'.encode('utf-8')
        elif 'programmes' in response.url:
            category = u'专题栏目'.encode('utf-8')
        elif 'local' in response.url:
            category = u'港澳'.encode('utf-8')
        else:
            category = u'首页'.encode('utf-8')
        publishedDate = pubTime
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
        try:
            timeArray = time.strptime(pubTime, "%Y-%m-%d %H:%M")
        except:
            t = pubTime.split(' ')[0]
            timeArray = time.strptime(t, "%Y-%m-%d")
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            self.count = self.count + 1
            item['count'] = self.count
            yield item








