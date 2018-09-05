#coding=utf-8
import scrapy
import re, time, json
from news.items import NewsItem

class jingjixueren(scrapy.Spider):
    name = 'jingjixueren'
    start_urls = [
        'https://www.economist.com/latest-updates',
        'https://www.economist.com/sections/leaders',
        'https://www.economist.com/sections/briefings',
        'https://www.economist.com/sections/united-states',
        'https://www.economist.com/sections/americas',
        'https://www.economist.com/sections/asia',
        'https://www.economist.com/sections/china',
        'https://www.economist.com/sections/middle-east-africa',
        'https://www.economist.com/sections/europe',
        'https://www.economist.com/sections/britain',
        'https://www.economist.com/sections/international',
        'https://www.economist.com/sections/business-finance',
        'https://www.economist.com/sections/economics',
        'https://www.economist.com/sections/science-technology'
    ]

    def parse(self, response):
        links = response.xpath('//div[@class="teaser-list"]/article/a/@href').extract()
        for i in range(len(links)):
            url = 'https://www.economist.com' + links[i]
            yield scrapy.Request(url,meta={
                'home_url':response.url
            }, callback=self.parse_item, dont_filter=True)

    def parse_item(self,response):
        app_name = '经济学人'
        home_url = response.meta['home_url']
        author = ''
        pic_url = ''
        title = response.xpath('//h1').extract()[0]
        title = title.replace('\t', '').replace('\n', '').replace('\r', '')
        title = re.findall('>(.*?)<', title)
        tit = ''
        for i in range(len(title)):
            tit += title[i]
        title = tit
        publishedDate = response.xpath('//time/text()').extract()[0]
        content = response.xpath('//div[@class="blog-post__text"]/p/text()').extract()
        contentt = ''
        for i in range(len(content)):
            contentt += content[i]
        content = contentt
        content = content.replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        describe = ''
        pic_more_url = ''
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

