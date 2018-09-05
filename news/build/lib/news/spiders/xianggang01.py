#coding=utf-8
import scrapy
import json,re,time
from news.items import NewsItem

class xianggang(scrapy.Spider):
    name = 'xianggang01'
    start_urls = [
        'https://www.hk01.com/'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//div[@class="s1lxp17y-1 cHzBvk"]/div/span/a/@href').extract()
        cate = response.xpath('//div[@class="s1lxp17y-1 cHzBvk"]/div/span/a/text()').extract()
        for i in range(len(links)):
            url = 'https://www.hk01.com' + links[i]
            category = cate[i]
            if category == '港聞' or category == "觀點" or category =="國際" or category == "中國" or category=="經濟":
                yield scrapy.Request(url, meta={
                    'category':category
                }, callback=self.parse_item)

    def parse_item(self,response):
        category = response.meta['category']
        links = response.xpath('//div[@class="sc-bwzfXH hxYtSF"]/div/div/span/a/@href').extract()
        for i in range(len(links)):
            url = 'https://www.hk01.com' + links[i]
            yield scrapy.Request(url,meta={
                'category':category
            },callback=self.parse_one)

    def parse_one(self,response):
        category = response.meta['category']
        links = response.xpath('//div[@class="sc-bdVaJa gRrvFh"]/span/a/@href').extract()
        for i in range(len(links)):
            url = 'https://www.hk01.com' + links[i]
            yield scrapy.Request(url, meta={
                'category': category
            }, callback=self.parse_two)

    def parse_two(self,response):
        category = response.meta['category']
        app_name = '香港01'
        describe = ''
        pic_url = ''
        publishedDate = response.xpath('//time/text()').extract()[0]
        home_url = 'https://www.hk01.com/'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        title = response.xpath('//h1/text()').extract()[0]
        pic_more_url = ''
        content = response.xpath('//p/text()').extract()
        contentt = ''
        for i in range(len(content)):
            contentt += content[i]
        content = contentt
        try:
            author = response.xpath('//a[@class="sc-gqjmRU dhKqyP"]/text()').extract()[0]
        except:
            author = ''
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M")
        timeStamp = int(time.mktime(timeArray))
        if timeStamp >= self.timeStamp:
            item['publishedDate'] = time.strftime("%Y-%m-%d %H:%M:%S" ,time.localtime(float(timeStamp)))
            yield item


