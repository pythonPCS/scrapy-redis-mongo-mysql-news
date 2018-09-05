#coding=utf-8
import time, json, re
from news.items import NewsItem
import scrapy
from lxml.etree import HTML

class shidaizhoukan(scrapy.Spider):
    name = 'shidaizhoukan'
    start_urls = [
        'http://time.com/section/politics/?page=1',
        'http://time.com/section/politics/?page=2',
        'http://time.com/section/politics/?page=3',
        'http://time.com/section/us/?page=1',
        'http://time.com/section/us/?page=2',
        'http://time.com/section/us/?page=3',
        'http://time.com/section/world/?page=1',
        'http://time.com/section/world/?page=2',
        'http://time.com/section/world/?page=3',
        'http://time.com/section/tech/?page=1',
        'http://time.com/section/tech/?page=2',
        'http://time.com/section/tech/?page=3'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-25', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links =response.xpath('//article/div[1]/div[1]/a/@href').extract()
        title =response.xpath('//article/div[1]/div[1]/a/text()').extract()
        for i in range(len(links)):
            if 'http' not in links[i]:
                url = 'http://time.com' + links[i]
            else:
                url = links[i]
            tit = title[i].replace('\t','').replace('\n','').replace('\r','')
            yield scrapy.Request(url, meta={
                'title': tit,
                'home_url': response.url
            }, callback=self.parse_item)

    def parse_item(self, response):
        title = response.meta['title']
        home_url = response.meta['home_url']
        app_name = '时代周刊'
        author = ''
        pic_url = ''
        describe = ''
        content = response.xpath('//div[@id="article-body"]').extract()
        selator = HTML(content[0])
        content = selator.xpath('//text()')
        content = ''.join(content)
        content = content.replace('\t', '').replace('\n', '').replace('\r', '')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_more_url = ''
        if 'politics' in home_url:
            category = 'Politics'
        elif 'us' in home_url:
            category = 'U.S.'
        elif 'world' in home_url:
            category = 'World'
        elif 'tech' in home_url:
            category = 'Tech'
        else:
            category = 'Politics'
        publishedDate = response.xpath('//div[@class="timestamp published-date padding-12-left"]/text()').extract()[0]
        publishedDate = publishedDate.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
        publishedDate = publishedDate.replace('Updated:','').replace('ET','').replace('EDT','').replace(',','')
        if '2018' in publishedDate:
            publishedDate = publishedDate.split('2018')
            t1 = publishedDate[0]
            publishedDate = '2018' + '-' + t1
        elif '2019' in publishedDate:
            publishedDate = publishedDate.split('2019')
            t1 = publishedDate[0]
            publishedDate = '2019' + '-' + t1
        else:
            publishedDate = '2018-1-01'
        t12 = publishedDate
        if 'June' in t12:
            tt = t12.replace('June','6-')
        elif 'Jun' in t12:
            tt = t12.replace('Jun', '6-')
        elif 'January' in t12:
            tt = t12.replace('January', '1-')
        elif 'Jan' in t12:
            tt = t12.replace('Jan', '1-')
        elif 'February' in t12:
            tt = t12.replace('February', '2-')
        elif 'Feb' in t12:
            tt = t12.replace('Feb', '2-')
        elif 'March' in t12:
            tt = t12.replace('March', '3-')
        elif 'Mar' in t12:
            tt = t12.replace('Mar', '3-')
        elif 'April' in t12:
            tt = t12.replace('April', '4-')
        elif 'Apr' in t12:
            tt = t12.replace('Apr', '4-')
        elif 'May' in t12:
            tt = t12.replace('May', '5-')
        elif 'July' in t12:
            tt = t12.replace('July', '7-')
        elif 'August' in t12:
            tt = t12.replace('August', '8-')
        elif 'Aug' in t12:
            tt = t12.replace('Aug', '8-')
        elif 'September' in t12:
            tt = t12.replace('September', '9-')
        elif 'Sept' in t12:
            tt = t12.replace('Sept', '9-')
        elif 'October' in t12:
            tt = t12.replace('October', '10-')
        elif 'Oct' in t12:
            tt = t12.replace('Oct', '10-')
        elif 'November' in t12:
            tt = t12.replace('November', '11-')
        elif 'Nov' in t12:
            tt = t12.replace('Nov', '11-')
        elif 'December' in t12:
            tt = t12.replace('December', '12-')
        elif 'Dec' in t12:
            tt = t12.replace('Dec', '12-')
        else:
            tt = t12
        publishedDate = tt + ' 00:00:00'
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item
