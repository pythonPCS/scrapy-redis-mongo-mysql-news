#coding=utf-8
import scrapy
import time
import re
from news.items import NewsItem

class djy(scrapy.Spider):
    name = 'dajiyuan'
    allowed_domains = ['epochtimes.com']
    start_urls = [
        'http://www.epochtimes.com/gb/n24hr.htm',    #即时
        'http://www.epochtimes.com/gb/nsc413_2.htm', #要闻
        'http://www.epochtimes.com/gb/nf4830.htm',   #神韵
        'http://www.epochtimes.com/gb/nsc1025.htm',  #评论
        'http://www.epochtimes.com/gb/ncid277.htm',  #中国
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//div[@class="posts column"]/div[1]/a/@href').extract()
        title = response.xpath('//div[@class="posts column"]/div[1]/a/text()').extract()
        pic_url = response.xpath('//div[@class="posts column"]/div[2]/a/img/@data-src').extract()
        summary = response.xpath('//div[@class="content"]/text()').extract()
        if len(links) > 0:
            for i in range(0, len(links)):
                try:
                    summary1 = summary[i].replace('\t','').replace('\n','').replace('\r','')
                except:
                    summary1 = ''
                try:
                    pic_url1 = pic_url[i]
                except:
                    pic_url1 = ''
                url = links[i].replace('\t','').replace('\n','').replace('\r','')
                yield scrapy.Request(url, meta={
                    'title': title[i].replace('\t','').replace('\n','').replace('\r',''),
                    'summary': summary1,
                    'home_url': response.url,
                    'pic_url': pic_url1
                }, callback=self.parse_item, dont_filter=True)
        else:
            links = response.xpath('//div[@class="newyork"]/ul[1]/li/a/@href').extract()
            title = response.xpath('//div[@class="newyork"]/ul[1]/li/a/text()').extract()
            pic_url = ''
            summary = ''
            for i in range(0,len(links)):
                url = links[i]
                yield scrapy.Request(url, meta={
                    'title': title[i].replace('\t', '').replace('\n', '').replace('\r', ''),
                    'summary': summary,
                    'home_url': response.url,
                    'pic_url': pic_url
                }, callback=self.parse_item, dont_filter=True)

    def parse_item(self,response):
        title = response.meta['title']
        describe = response.meta['summary']
        home_url = response.meta['home_url']
        app_name = '大纪元'
        pic_url = response.meta['pic_url']
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        try:
            try:
                pubTime = response.xpath('//div[@class="mbottom10 large-12 medium-12 small-12 columns"]/time/text()').extract()[0]
                pubTime = pubTime.replace(u'更新: ', '').replace('PM', '').replace('AM', '').replace('\t', '').replace('\n', '').replace('\r', '')
            except:
                pubTime = response.xpath('//div[@ class="art-head"]/span/text()').extract()
                pubTime = pubTime[0].split(' ')[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
        except:
            pubTime = time.strftime("%Y-%m-%d") + ' 00:00'
        content = response.xpath('//p').extract()
        contentdata = ''
        for i in range(0, len(content)):
            contentdata += content[i]
        content = re.findall('>(.*?)<', contentdata)
        contentdata = ''
        for i in range(0, len(content)):
            contentdata += content[i]
        content = contentdata
        if 'n24hr' in home_url:
            category = u'即时'.encode('utf-8')
        elif 'nsc413' in home_url:
            category = u'要闻'.encode('utf-8')
        elif 'nsc1025' in home_url:
            category = u'评论'.encode('utf-8')
        elif 'ncid277' in home_url:
            category = u'中国'.encode('utf-8')
        else:
            category = u'神韵'.encode('utf-8')
        author = ''
        pic_more_url = ''
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
        t = pubTime
        try:
            t1 = pubTime.split(' ')[0]
            t2 = pubTime.split(' ')[1]
            t = t1 + ' ' + t2
            timeArray = time.strptime(t, "%Y-%m-%d %H:%M")
        except:
            t = pubTime.split(' ')[0]
            timeArray = time.strptime(t, "%Y-%m-%d")
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            self.count = self.count + 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            yield item
