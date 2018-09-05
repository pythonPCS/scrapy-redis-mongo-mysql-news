#coding=utf-8
import scrapy
import json,re
import time
from news.items import NewsItem

class xiangangyizhoukan(scrapy.Spider):
    name = 'xianggangyizhoukan'
    start_urls = [
        'http://www.nextdigital.com.hk/'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        links = response.xpath('//ul[@class="blk_realtime"]/li/a/@href').extract()
        title = response.xpath('//ul[@class="blk_realtime"]/li/a/img/@alt').extract()
        for i in range(len(links)):
            url = links[i]
            yield scrapy.Request(url,meta={
                'title':title[i]
            },callback=self.parse_item)
        links = response.xpath('//ul[@class="blk_daily"]/li/a/@href').extract()
        title = response.xpath('//ul[@class="blk_daily"]/li/a/img/@alt').extract()
        for i in range(len(links)):
            url = links[i]
            yield scrapy.Request(url, meta={
                'title': title[i]
            }, callback=self.parse_item)
        links = response.xpath('//ul[@class="blk_weekly"]/li/a/@href').extract()
        title = response.xpath('//ul[@class="blk_daily"]/li/a/img/@alt').extract()
        for i in range(len(links)):
            url = links[i]
            yield scrapy.Request(url, meta={
                'title': title[i]
            }, callback=self.parse_item)


    def parse_item(self,response):
        app_name = '香港壹周刊'
        pic_url = ''
        describe = ''
        title = response.meta['title']
        publishedDate = response.xpath('//span[@class="last_update"]/text()').extract()[0]
        content = response.xpath('//p/text()').extract()
        contentt = ''
        for i in range(len(content)):
            contentt += content[i]
        content = contentt
        author = ''
        category = '今日'
        pic_more_url = ''
        home_url = 'http://www.nextdigital.com.hk/'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
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
            item['publishedDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timeStamp)))
            yield item



