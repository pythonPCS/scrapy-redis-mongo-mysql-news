#coding=utf-8
import scrapy
import time
import re
from news.items import NewsItem

class dtw(scrapy.Spider):
    name='dongtaiwang'
    start_urls=[
        'http://dongtaiwang.com/loc/phome.php?v=0'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links_url=response.xpath('//div[@class="content_list"]/li/a/@href').extract()
        title = response.xpath('//div[@class="content_list"]/li/a/text()').extract()
        for i in range(0,len(links_url)):
            url = links_url[i]
            yield scrapy.Request(url,meta={
                'title':title[i],
                'home_url':response.url
            },callback=self.parse_item,dont_filter=True)

    def parse_item(self,response):
        title=response.meta['title']
        home_url=response.meta['home_url']
        app_name='动态网'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_url=''
        describe = ''
        author = ''
        try:
            content=response.xpath('//div[@id="ar_bArticleContent"]').extract()
            contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('>(.*?)<', contentt)
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
        except:
            content=response.xpath('//p').extract()
            contentdata=''
            for i in  range(0,len(content)):
                    contentdata+=content[i]
            content=contentdata
            content = content.replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('>(.*?)<', content)
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
        pic_more_url=''
        if 'nsc' in response.url:
            category = u'中国要闻'.encode('utf-8')
        elif 'prog' in response.url:
            category = u'明慧要闻'.encode('utf-8')
        elif 'dweb' in response.url:
            category = u'明慧新闻'.encode('utf-8')
        elif 'gb' in response.url:
            category = u'明慧新闻'.encode('utf-8')
        elif 'mh' in response.url:
            category = u'明慧要闻'.encode('utf-8')
        else:
            category = u'中国要闻'.encode('utf-8')
        try:
            try:
                pubTime=response.xpath('//div[@class="mbottom10 large-12 medium-12 small-12 columns"]/time/text()').extract()[0]
                pubTime=pubTime.replace(u'更新: ','').replace('PM','').replace('AM','').replace('\t','').replace('\n','').replace('\r','')
            except:
                pubTime=response.xpath('//div[@class="art-head"]/span/text()').extract()
                pubTime=pubTime[0].split(' ')[0].replace(u'年','-').replace(u'月','-').replace(u'日','')
        except:
            pubTime = str(time.strftime("%Y-%m-%d"))
        if category=='更多新闻':
            publishedDate = pubTime
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
            print pubTime
            t = pubTime.split(' ')[0]
            timeArray = time.strptime(t, "%Y-%m-%d")
            publishedDate = time.mktime(timeArray)
            if publishedDate >= self.timeStamp:
                self.count += 1
                item['count'] = self.count
                publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
                item['publishedDate'] = publishedDate
                yield item
