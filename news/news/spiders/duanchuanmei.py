#coding=utf-8
import scrapy
import time
import json
import re
from news.items import NewsItem
from scrapy.selector import Selector
from news.DataResource import TransportData
class bbc(scrapy.Spider):
    name='duanchuanmei'
    allowed_domains = ["theinitium.com"]
    start_urls=[
       'https://theinitium.com/channel/feature/',
        'https://theinitium.com/channel/news-brief/',
        'https://theinitium.com/channel/roundtable/',
        'https://theinitium.com/channel/travel/',
        'https://theinitium.com/channel/notes-and-letters/',
        'https://theinitium.com/channel/pick_up/'
    ]
    base_url='https://theinitium.com'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-13', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        links=response.xpath('//li[@class="l-waffle-1 l-waffle-sm-2 l-waffle-md-3 l-waffle-lg-4"]/div[1]/a/@href').extract()
        pic_url=response.xpath('//li[@class="l-waffle-1 l-waffle-sm-2 l-waffle-md-3 l-waffle-lg-4"]/div[1]/a/div/@style').extract()
        title=response.xpath('//li[@class="l-waffle-1 l-waffle-sm-2 l-waffle-md-3 l-waffle-lg-4"]/div[1]/div/div/a/h3/text()').extract()
        summary=response.xpath('//li[@class="l-waffle-1 l-waffle-sm-2 l-waffle-md-3 l-waffle-lg-4"]/div[1]/div/div/p/text()').extract()
        Url=[]
        Pic_url=[]
        Summary=[]
        Title=[]
        for i in range(0,len(links)):
            url=self.base_url + links[i]
            try:
                pic_url =  pic_url[i]
            except:
                pic_url=''
            try:
                summary = summary[i]
            except:
                summary=''

            Url.append(url)
            Title.append(title[i])
            Pic_url.append(pic_url)
            Summary.append(summary)
        links = response.xpath('//li[@class="l-waffle-1 l-waffle-sm-3"]/div[1]/a/@href').extract()
        pic_url = response.xpath('//li[@class="l-waffle-1 l-waffle-sm-3"]/div[1]/a/div/@style').extract()
        title = response.xpath('//li[@class="l-waffle-1 l-waffle-sm-3"]/div[1]/div/div[2]/a/h3/text()').extract()
        summary = response.xpath('//li[@class="l-waffle-1 l-waffle-sm-3"]/div[1]/div/div[2]/p/text()').extract()
        for i in range(0, len(links)):
            url = self.base_url + links[i]
            # print url
            try:
                pic_url = pic_url[i]
            except:
                pic_url = ''
            # print title[i]
            try:
                summary = summary[i]
            except:
                summary = ''
            Url.append(url)
            Title.append(title[i])
            Pic_url.append(pic_url)
            Summary.append(summary)

        for i in range(0,len(Url)):
            yield scrapy.Request(Url[i],meta={
                    'title':Title[i],
                    'pic_url':Pic_url[i],
                    'summary':Summary[i],
                    'home_url':response.url
                },callback=self.parse_item)


    def parse_item(self,response):
        title=response.meta['title']
        pic_url=response.meta['pic_url']
        describe=response.meta['summary']
        home_url=response.meta['home_url']
        app_name='端传媒新闻'
        pubTime=response.xpath('//time[@class="posted-time"]/text()').extract()[0].replace('\t','').replace('\n','').replace('\r','').replace(' ','')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content=response.xpath('//div[@class="p-article__content u-content l-col-12 l-col-lg-9" ]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        try:
            category = response.xpath('//div[@class="p-article__channels"]/span[2]/a/text()').extract()[0]
        except:
            category = response.xpath('//div[@class="p-article__channels"]/span[1]/a/text()').extract()[0]
        pic_more_url=''
        try:
            author=response.xpath('//span[@class="byline u-inline-divider"]/span/text()').extract()[0]
        except:
            author=''

        # print "app名称", app_name
        # print "主图片url", pic_url
        # print "子图片url", pic_more_url
        # print "作者", writer
        # print "详情页地址", response.url
        # print "所属类型", content_type
        # print "标题", title
        # print "描述", summary
        # print "内容", content
        # print "主url", home_url
        # print "发布时间", pubTime
        # print "爬取时间", crawlTime
        #
        # item = NewsItem()
        # item['app_name'] = app_name
        # item['pic_url'] = pic_url
        # item['pic_more_url'] = pic_more_url
        # item['writer'] = writer
        # item['content_url'] = response.url
        # item['content_type'] = content_type
        # item['title'] = title
        # item['summary'] = summary
        # item['content'] = content
        # item['home_url'] = home_url
        # item['pubTime'] = pubTime
        # item['crawlTime'] = crawlTime
        # yield item

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

        item['crawlTime'] = crawlTime
        # existing_title = TransportData.getData('端新闻_b')
        # 符合要求，可以入库的title list
        acceptable_title = []
        # t = pubTime.split(' ')[0]
        timeArray = time.strptime(pubTime, "%Y-%m-%d")
        publishedDate = time.mktime(timeArray)
        # if title not in existing_title:
        if publishedDate >= self.timeStamp:
            acceptable_title.append(title)
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            print "okokokokok"
            self.count += 1
            item['count'] = self.count
            yield item
            # TransportData.transport_data(app_name, pic_url, pic_more_url, author, response.url, category, title,
            #                              describe,
            #                              content,
            #                              home_url, publishedDate, crawlTime)