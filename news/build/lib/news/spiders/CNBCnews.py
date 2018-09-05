#coding=utf-8
import time, re, json, scrapy
from news.items import NewsItem
from lxml.etree import HTML

class cbnc(scrapy.Spider):
    name = 'cnbcnews'
    start_urls = [
        'https://www.cnbc.com/us-news/?page=1',
        'https://www.cnbc.com/us-news/?page=2',
        'https://www.cnbc.com/investing/?page=1',
        'https://www.cnbc.com/investing/?page=2',
        'https://www.cnbc.com/technology/?page=1',
        'https://www.cnbc.com/technology/?page=2'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-01', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//ul[@id="pipeline_assetlist_0"]/li/div/div/a/@href').extract()
        title = response.xpath('//ul[@id="pipeline_assetlist_0"]/li/div/div/a/text()').extract()
        for i in range(len(links)):
            if 'http' not in links[i]:
                url = 'https://www.cnbc.com' + links[i]
            else:
                url = links[i]
            yield scrapy.Request(url, meta={
                'title': title[i],
                'home_url': response.url
            }, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        app_name = 'CNBC'
        describe = ''
        author = ''
        pic_url = ''
        title = response.meta['title'].replace('\t', '').replace('\n', '').replace('\r', '').replace('                                 ','')
        try:
            publishedDate = response.xpath('//time/@datetime').extract()[0]
            publishedDate = publishedDate.replace('T', ' ').replace('-0400','')
        except:
            publishedDate = '2018-01-01 01:01:01'
        content = response.xpath('//article').extract()
        selator = HTML(content[0])
        content = selator.xpath('//text()')
        content = ''.join(content)
        content = content.replace('\t', '').replace('\n', '').replace('\r', '')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url = response.meta['home_url']
        pic_more_url = selator.xpath('//img/@src')
        pic_more_urll = []
        for i in range(len(pic_more_url)):
            pic_more_urll.append(pic_more_url[i])
        pic_more_url = str(pic_more_urll)
        if 'us-news' in home_url:
            category = 'us-news'
        elif 'investing' in home_url:
            category = 'investing'
        elif 'technology' in home_url:
            category = 'technology'
        else:
            category = 'news'
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
            yield item
