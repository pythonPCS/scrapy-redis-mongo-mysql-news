#coding=utf-8
import re
import json
import scrapy,time
from news.items import NewsItem
class lcnews(scrapy.Spider):
    name = 'lichangxinwen'
    start_urls = [
        'http://www.thestand.news/politics/?page=1',#政治
        'http://www.thestand.news/international/?page=1',#国际
        'http://www.thestand.news/finance/?page=1',#财经
        'http://www.thestand.news/%E5%8F%B0%E7%81%A3/?page=1',#台湾
        'http://www.thestand.news/china/?page=1',#中国
        'http://www.thestand.news/%E6%BE%B3%E9%96%80/?page=1',#澳门
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    base_url = 'http://www.thestand.news'

    def parse(self, response):
        try:
            title = response.xpath('//div[@clas="news-articles"]/div[1]/div/h3/a/text()').extract()
            links = response.xpath('//div[@clas="news-articles"]/div[1]/div/h3/a/@href').extract()
            pubti = response.xpath('//div[@clas="news-articles"]/div[1]/div/p[1]/span[2]/text()').extract()
            pic_u = response.xpath('//div[@clas="news-articles"]/div[1]/div/div/a/img/@src').extract()
            desc  = response.xpath('//div[@clas="news-articles"]/div[1]/div/p[2]/text()').extract()
            accept_title = []
            for i in range(0,len(title)):
                titl = title[i].replace('\t','').replace('\n','').replace('\r','').replace(' ','')
                url  = self.base_url + links[i]
                if 'http' not in pic_u[i]:
                    pic_url = 'http:' + pic_u[i]
                else:
                    pic_url = pic_u[i]
                describe = desc[i].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                publishedDate = pubti[i].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '').replace(
                    ' — ', ' ').replace('/', '-').replace('—',' ')
                print publishedDate
                timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M")
                publishedDa = int(time.mktime(timeArray))
                if publishedDa >= self.timeStamp:
                    accept_title.append(titl)
                    publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDa)))
                    yield scrapy.Request(url,meta={
                        'title':titl,
                        'pic_url':pic_url,
                        'publishedDate':publishedDate,
                        'describe':describe,
                        'home_url':response.url
                    },callback=self.parse_item,dont_filter=True)
        except:
            title = response.xpath('//div[@class="articles-wrap"]/div/div[2]/h3/a/text()').extract()
            links = response.xpath('//div[@class="articles-wrap"]/div/div[2]/h3/a/@href').extract()
            pic_u = response.xpath('//div[@class="articles-wrap"]/div/div[1]/a/img/@src').extract()
            pubti = response.xpath('//div[@class="articles-wrap"]/div/div[2]/p[1]/span[2]/text()').extract()
            desc = response.xpath('//div[@class="articles-wrap"]/div/div[2]/p[2]/text()').extract()
            accept_title = []
            for i in range(0, len(title)):
                titl = title[i].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                url = self.base_url + links[i]
                if 'http' not in pic_u[i]:
                    pic_url = 'http:' + pic_u[i]
                else:
                    pic_url = pic_u[i]
                describe = desc[i].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                publishedDate = pubti[i].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '').replace(
                    ' — ', ' ').replace('/', '-').replace('—',' ')
                print publishedDate
                timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M")
                publishedDa = int(time.mktime(timeArray))
                if publishedDa >= self.timeStamp:
                    accept_title.append(titl)
                    publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDa)))
                    yield scrapy.Request(url, meta={
                        'title': titl,
                        'pic_url': pic_url,
                        'publishedDate': publishedDate,
                        'describe': describe,
                        'home_url': response.url
                    }, callback=self.parse_item)
        if len(accept_title) == 20:
            num = str(response.url).split('page=')[1]
            num1 = int(num) + 1
            url =str(response.url).replace( 'page='+ num , 'page=' + str(num1))
            yield scrapy.Request(url,callback=self.parse)

    def parse_item(self,response):
        title = response.meta['title']
        pic_url = response.meta['pic_url']
        publishedDate =response.meta['publishedDate']
        describe = response.meta['describe']
        home_url = response.meta['home_url']
        app_name = '立场新闻'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content = response.xpath('//div[@class="article-content"]').extract()
        contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '').replace('　　', '')
        content = re.findall('>(.*?)<', contentt)
        contentdata = ''
        for i in range(0, len(content)):
            contentdata += content[i]
        content = contentdata
        try:
            pic_more_url = response.xpath('//div[@class="article-photo article-media"]/a/img/@src').extract()[0]
        except:
            pic_more_url = ''
        author = ''
        if '%E6%BE%B3%E9%96%80' in home_url:
            category = u'澳门'.encode('utf-8')
        elif 'china' in home_url:
            category = u'中国'.encode('utf-8')
        elif 'politics' in home_url:
            category = u'政治'.encode('utf-8')
        elif 'international' in home_url:
            category = u'国际'.encode('utf-8')
        elif 'finance' in home_url:
            category = u'财经'.encode('utf-8')
        elif '%E5%8F%B0%E7%81%A3' in home_url:
            category = u'台湾'.encode('utf-8')
        else:
            category = u'首页'.encode('utf-8')
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
