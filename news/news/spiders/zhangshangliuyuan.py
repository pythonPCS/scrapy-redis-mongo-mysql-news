#-*- coding: utf-8 -*-
import time
import re
import sys
import scrapy
from news.items import NewsItem
reload(sys)
sys.setdefaultencoding('utf8')

class zhangshangliuyuan(scrapy.Spider):
    name = 'zhangshangliuyuan'
    start_urls = [
        'http://site.6parker.com/finance/index.php?app=forum&act=cachepage&cp=tree1',#经济观察
        'http://news.6parker.com/newspark/index.php?p=1',#实时新闻
        'http://news.6parker.com/newspark/index.php?type=8',#历史
        'http://news.6parker.com/newspark/index.php?type=2',
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-10', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//div[@id="d_list"]/ul/li/a[1]/@href').extract()
        title = response.xpath('//div[@id="d_list"]/ul/li/a[1]/text()').extract()
        pubTime = response.xpath('//div[@id="d_list"]/ul/li/i/text()').extract()
        for i in range(0,len(links)):
            url = links[i]
            if 'http' not in url:
                url = 'http://site.6parker.com/finance/' + url
            tit = title[i]
            pub = pubTime[i].split('/')
            t1 = pub[0]
            t2 = pub[1]
            t3 = pub[2]
            publishedDate = '20'+t3 + '-' + t1 + '-' + t2
            timeArray = time.strptime(publishedDate, "%Y-%m-%d")
            publishedDa = time.mktime(timeArray)
            if publishedDa >= self.timeStamp:
                publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDa)))
                yield scrapy.Request(url,meta={
                    'title':tit,
                    'home_url':response.url,
                    'publishedDate':publishedDate
                },callback=self.parse_item,dont_filter=True)

    def parse_item(self,response):
        title = response.meta['title']
        home_url = response.meta['home_url']
        publishedDate = response.meta['publishedDate']
        app_name = u'掌上留园'.encode('utf-8')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        describe = ''
        author =''
        pic_url = ''
        if 'tree1' in home_url:
            category = u'经济观察'.encode('utf-8')
        elif 'type=2' in home_url:
            category = u'财经'.encode('utf-8')
        elif 'type=8' in home_url:
            category = u'历史'.encode('utf-8')
        else:
            category = u'实时新闻'.encode('utf-8')
        try:
            content = response.xpath('//div[@id="mainContent"]').extract()
            contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace('　　', '').replace(' ', '')
            content = re.findall('>(.*?)<', contentt)
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
            pic_more_url = re.findall('<img(.*?)src="(.*?)"', contentt)
            pic_more_url1 = []
            if len(pic_more_url) > 0:
                for i in range(0, len(pic_more_url)):
                    if '.js' not in pic_more_url[i][1]:
                        pic_more_url1.append(pic_more_url[i][1])
                pic_more_url = str(set(pic_more_url1))
            else:
                pic_more_url = ''
        except:
            content = response.xpath('//p/text()').extract()
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
            pic_more_url = ''
        self.count = self.count + 1
        url = response.url
        item = NewsItem()
        item['app_name'] = app_name
        item['count'] = self.count
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
        yield item

