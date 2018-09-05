#coding=utf-8
import scrapy
import json, time, re
from news.items import NewsItem

class afp(scrapy.Spider):
    name = 'afp'
    page = 1
    start_urls = [
        'http://www.afpbb.com/list/latest?p=1',
        'http://www.afpbb.com/list/latest?p=2',
        'http://www.afpbb.com/list/latest?p=3',
        'http://www.afpbb.com/list/latest?p=4',
        'http://www.afpbb.com/list/latest?p=5',
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//li[@class="thumb-list"]/a/@href').extract()
        pic_url = response.xpath('//li[@class="thumb-list"]/a/div[1]/img/@src').extract()
        for i in range(len(links)):
            url = links[i]
            try:
                pic = pic_url[i]
            except:
                pic = ''
            yield scrapy.Request(url, meta={
                'pic_url': pic
            },callback=self.parse_item)

    def parse_item(self,response):
        title = response.xpath('//h1/text()').extract()[0]
        pic_url = response.meta['pic_url']
        describe = ''
        publishedDate = response.xpath('//span[@class="day"]/text()').extract()
        publishedDate = publishedDate[0].replace('年', '-').replace('月', '-').replace('日', '').replace('　','')
        app_name = 'AFP news'
        author = ''
        home_url = 'http://www.afpbb.com'
        category = 'Latest'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_more_url = ''
        content = response.xpath('//div[@class="article-body clear"]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        # print "app名称", app_name
        # print "主图片url", pic_url
        # print "子图片url", pic_more_url
        # print "作者", author
        # print "详情页地址", response.url
        # print "所属类型", category
        # print "标题", title
        # print "描述", describe
        # print "内容", content
        # print "主url", home_url
        print "发布时间", publishedDate
        # print "爬取时间", crawlTime
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item

