#-*- coding: utf-8 -*-
from scrapy.spiders import Spider
import time
from news.items import NewsItem

class toutiaocaijing(Spider):
    name = 'toutiaocaijing'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    start_urls = [
        'http://iphone.headlinefinance.hk/xml/2018/%s/finance_instant.xml'%time_str.replace('-',''),             #即市新闻
        'http://iphone.headlinefinance.hk/xml/2018/%s/finance_daily.xml'%time_str.replace('-',''),               #日报新闻
        'http://iphone.headlinefinance.hk/xml/2018/%s/finance_investment_columnist.xml'%time_str.replace('-',''),#投资专栏&名家精选
        'http://iphone.headlinefinance.hk/xml/2018/%s/finance_warrants.xml'%time_str.replace('-',''),            #轮商精选
    ]


    def parse(self, response):
        links = response.xpath('//new/id/text()').extract()
        title = response.xpath('//new/title/text()').extract()
        published = response.xpath('//new/publishdate/text()').extract()
        description = response.xpath('//new/short_description/text()').extract()
        contentt =  response.xpath('//new/description/text()').extract()
        author = ''
        pic_url = ''
        pic_more_url = ''
        app_name = u'头条财经'.encode('utf-8')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if 'finance_instant' in response.url:
            category = u'即市新闻'.encode('utf-8')
        elif 'finance_daily' in response.url:
            category = u'日报新闻'.encode('utf-8')
        elif 'finance_investment_columnist' in response.url :
            category = u'投资专栏'.encode("utf-8")
        else:
            category = u'轮商精选'.encode('utf-8')
        for i in range(0,len(links)):
            tit = title[i]
            publishedDate = published[i]
            describe = description[i]
            content = contentt[i]
            self.count = self.count + 1
            item = NewsItem()
            item['app_name'] = app_name
            item['count'] = self.count
            item['pic_url'] = pic_url
            item['pic_more_url'] = pic_more_url
            item['author'] = author
            item['url'] = response.url
            item['category'] = category
            item['title'] = tit
            item['describe'] = describe
            item['content'] = content.replace('\t', '').replace('\n', '').replace('\r', '')
            item['home_url'] = response.url
            item['publishedDate'] = publishedDate
            item['crawlTime'] = crawlTime
            print publishedDate
            try:
                timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
            except:
                timeArray = time.strptime(publishedDate, "%Y-%m-%d")
            publishedDate = time.mktime(timeArray)
            if publishedDate >= self.timeStamp:
                publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
                item['publishedDate'] = publishedDate
                yield item

