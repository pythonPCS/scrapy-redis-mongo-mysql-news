#-*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from urlparse import urljoin
import json
import time
import re
from news.DataResource import TransportData
from news.items import NewsItem


class dw(Spider):
    name='duoweixinwen'
    start_urls=[
        'http://news.dwnews.com/china/',#中国
        'http://news.dwnews.com/china/list/list1.json',
        'http://news.dwnews.com/global/',#国际
        'http://news.dwnews.com/global/list/list1.json',
        'http://news.dwnews.com/taiwan/',#台湾
        'http://news.dwnews.com/taiwan/list/list1.json',
        'http://news.dwnews.com/hongkong/',#香港
        'http://news.dwnews.com/hongkong/list/list1.json',
        'http://economics.dwnews.com/',#经济
        'http://culture.dwnews.com/history/',#历史
        'http://culture.dwnews.com/history/list/list1.json',
        'http://blog.dwnews.com/',#多维客
        'http://blog.dwnews.com/index.php?r=club%2Fajax_list&catid=0&page=1&type=index',
    ]
    base_url = ""
    count = 0
    number=1
    download_delay = 2
    # a = "2018-03-18 00:00:00"
    # timeArray = time.strptime(a,"%Y-%m-%d %H:%M:%S")
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        try:
            try:
                try:
                    try:
                        #经济
                        links = response.xpath('//div[@class="news-list vikey"]/a/@href').extract()
                        print "123"
                        t= links[1]
                        pic_url =  response.xpath('//div[@class="news-list vikey"]/a/img/@src').extract()
                        title = response.xpath('//div[@class="news-list vikey"]/div[1]/h2/a/text()').extract()
                        decsribe = ''
                        print "####################################"
                        for i in range(0,len(links)):
                            url = links[i]
                            tit = title[i]
                            try:
                                pic = pic_url[i]
                            except:
                                pic = ''
                            desc= decsribe
                            yield Request(url,meta={
                                'title':tit,
                                'pic_url':pic,
                                'describe':desc,
                                'home_url':response.url
                            },callback=self.parse_item,dont_filter=True)
                    except:
                        #json
                        data = json.loads(response.body)
                        print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                        for i in data:
                            tit = i['title']
                            url = i['url']
                            pic = i['relevantPhoto']
                            desc = i['digest']
                            yield Request(url, meta={
                                'title': tit,
                                'pic_url': pic,
                                'describe': desc,
                                'home_url': response.url
                            }, callback=self.parse_item,dont_filter=True)
                except:
                    #中国,国际，台湾，香港
                    links = response.xpath('//div[@class="lisbox"]/ul/li/div[1]/a/@href').extract()
                    tt = links[1]
                    title = response.xpath('//div[@class="lisbox"]/ul/li/div[1]/a/text()').extract()
                    pic_url = response.xpath('//div[@class="lisbox"]/ul/li/div[2]/a/img/@src').extract()
                    decsribe = response.xpath('//div[@class="lisbox"]/ul/li/div[3]/p/text()').extract()
                    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                    for i in range(0,len(links)):
                        url = links[i]
                        tit = title[i]
                        pic = pic_url[i]
                        desc = decsribe[i]
                        yield Request(url, meta={
                            'title': tit,
                            'pic_url': pic,
                            'describe': desc,
                            'home_url': response.url
                        }, callback=self.parse_item)
            except:
                #多维客
                links    = response.xpath('//li[@class="vikey"]/div[1]/a/@href').extract()
                title    = response.xpath('//li[@class="vikey"]/div[1]/a/text()').extract()
                pic_url  = response.xpath('//li[@class="vikey"]/div[2]/a/img/@src').extract()
                decsribe = response.xpath('//li[@class="vikey"]/div[3]/p/text()').extract()
                print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
                for i in range(0, len(links)):
                    url = links[i]
                    tit = title[i]
                    try:
                        pic = pic_url[i]
                    except:
                        pic = ''
                    try:
                        desc = decsribe[i]
                    except:
                        desc = ''
                    yield Request(url, meta={
                        'title': tit,
                        'pic_url': pic,
                        'describe': desc,
                        'home_url': response.url
                    }, callback=self.parse_item)
        except:
            #历史
            print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
            links = response.xpath('//div[@class="main"]/div/ul/li/div[1]/a/@href').extract()
            pic_url = response.xpath('//div[@class="main"]/div/ul/li/div[1]/a/text()').extract()
            title = response.xpath('//div[@class="main"]/div/ul/li/div[2]/h3/a/text()').extract()
            decsribe = response.xpath('//div[@class="main"]/div/ul/li/div[2]/p/text()').extract()
            for i in range(0, len(links)):
                url = links[i]
                tit = title[i]
                try:
                    pic = pic_url[i]
                except:
                    pic = ''
                try:
                    desc = decsribe[i]
                except:
                    desc = ''
                yield Request(url, meta={
                    'title': tit,
                    'pic_url': pic,
                    'describe': desc,
                    'home_url': response.url
                }, callback=self.parse_item)


    def parse_item(self,response):
        title=response.meta['title']
        pic_url=response.meta['pic_url']
        describe=response.meta['describe']
        try:
            publishedDate = response.xpath('//div[@class="r"]/text()').extract()[0]
        except:
            publishedDate = response.xpath('//div[@class="time"]/text()').extract()[0]
        home_url=response.meta['home_url']
        app_name='多维新闻'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if 'china' in home_url:
            category=u'中国'.encode('utf-8')
        elif 'global' in home_url:
            category=u'国际'.encode('utf-8')
        elif 'hongkong' in home_url:
            category=u'香港'.encode('utf-8')
        elif 'taiwan' in home_url:
            category=u'台湾'.encode('utf-8')
        elif 'economics' in home_url:
            category =u'经济'.encode('utf-8')
        elif 'history' in home_url:
            category = u'历史'.encode('utf-8')
        else:
            category = u'多维客'.encode('utf-8')
        try:
            try:
                try:
                    content=response.xpath('//div[@class="dia-lead-one"]').extract()
                    contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                    content = re.findall('>(.*?)<', contentt)
                    contentdata = ''
                    for i in range(0, len(content)):
                        contentdata += content[i]
                    contentt = contentdata
                    pic_more_url=re.findall('src="(.*?)"',contentt)
                    pic_more_url1 = []
                    for i in range(0, len(pic_more_url)):
                        pic_more_url1.append(pic_more_url[i])
                    pic_more_url = str(set(pic_more_url1))
                except:
                    content = response.xpath('//div[@class="container"]').extract()
                    contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                    content = re.findall('>(.*?)<', contentt)
                    contentdata = ''
                    for i in range(0, len(content)):
                        contentdata += content[i]
                    contentt = contentdata
                    pic_more_url = re.findall('src="(.*?)"', contentt)
                    pic_more_url1 = []
                    for i in range(0, len(pic_more_url)):
                        pic_more_url1.append(pic_more_url[i])
                    pic_more_url = str(set(pic_more_url1))
            except:
                content=response.xpath('//div[@class="captions"]').extract()
                contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                content = re.findall('>(.*?)<', contentt)
                contentdata = ''
                for i in range(0, len(content)):
                    contentdata += content[i]
                contentt = contentdata
                pic_more_url=response.xpath('//div[@class="bigImgs"]/img/@src').extract()
                pic_more_url1 = []
                for i in range(0, len(pic_more_url)):
                    pic_more_url1.append(pic_more_url[i])
                pic_more_url = str(set(pic_more_url1))
        except:
            content = response.xpath('//p').extract()
            contentt = ''
            for i in range(0,len(content)):
                contentt += content[i]
            pic_more_url = ''
        try:
            try:
                writer=response.xpath('//div[@class="nw"]/text()').extract()
                author=writer[0]
            except:
                writer=response.xpath('//div[@class="author"]/text()').extract()
                author=writer[0]
        except:
            author=''

        print "app名称", app_name
        print "主图片url", pic_url
        print "子图片url", pic_more_url
        print "作者", author
        print "详情页地址", response.url
        print "所属类型", category
        print "标题", title
        print "描述", describe
        print "内容", contentt
        print "主url", home_url
        print "发布时间", publishedDate
        print "爬取时间", crawlTime
        self.count = self.count + 1
        url=response.url
        item = NewsItem()
        item['app_name'] = app_name
        item['count'] = self.count
        item['pic_url'] = pic_url
        item['pic_more_url'] = ""
        item['author'] = author
        item['url'] = url
        item['category'] = category
        item['title'] = title
        item['describe'] = describe
        item['content'] = contentt
        item['home_url'] = home_url
        item['publishedDate'] = publishedDate
        item['crawlTime'] = crawlTime
        try:
            timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
        except:
            timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M")

        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            self.count = self.count + 1
            item['count'] = self.count
            print "okokokokok"
            yield item

        # yield item
        # TransportData.transport_data(app_name, pic_url, pic_more_url, author, response.url, category, title, describe,
        #                              contentt,
        #                              home_url, publishedDate, crawlTime)
