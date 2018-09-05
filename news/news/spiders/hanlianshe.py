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
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        if 'allheadlines' in response.url:
            category = '滚动'
        elif 'international' in response.url:
            category = '国际'
        else:
            category = '国内'
        url = response.xpath('//div[@class="con_article_list"]/ul/li[1]/a/@href').extract()
        for i in range(len(url)):
            links = url[i]
            yield scrapy.Request(links, meta={
                'category': category
            }, callback=self.parse_item)

    def parse_item(self, response):
        category = response.meta['category']
        title = response.xpath('//h1/text()').extract()[0]
        pic_url = ''
        describe = ''
        app_name = '韩联社'
        content = response.xpath('//div[@id="articleBody"]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '')
        content = re.findall('>(.*?)<',content)
        contentt = ''
        for i in range(len(content)):
            contentt += content[i]
        content = contentt
        publishedDate = response.xpath('//p[@class="publish-time"]/text()').extract()[0].replace(' KST','')
        author = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url = 'http://chinese.yonhapnews.co.kr/'
        pic = response.xpath('//div[@id="articleBody"]').extract()[0]
        Sector = HTML(pic)
        pic_more = Sector.xpath('//img/@src')
        pic_more_url = []
        for i in range(len(pic_more)):
            pic_more_url.append(pic_more[i])
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
        timeArray = time.strptime(publishedDate, "%Y/%m/%d %H:%M")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item
