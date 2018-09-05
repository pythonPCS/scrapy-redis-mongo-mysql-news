#-*- coding: utf-8 -*-
import time
import re
from news.items import NewsItem
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
import scrapy

class Lianhezaob(scrapy.Spider):
    name = "lianhezaobao"
    start_urls = [
        'http://www.zaobao.com/realtime/china',#中国
        'http://www.zaobao.com/news/china',
        'http://www.zaobao.com/realtime/world',#国际
        'http://www.zaobao.com.sg/znews/greater-china',
        'http://www.zaobao.com.sg/znews/international',
        'http://www.zaobao.com.sg/realtime/china',
        'http://www.zaobao.com.sg/realtime/world',
        'http://www.zaobao.com.sg/zfinance/realtime',
        'http://www.zaobao.com/znews/international',
        'http://www.zaobao.com/finance/realtime',#财经
        'http://www.zaobao.com/news/greater-china',#中港台
        'http://www.zaobao.com/opinions/editorial',#言论
        'http://www.zaobao.com.sg/zfinance/realtime',#财经
        'http://www.zaobao.com/realtime/singapore',
        'http://www.zaobao.com/finance/china',
        'http://www.zaobao.com/special/report/politic/cnpol',
        'http://www.zaobao.com/forum/views',
    ]
    base_url = "http://www.zaobao.com"
    count = 0
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links_url = response.xpath('//div[@class=" row list"]/div[1]/a/@href').extract()
        for i in range(0,len(links_url)):
            if 'http' not in links_url[i]:
                url = 'http://www.zaobao.com/' + links_url[i]
                yield scrapy.Request(url,meta={
                    'home_url':response.url
                }, callback=self.parse_news,dont_filter=True)
            else:
                url = links_url[i]
                yield scrapy.Request(url,meta={
                    'home_url':response.url
                },callback=self.parse_news,dont_filter=True)


    def parse_news(self,response):
        title = response.xpath('//h1/text()').extract()
        if title:
            title = title[0].encode('utf-8')
        else:
            return
        publishedDate = response.xpath('//span[@class="datestamp date-published meta-date-published"]').extract()
        p = publishedDate[0].replace('\t','').replace('\n','').replace('\r','')
        p = re.findall('>(.*?)<', p)
        pp = ''
        for i in range(len(p)):
            pp += p[i]
        publishedDate = pp.replace('发布', '').replace(' ', '').replace('AM', '').replace('PM', '')
        publishedDate = publishedDate.replace('年', '-').replace('月', '-').replace('日', ' ').replace('/','')
        print publishedDate
        # if publishedDate:
        #     publishedDate = publishedDate[0].encode('utf-8')
        #     publishedDate = re.findall('\d+',publishedDate)
        #     year = publishedDate[0]
        #     month = publishedDate[1]
        #     day = publishedDate[2]
        #     publishedDate = year+'-'+month+'-'+day
        # else:
        #     publishedDate = self.time_str
        content = response.xpath('//div[@id="FineDining"]/p//text()').extract()
        if content:
            content = ''.join(content).encode('utf-8').strip()
        else:
            content = ''
        pic_url = ''
        author = ""
        pic_more_url = set()
        category = response.xpath('//section[@id="breadcrumbs"]/a[3]/text()').extract()
        if category:
            category = category[0].encode('utf-8')
            if category == u'社论':
                category = u'观点'.encode('utf-8')
            if category == u'中港台即时':
                category = u'中港台'.encode('utf-8')
            if category == u'国际即时':
                category = u'国际'.encode('utf-8')
            if category == u'中国即时':
                category = u'中国'.encode('utf-8')
        else:
            category = u'首页'.encode('utf-8')
        home_url = response.meta['home_url']
        if u'/china' in home_url:
            category = u'中国'.encode('utf-8')
        elif u'-china' in home_url:
            category = u'中港台'.encode('utf-8')
        elif u'finance' in home_url:
            category = u'中国财经'.encode('utf-8')
        elif u'world' in home_url:
            category = u'国际'.encode('utf-8')
        elif u'international' in home_url:
            category = u'国际'.encode('utf-8')
        elif u'opinions' in home_url:
            category = u'观点'.encode('utf-8')
        elif 'view' in home_url:
            category = u'观点'.encode('utf-8')
        else:
            category = u'首页'.encode('utf-8')
        describe = response.xpath('//div[@id="FineDining"]/p[1]//text()').extract()
        if describe:
            describe = describe[0].encode('utf-8')
        else:
            describe = ''
        home_url = "http://www.zaobao.com/"
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        app_name = '联合早报'
        self.count = self.count + 1
        item = NewsItem()
        item['app_name'] = app_name
        item['count'] = self.count
        item['pic_url'] = pic_url
        item['pic_more_url'] = pic_more_url
        item['author'] = author
        item['url'] = response.url
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