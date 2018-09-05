#coding=utf-8
import scrapy
import json,re,time
from news.items import NewsItem
from lxml.etree import HTML

class hanlian(scrapy.Spider):
    name = 'hanlianshe'
    start_urls = [
        'http://chinese.yonhapnews.co.kr/allheadlines/0200000001.html',#滚动
        'http://chinese.yonhapnews.co.kr/international/0306000001.html',#国际
        'http://chinese.yonhapnews.co.kr/domestic/0406000001.html',#国内
    ]

    def parse(self, response):
        url = response.xpath('//div[@class="con_article_list"]/ul/li[1]/a/@href').extract()
        for i in range(len(url)):
            links = url[i]
            yield scrapy.Request(links,callback=self.parse_item)

    def parse_item(self, response):
        title = response.xpath('//h1/text()').extract()[0]
        pic_url = ''
        describe = ''
        app_name = '韩联社'
        content = response.xpath('//div[@id="articleBody"]/p/text()')
        contentt = ''
        for i in range(len(contentt)):
            contentt += content[i]
        content = contentt
        publishedDate = response.xpath('//p[@class="publish-time"]/text()').extract()[0]
        author = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url = 'http://chinese.yonhapnews.co.kr/'
        pic = response.xpath('//div[@id="articleBody"]').extract()[0]
        Sector = HTML(pic)
        pic_more = Sector.xpath('//img/@src')
        pic_more_url = []
        for i in range(len(pic_more)):
            pic_more_url.append(pic_more[i])
        category = ''
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