#coding=utf-8
import scrapy
import time
import json
import re
from news.items import NewsItem
from scrapy.selector import Selector
from news.DataResource import TransportData
class rfa(scrapy.Spider):
    name='xdrbnews'
    allowed_domains = ["stheadline.com"]
    start_urls = [
        'http://std.stheadline.com/daily/daily.php',
    ]
    base_url = 'http://std.stheadline.com/daily/'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//ul[@class="nav"]/li/ul/li/a/@href').extract()
        for i in range(0,len(links)):
            url = links[i]
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self,resposne):
        links = resposne.xpath('//div[@class="module-wrap none-thumb underline"]/a/@href').extract()
        title = resposne.xpath('//div[@class="module-wrap none-thumb underline"]/a/div[@class="module-detail"]/div[@class="title"]/text()').extract()
        pic_url = resposne.xpath('//div[@class="module-wrap none-thumb underline"]/a/div[@class="module-thumb"]/div[@class="img"]/img/@src').extract()
        summary = resposne.xpath('//div[@class="module-wrap none-thumb underline"]/a/div[@class="module-detail"]/div[@class="des"]/text()').extract()
        Url = []
        Title = []
        Pic_url = []
        Summary = []
        for i in range(0, len(title)):
            try:
                Url.append(links[i])
                Title.append(title[i])
                Pic_url.append(pic_url[i])
                Summary.append(summary[i].replace('\t','').replace('\n','').replace('\r','').replace(' ',''))
            except:
                Url.append(links[i])
                Title.append(title[i])
                Pic_url.append(' ')
                Summary.append(summary[i].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', ''))
        links = resposne.xpath('//div[@class="module-wrap thumb-pull-right underline"]/a/@href').extract()
        title = resposne.xpath('//div[@class="module-wrap thumb-pull-right underline"]/a/div[@class="module-detail"]/div[@class="title"]/text()').extract()
        pic_url = resposne.xpath('//div[@class="module-wrap thumb-pull-right underline"]/a/div[@class="module-thumb"]/div[@class="img"]/img/@src').extract()
        summary = resposne.xpath('//div[@class="module-wrap thumb-pull-right underline"]/a/div[@class="module-detail"]/div[@class="des"]/text()').extract()
        for i in range(0, len(title)):
            try:
                Url.append(links[i])
                Title.append(title[i])
                Pic_url.append(pic_url[i])
                Summary.append(summary[i].replace('\t','').replace('\n','').replace('\r','').replace(' ',''))
            except:
                Url.append(links[i])
                Title.append(title[i])
                Pic_url.append(' ')
                Summary.append(summary[i].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', ''))
        for i in range(0, len(Url)):
            try:
                url = self.base_url + Url[i]
                yield scrapy.Request(url, meta={
                    'title': Title[i],
                    'pic_url': Pic_url[i],
                    'summary': Summary[i],
                    'home_url': resposne.url
                }, callback=self.parse_one)
            except:
                url = self.base_url + Url[i]
                yield scrapy.Request(url, meta={
                    'title': Title[i],
                    'pic_url': '',
                    'summary': '',
                    'home_url': resposne.url
                }, callback=self.parse_one)

    def parse_one(self, response):
        title = response.meta['title']
        describe = response.meta['summary']
        pic_url = response.meta['pic_url']
        author = ''
        pic_more_url = ''
        home_url = response.meta['home_url']
        app_name = '星岛日报'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content = response.xpath('//div[@class="post-content"]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        pubTime = response.xpath('//div[@class="post-heading supplement-p-h"]/div[@class="date"]/text()').extract()[1].replace(' ','')
        category = response.xpath('//div[@class="post-heading supplement-p-h"]/div[@class="date"]/a/text()').extract()[0]
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
        timeArray = time.strptime(pubTime, "%Y-%m-%d")
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            self.count = self.count + 1
            item['count'] = self.count
            yield item


