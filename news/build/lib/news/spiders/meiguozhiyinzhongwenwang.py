#coding=utf-8
import scrapy
import time,re,json
from news.items import NewsItem

class meiguozhiyin(scrapy.Spider):
    name = 'meiguozhiyinzhongwenwang'
    start_urls = [
        'https://www.voachinese.com/z/1746',#美国
        'https://www.voachinese.com/z/1757',#中国
        'https://www.voachinese.com/z/1769',#台湾
        'https://www.voachinese.com/z/1755',#港澳
        'https://www.voachinese.com/z/1758',#法律
        'https://www.voachinese.com/z/1740',#国际
        'https://www.voachinese.com/z/1748',#经济
        'https://www.voachinese.com/z/1776',#美中关系
        'https://www.voachinese.com/z/5403',#川金会
        'https://www.voachinese.com/s?k=%E4%B9%A0%E8%BF%91%E5%B9%B3&tab=all&pi=1&r=any&pp=10'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-24', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        if '1746' in response.url:
            category = '美国'
        elif '1757' in response.url:
            category = '中国'
        elif '1769' in response.url:
            category = '台湾'
        elif '1755' in response.url:
            category = '港澳'
        else:
            category = '新闻'

        links = response.xpath('//ul[@id="ordinaryItems"]/li/div[1]/div/a/@href').extract()
        title = response.xpath('//ul[@id="ordinaryItems"]/li/div[1]/div/a/h4/span/text()').extract()
        cate = response.xpath('//ul[@id="ordinaryItems"]/li/div[1]/div/a/p/text()').extract()
        for i in range(len(links)):
            url = 'https://www.voachinese.com' + links[i]
            tit = title[i]
            desc = cate[i]
            print tit
            print url
            yield scrapy.Request(url, meta={
                'title': tit,
                'describe': desc,
                'category': category
            }, callback=self.parse_item)

    def parse_item(self, response):
        title = response.meta['title']
        describe = response.meta['describe']
        app_name = '美国之音中文网'
        pubt = response.xpath('//time/text()').extract()[0].replace('\t', '').replace('\n', '').replace('\r', '')
        publishedDate = pubt.replace('年', '-').replace('月', '-').replace('日', '')
        pic_url = ''
        author = ''
        home_url = 'https://www.voachinese.com'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content = response.xpath('//p/text()').extract()
        contentt = ''
        for i in range(len(content)):
            contentt += content[i]
        content = contentt.replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        pic_more_url = ''
        category = response.meta['category']
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item
