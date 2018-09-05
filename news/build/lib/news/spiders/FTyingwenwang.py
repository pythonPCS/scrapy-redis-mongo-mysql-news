#coding=utf-8
import json
import scrapy
import time,re,time
from news.items import NewsItem
from news.DataResource import TransportData

class ft(scrapy.Spider):
    name = 'ftyingwenwang'
    start_urls = [
        'https://www.ft.com/world?format=&page=1',#world
        'https://www.ft.com/world?format=&page=2',#world
        'https://www.ft.com/world/us?format=&page=1',#US
        'https://www.ft.com/world/us?format=&page=2',#US
        'https://www.ft.com/companies?format=&page=1',#COMPANIES
        'https://www.ft.com/companies?format=&page=2',#COMPANIES
        'https://www.ft.com/markets?format=&page=1',#MARKETS
        'https://www.ft.com/markets?format=&page=2',#MARKETS
        'https://www.ft.com/opinion?format=&page=1',#OPINION
        'https://www.ft.com/opinion?format=&page=2',#OPINION
        'https://www.ft.com/work-careers?format=&page=1',#WORK & CAREERS
        'https://www.ft.com/work-careers?format=&page=2',#WORK & CAREERS
    ]

    def parse(self, response):
        links = response.xpath('//ul[@class="o-teaser-collection__list"]/li/div[2]/div/div/div[1]/div[2]/a/@href').extract()
        title = response.xpath('//ul[@class="o-teaser-collection__list"]/li/div[2]/div/div/div[1]/div[2]/a/text()').extract()
        #descr = response.xpath('//ul[@class="o-teaser-collection__list"]/li/div[2]/div/div/div[1]/p/text()').extract()
        #pic = response.xpath('//ul[@class="o-teaser-collection__list"]/li/div[2]/div/div/div[2]/a/div/img/@data-srcset').extract()
        for i in range(len(links)):
            url = 'https://www.ft.com' + links[i]
            tit = title[i]
            # describe = descr[i]
            # pic_url = pic[i]
            # print url
            # print tit
            # print describe
            # print pic_url
            yield scrapy.Request(url, meta={
                'title':tit,
                'home_url':response.url
            }, callback=self.parse_item)

    def parse_item(self,response):
        title = response.meta['title']
        home_url = response.meta['home_url']
        author = ''
        pic_url = ''
        describe = ''
        category = ''
        app_name = 'FT英文网'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print "app名称", app_name
        print "主图片url", pic_url
        # print "子图片url", pic_more_url
        print "作者", author
        print "详情页地址", response.url
        print "所属类型", category
        print "标题", title
        print "描述", describe
        # print "内容", content
        print "主url", home_url
        # print "发布时间", publishedDate
        print "爬取时间", crawlTime