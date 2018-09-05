#coding=utf-8
import scrapy
import json,re
import time
from news.items import NewsItem

class xianggang(scrapy.Spider):
    name = 'xianggang02'
    start_urls = [
        'https://web-data.api.hk01.com/v2/feed/category/364?offset=99999999987&bucketId=00000',#中国
        'https://web-data.api.hk01.com/v2/feed/category/365?offset=99999999988&bucketId=00000',#中国
        'https://web-data.api.hk01.com/v2/feed/category/366?offset=99999999987&bucketId=00000',#中国
        'https://web-data.api.hk01.com/v2/feed/category/367?offset=99999999987&bucketId=00000',#中国
        'https://web-data.api.hk01.com/v2/feed/category/2?offset=99999999993&bucketId=00000',#港闻
        'https://web-data.api.hk01.com/v2/feed/category/6?offset=99999999990&bucketId=00000',#港闻
        'https://web-data.api.hk01.com/v2/feed/category/310?offset=99999999991&bucketId=00000',#港闻
        'https://web-data.api.hk01.com/v2/feed/category/143?offset=99999999993&bucketId=00000',#港闻
        'https://web-data.api.hk01.com/v2/feed/category/403?offset=99999999993&bucketId=00000',#港闻
        'https://web-data.api.hk01.com/v2/feed/category/19?offset=99999999990&bucketId=00000',#国际
        'https://web-data.api.hk01.com/v2/feed/category/405?offset=99999999990&bucketId=00000',#国际
        'https://web-data.api.hk01.com/v2/feed/category/406?offset=99999999987&bucketId=00000',#国际
        'https://web-data.api.hk01.com/v2/feed/category/407?offset=99999999988&bucketId=00000',#国际
        'https://web-data.api.hk01.com/v2/feed/category/408?offset=99999999991&bucketId=00000',#国际
        'https://web-data.api.hk01.com/v2/feed/category/409?offset=99999999991&bucketId=00000',#国际
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        data = json.loads(response.body)
        number = data['nextOffset']
        data = data['items']
        num = 0
        for i in range(len(data)):
            title = data[i]['data']['title']
            url = data[i]['data']['publishUrl']
            category = data[i]['data']['mainCategory']
            pubt = data[i]['data']['publishTime']
            try:
                pic = data[i]['data']['mainImage']['cdnUrl']
            except:
                pic = ''
            try:
                desc = data[i]['data']['description']
            except:
                desc = ''
            try:
                author = data[i]['data']['authors'][0]['publishName']
            except:
                author = ''
            rrr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(pubt)))
            print rrr
            if float(pubt) >= self.timeStamp:
                num += 1
                pubt = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(pubt)))
                yield scrapy.Request(url,meta={
                    'title':title,
                    'category':category,
                    'pubt':pubt,
                    'desc':desc,
                    'author':author,
                    'pic':pic
                }, callback=self.parse_item, dont_filter=True)
        if num > 0 :
            nu = str(response.url).split('offset=')[0]
            url = nu + 'offset=' + str(number) + '&bucketId=00000'
            yield scrapy.Request(url,callback=self.parse)


    def parse_item(self,response):
        title = response.meta['title']
        category = response.meta['category']
        publishedDate = response.meta['pubt']
        describe = response.meta['desc']
        author = response.meta['author']
        app_name=  '香港01'
        pic_url = response.meta['pic']
        home_url = 'https://www.hk01.com/'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content = response.xpath('//p/text()').extract()
        contentt = ''
        for i in range(len(content)):
            contentt += content[i]
        content = contentt
        pic_more_url = pic_url
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