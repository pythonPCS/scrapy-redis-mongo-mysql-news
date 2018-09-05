#-*- coding: utf-8 -*-
from scrapy.spider import Spider
import scrapy
import sys
import json,time
from news.items import NewsItem
reload(sys)
sys.setdefaultencoding('utf8')

class guangming(scrapy.Spider):
    name = 'guangmingribao'
    page = 0
    start_urls = [
        'http://s.cloud.gmw.cn/zcms/searchContent?SiteID=126&CatalogID=15277,15285&Query=%E4%B9%A0%E8%BF%91%E5%B9%B3&PageSize=10&PageIndex=' + str(page)#query = 后为习近平
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-01', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        data = json.loads(response.body)
        data = data['data']
        num = 0
        for i in range(len(data)):
            title = data[i]['title']
            category = data[i]['catalogName']
            publishe = data[i]['publishDate']
            pic_url = 'http://s.cloud.gmw.cn/2016' + data[i]['logoFile']
            id = data[i]['articleId']
            url = 'http://s.cloud.gmw.cn/zcms/getArticleInfo?articleId=%s'%id
            if float(publishe)/1000 >= self.timeStamp:
                num += 1
                yield scrapy.Request(url,meta={
                    'title':title,
                    'category':category,
                    'published':publishe,
                    'pic_url':pic_url
                },callback=self.parse_item)
        if num > 0:
            self.page += 1
            url = 'http://s.cloud.gmw.cn/zcms/searchContent?SiteID=126&CatalogID=15277,15285&Query=%E4%B9%A0%E8%BF%91%E5%B9%B3&PageSize=10&PageIndex=' + str(self.page)#query = 后为习近平
            yield scrapy.Request(url, callback=self.parse)


    def parse_item(self,response):
        title = response.meta['title']
        category = response.meta['category']
        published = response.meta['published']
        app_name = '光明日报'
        pic_url = response.meta['pic_url']
        describe = ''
        home_url = 'http://s.cloud.gmw.cn/'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(published)/1000))
        data = json.loads(response.body)
        data = data['data']
        content = data['artContent']
        author = data['artAuthor']
        pic_more_url = str(data['images'])
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
        self.count += 1
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
        item['count'] = self.count
        yield item
