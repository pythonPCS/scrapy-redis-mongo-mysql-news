#coding=utf-8
import scrapy, re, time, json
from news.items import NewsItem
from lxml.etree import HTML

class yindushibao(scrapy.Spider):
    name = 'yindushibaoyingwen'
    start_urls = [
        'https://timesofindia.indiatimes.com/topic/Xi-Jinping'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-01', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//ul[@itemprop="ItemList"]/li/div/a/@href').extract()
        title = response.xpath('//ul[@itemprop="ItemList"]/li/div/a/span[1]/text()').extract()
        for i in range(len(links)):
            if '' not in links:
                url = 'https://timesofindia.indiatimes.com' + links[i]
            else:
                url = links[i]
            yield scrapy.Request(url, meta={
                'title': title[i]
            }, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        app_name = '印度时报'
        describe = ''
        author = ''
        pic_url = ''
        title = response.meta['title'].replace('\t', '').replace('\n', '').replace('\r', '')
        publishedDate = response.xpath('//time/@datetime').extract()[0]
        publishedDate = publishedDate.split('+')[0].replace('T',' ')
        content = response.xpath('//div[@class="section1"]').extract()
        selator = HTML(content[0])
        content = selator.xpath('//text()')
        content = ''.join(content)
        content = content.replace('\t', '').replace('\n', '').replace('\r', '')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url = 'https://timesofindia.indiatimes.com'
        pic_more_url = ''
        category = 'World'
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