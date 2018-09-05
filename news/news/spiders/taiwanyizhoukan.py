#coding=utf-8
import scrapy
import json,re
import time
from news.items import NewsItem

class taiwanyizhoukan(scrapy.Spider):
    name = 'taiwanyizhoukan'
    Ttime = int(round(time.time() * 1000))
    start_urls = [
        'http://www.nextmag.com.tw/breakingnews/mosthit',#热门
        'http://www.nextmag.com.tw/section/getNext/mosthit/0/10/2/20/?&_=%s'%Ttime,
        'http://www.nextmag.com.tw/breakingnews/topic',#推荐
        'http://www.nextmag.com.tw/section/getNext/117/0/10/2/20/?&_=%s'%Ttime,
        'http://www.nextmag.com.tw/breakingnews/business',
        'http://www.nextmag.com.tw/section/getNext/112/0/10/2/20/?&_=%s'%Ttime,
        'http://www.nextmag.com.tw/breakingnews/politics',
        'http://www.nextmag.com.tw/section/getNext/108/0/10/2/20/?&_=%s'%Ttime,
        'http://www.nextmag.com.tw/breakingnews/international',
        'http://www.nextmag.com.tw/section/getNext/111/0/10/2/20/?&_=%s'%Ttime,
        'http://www.nextmag.com.tw/breakingnews/latest',
        'http://www.nextmag.com.tw/section/getNext/0/0/10/2/20/?&_=%s'%Ttime,
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//li[@class="video"]/a/@href').extract()
        title = response.xpath('//li[@class="video"]/a/div[2]/div/h3/text()').extract()
        piccc = response.xpath('//li[@class="video"]/a/div[1]/span/@style').extract()
        for i in range(len(links)):
            url = 'http://www.nextmag.com.tw' + links[i]
            try:
                pic = piccc[i].replace('background-image:url(','').replace(');','')
            except:
                pic = ''
            yield scrapy.Request(url,meta={
                'title':title[i],
                'pic':pic
            },callback=self.parse_item,dont_filter=True)

    def parse_item(self,response):
        title = response.meta['title']
        pic_url = response.meta['pic']
        app_name = '台湾壹周刊'
        describe = ''
        author = ''
        home_url = 'http://www.nextmag.com.tw'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_more_url = ''
        publishedDate = response.xpath('//time[@class="time"]/text()').extract()[0]
        publishedDate = publishedDate.replace('年','-').replace('月','-').replace('日','')
        content = response.xpath('//p/text()').extract()
        contentt = ''
        for i in range(len(content)):
            contentt += content[i]
        content = contentt
        category = response.xpath('//div[@class="category"]/span/text()').extract()[0]
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


