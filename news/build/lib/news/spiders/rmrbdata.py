#-*- coding: utf-8 -*-
from scrapy.spider import Spider
import scrapy
from urlparse import urljoin
from scrapy.selector import Selector
from scrapy.http import Request
import time
import json
#from selenium import selenium
import re
import sys
# 全部爬取
from news.DataResource import TransportData
from news.items import NewsItem
reload(sys)
sys.setdefaultencoding('utf8')

class lwl(Spider):
    name='rmrbdata'
    allowed_domains=['people.com.cn']
    start_urls=[
        'http://world.people.com.cn/',  #国际
        'http://finance.people.com.cn/',#财经
        'http://tw.people.com.cn/',#台湾
        'http://military.people.com.cn/',#军事
        'http://opinion.people.com.cn/',#观点
        'http://politics.people.com.cn/',#时政
        'http://leaders.people.com.cn/',#领导
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        base_url = str(response.url).split('/index')[0]
        try:
            try:
                try:
                    title     = response.xpath('//div[@class=" hdNews clearfix"]/p/strong/a/text()').extract()
                    links_url = response.xpath('//div[@class=" hdNews clearfix"]/p/strong/a/@href').extract()
                    describe  = response.xpath('//div[@class=" hdNews clearfix"]/p/em/a/text()').extract()
                    tt = title[0]
                    for j in range(0,len(title)):
                        if 'http' not in links_url[j]:
                            url = base_url + links_url[j]
                        else:
                            url = links_url[j]
                        yield scrapy.Request(url, meta={
                            'title': title[j],
                            'describe': describe[j],
                            'home_url': response.url
                        }, callback=self.parse_item,dont_filter=True)
                except:
                    title     = response.xpath('//div[@class="hdNews clearfix"]/p/strong/a/text()').extract()
                    links_url = response.xpath('//div[@class="hdNews clearfix"]/p/strong/a/text()').extract()
                    describe  = response.xpath('//div[@class="hdNews clearfix"]/p/em/a/text()').extract()
                    tt = title[0]
                    for j in range(0, len(title)):
                        if 'http' not in links_url[j]:
                            url = base_url + links_url[j]
                        else:
                            url = links_url[j]
                        yield scrapy.Request(url, meta={
                            'title': title[j],
                            'describe': describe[j],
                            'home_url': response.url
                        }, callback=self.parse_item,dont_filter=True)
            except:
                # print "第三次"
                title     = response.xpath('//div[@class=" hdNews clearfix"]/div/h5/a/text()').extract()
                links_url = response.xpath('//div[@class=" hdNews clearfix"]/div/h5/a/@href').extract()
                describe  = response.xpath('//div[@class=" hdNews clearfix"]/div/em/a/text()').extract()
                tt = title[0]
                for j in range(0, len(title)):
                    if 'http' not in links_url[j]:
                        url = base_url + links_url[j]
                    else:
                        url = links_url[j]
                    yield scrapy.Request(url, meta={
                        'title': title[j],
                        'describe': describe[j],
                        'home_url': response.url
                    }, callback=self.parse_item,dont_filter=True)
        except:
            # print "第四次"
            title = response.xpath('//div[@class="hdNews clearfix"]/div/h5/a/text()').extract()
            links_url = response.xpath('//div[@class="hdNews clearfix"]/div/h5/a/@href').extract()
            describe = response.xpath('//div[@class="hdNews clearfix"]/div/em/a/text()').extract()
            tt = title[0]
            for j in range(0, len(title)):
                if 'http' not in links_url[j]:
                    url = base_url + links_url[j]
                else:
                    url = links_url[j]
                try:
                    describ = describe[j]
                except:
                    describ = ''
                yield scrapy.Request(url, meta={
                    'title': title[j],
                    'describe': describ,
                    'home_url': response.url
                }, callback=self.parse_item,dont_filter=True)


    def parse_item(self,response):
        title = response.meta['title']
        describe = response.meta['describe']
        home_url = response.meta['home_url']
        app_name = '人民日报'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        try:
            pubTime = response.xpath('//div[@class="box01"]/div[1]/text()').extract()[0]
            pubTime = pubTime.replace('来源：','').replace('  ','').replace('年','-').replace('月','-').replace('日',' ')
        except:
            pubTime =re.findall(r'n1/(.*?)/(.*?)/',str(response.url))
            # print pubTime
            pub1 = pubTime[0][0]
            pub2 = pubTime[0][1]
            pub3 = re.findall('\d{2}',pub2)
            pubTime = pub1 + '-' + pub3[0]+'-'+pub3[1]
        try:
            try:
                content = response.xpath('//div[@class="box_con"]').extract()
                contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                content = re.findall('>(.*?)<', contentt)
                contentdata = ''
                for i in content:
                    contentdata += i
                content = contentdata
                pic_more_url = re.findall('src="(.*?)"',contentt)
                pic_more_url1 = []
                for i in range(0,len(pic_more_url)):
                    if 'http' not in pic_more_url[i]:
                        pic_more_urlt = str(response.url).split('.cn/')[0] + '.cn' + pic_more_url[i]
                        pic_more_url1.append(pic_more_urlt)
                    else:
                        pic_more_url1.append(pic_more_url[i])
                pic_more_url = str(set(pic_more_url1))
            except:
                content = response.xpath('//div[@id="picG"]').extract()
                contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                content = re.findall('>(.*?)<', contentt)
                contentdata = ''
                for i in content:
                    contentdata += i
                content = contentdata
                pic_more_url = re.findall('src="(.*?)"', contentt)
                pic_more_url1 = []
                for i in range(0,len(pic_more_url)):
                    if 'http' not in pic_more_url[i]:
                        pic_more_urlt = str(response.url).split('.cn/')[0] + '.cn' + pic_more_url[i]
                        pic_more_url1.append(pic_more_urlt)
                    else:
                        pic_more_url1.append(pic_more_url[i])
                pic_more_url = str(set(pic_more_url1))

        except:
            content= response.xpath('//div[@class="show_text"]').extract()
            contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('>(.*?)<', contentt)
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
            pic_more_url = re.findall('src="(.*?)"', contentt)
            pic_more_url1 = []
            for i in range(0, len(pic_more_url)):
                if 'http' not in pic_more_url[i]:
                    pic_more_urlt = str(response.url).split('.cn/')[0] + '.cn' + pic_more_url[i]
                    pic_more_url1.append(pic_more_urlt)
                else:
                    pic_more_url1.append(pic_more_url[i])
            pic_more_url = str(set(pic_more_url1))

        author = ''
        category = '首页新闻'
        pic_url = ''
        try:
            timeArray = time.strptime(pubTime, "%Y-%m-%d %H:%M")
            timenum = int(time.mktime(timeArray))
        except:
            timeArray = time.strptime(pubTime, "%Y-%m-%d")
            timenum = int(time.mktime(timeArray))
        accept_title =[]
        if timenum > self.timeStamp:
            accept_title.append(title)
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
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
            self.count += 1
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
            item['count'] = self.count
            yield item
        if len(accept_title) > 0:
            self.number += 1
            if self.number <= 5:
                if 'index' not in home_url:
                    url = home_url + 'index2.html'
                    yield scrapy.Request(url,callback=self.parse)
                else:
                    numt = re.findall('\d+',home_url)[0]
                    num = str(int(numt) + 1)
                    url = str(home_url).replace(numt,num)
                    yield scrapy.Request(url,callback=self.parse,dont_filter=True)