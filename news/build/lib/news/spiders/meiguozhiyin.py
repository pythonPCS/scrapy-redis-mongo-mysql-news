#coding=utf-8
import scrapy
import json,re,time
from news.items import NewsItem
from lxml.etree import HTML

class meiguozhiyin(scrapy.Spider):
    name = 'meiguozhiyin'
    start_urls = [
        'https://www.voachinese.com/mobapp/zones.xml'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        num = response.xpath('//item/zone/@id').extract()
        cate = response.xpath('//item/zone/name/text()').extract()
        for i in range(len(num)):
            numt = num[i]
            category = cate[i]
            if category == '国际' or category == "亚太" or category == "全球议题" or category == "美国" or category == "中国" or category == "台湾"\
                    or category == "港澳" or category == "美中关系" or category == "美中贸易争端"  or category == "韩朝峰会" \
                    or category == "朝鲜核问题" or category == "台海两岸关系" or category == "南中国海争端" or category == "世界媒体看中国" \
                    or category == "时事看台" or category == "焦点对话":
                url = 'https://www.voachinese.com/mobapp/articles.xml?zoneid=%s&html=2'%numt
                yield scrapy.Request(url, meta={
                    'category': category
                }, callback=self.parse_item)

    def parse_item(self, response):
        category = response.meta['category']
        app_name = '美国之音'
        home_url = 'https://www.voachinese.com/'
        pic_url = ''
        describe = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        author = ''
        tit = response.xpath('//item/article/title/text()').extract()
        pic_more = response.xpath('//item/article/img/@src').extract()
        conten = response.xpath('//item/article/content/text()').extract()
        publishedDat = response.xpath('//item/article/@pubDate').extract()
        pic_more_url = ''
        for i in range(len(tit)):
            title = tit[i]
            content = conten[i].replace('\t', '').replace('\n', '').replace('\r', '')
            publishedDate = publishedDat[i].replace(' GMT','').replace('Tue, ','').replace('Thu, ','')
            publishedDate = publishedDate.replace('Wed, ','').replace('Sat, ','').replace('Mon, ','')
            publishedDate = publishedDate.replace('Sun, ','').replace('Fri, ','')
            t = publishedDate.split(' ')
            t1 = t[0]
            t2 = t[1]
            t3 = t[2]
            t4 = t[3]
            publishedDate = t3 + '-' + t2 + '-' + t1 + ' ' + t4
            if 'Jan' in publishedDate:
                publishedDate = publishedDate.replace('Jan','01')
            elif 'Feb' in publishedDate:
                publishedDate = publishedDate.replace('Feb','02')
            elif 'Mar' in publishedDate:
                publishedDate = publishedDate.replace('Mar','03')
            elif 'Apr' in publishedDate:
                publishedDate = publishedDate.replace('Apr','04')
            elif 'May' in publishedDate:
                publishedDate = publishedDate.replace('May','05')
            elif 'Jun' in publishedDate:
                publishedDate = publishedDate.replace('Jun','06')
            elif 'Jul' in publishedDate:
                publishedDate = publishedDate.replace('Jul','07')
            elif 'Aug' in publishedDate:
                publishedDate = publishedDate.replace('Aug','08')
            elif 'Sept' in publishedDate:
                publishedDate = publishedDate.replace('Sept', '09')
            elif 'Sep' in publishedDate:
                publishedDate = publishedDate.replace('Sep','09')
            elif 'Oct' in publishedDate:
                publishedDate = publishedDate.replace('Oct','10')
            elif 'Nov' in publishedDate:
                publishedDate = publishedDate.replace('Nov','11')
            elif 'Dec' in publishedDate:
                publishedDate = publishedDate.replace('Dec','12')

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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item
