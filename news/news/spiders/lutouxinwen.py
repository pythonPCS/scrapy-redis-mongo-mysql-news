#coding=utf-8
import scrapy
import time
from news.items import NewsItem

class twpg(scrapy.Spider):
    name = 'lutouxinwen'
    allowed_domains = ['cn.reuters.com']
    start_urls = [
        'https://cn.reuters.com/news/archive/CNTopGenNews?view=page&page=1&pageSize=10', #时事要闻
        'https://cn.reuters.com/news/archive/CNTopGenNews?view=page&page=2&pageSize=10', #时事要闻
        'https://cn.reuters.com/news/archive/CNAnalysesNews?view=page&page=1&pageSize=10',#深度分析
        'https://cn.reuters.com/news/archive/CNAnalysesNews?view=page&page=2&pageSize=10',#深度分析
        'https://cn.reuters.com/news/archive/topic-cn-lifestyle?view=page&page=1&pageSize=10',#生活
        'https://cn.reuters.com/news/archive/topic-cn-lifestyle?view=page&page=2&pageSize=10',#生活
        'https://cn.reuters.com/news/archive/companyNews?view=page&page=1&pageSize=10', #投资
        'https://cn.reuters.com/news/archive/companyNews?view=page&page=2&pageSize=10', #投资
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links_url = response.xpath('//article[@class="story "]/div[@class="story-content"]/a/@href').extract()
        title = response.xpath('//article[@class="story "]/div[@class="story-content"]/a/h3/text()').extract()
        summary = response.xpath('//article[@class="story "]/div[@class="story-content"]/p/text()').extract()
        pic_url = response.xpath('//article[@class="story "]/div[1]/a/img/@src').extract()
        for i in range(0, len(links_url)):
            url = 'https://cn.reuters.com/news' + links_url[i]
            try:
                pic_url1 = pic_url[i]
            except:
                pic_url1 = ''
            yield scrapy.Request(url, meta={
                'title': title[i].replace('\t', '').replace('\n', '').replace('\r', ''),
                'summary': summary[i].replace('\t', '').replace('\n', '').replace('\r', ''),
                'home_url': response.url,
                'pic_url': pic_url1
            }, callback=self.parse_item)

    def parse_item(self, response):
        title = response.meta['title']
        describe = response.meta['summary']
        home_url = response.meta['home_url']
        app_name = u'路透新闻'.encode('utf-8')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_url = response.meta['pic_url']
        content = response.xpath('//meta[@name="description"]/@content').extract()
        content = content[0]
        pubTime = response.xpath('//meta[@name="analyticsAttributes.articleDate"]/@content').extract()
        tt = response.xpath('//div[@class="date_V9eGk"]/text()').extract()[0]
        t1 = tt.split('/')[0]
        t2 = tt.split('/')[1]
        t3 = t1 + t2
        t3 = t3.replace('   ', ' ').replace('AM', '').replace('PM', '').replace('  ','')
        timeStruct = time.strptime(t3, "%B %d, %Y %H:%M")
        pubTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)
        print pubTime
        # pubTime = pubTime[0].split('T')[0]
        pic_more_url = ''
        author = ''
        if 'CNTopGenNews' in home_url:
            category = u'要闻'.encode('utf-8')
        elif 'CNAnalysesNews' in response.url:
            category = u'深度分析'.encode('utf-8')
        elif 'topic-cn-lifestyle' in response.url:
            category = u'生活'.encode('utf-8')
        elif 'companyNews' in response.url:
            category = u'投资'.encode('utf-8')
        else:
            category = u'实时资讯'.encode('utf-8')
        publishedDate = pubTime
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
        # print publishedDate
        # print pubTime
        # t = pubTime.split(' ')[0]
        timeArray = time.strptime(pubTime, "%Y-%m-%d %H:%M:%S")
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            self.count = self.count + 1
            item['count'] = self.count
            yield item
