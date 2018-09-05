#coding=utf-8
import scrapy
import json, re, time
from news.items import NewsItem

class huaerjie(scrapy.Spider):
    name = 'huaerjieyg'
    allow_domains = [
        'https://www.wsj.com/'
    ]
    start_urls = [
        'https://www.wsj.com/',
        'https://www.wsj.com/news/world',
        'https://www.wsj.com/news/us',
        'https://www.wsj.com/news/politics',
        'https://www.wsj.com/news/economy',
        'https://www.wsj.com/news/business',
        'https://www.wsj.com/news/technology',
        'https://www.wsj.com/news/markets',
        'https://www.wsj.com/news/opinion'
    ]

    def parse(self, response):
        links = re.findall('href="https://www.wsj.com/articles/(.*?)"', response.body)
        for i in range(len(links)):
            url = 'https://www.wsj.com/articles/' + links[i]
            yield scrapy.Request(url, meta={
                'home_url': response.url
            }, callback=self.parse_item)

    def parse_item(self, response):
        title = response.xpath('//h1/text()').extract()[0]
        publishedDate = response.xpath('//time/text()').extract()[0]
        pic_url = ''
        describe = ''
        app_name = '华尔街日报英文网'
        home_url = 'https://www.wsj.com/'
        author = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        print "app名称", app_name
        print "主图片url", pic_url
        # print "子图片url", pic_more_url
        print "作者", author
        print "详情页地址", response.url
        # print "所属类型", category
        print "标题", title
        print "描述", describe
        # print "内容", content
        print "主url", home_url
        print "发布时间", publishedDate
        print "爬取时间", crawlTime
