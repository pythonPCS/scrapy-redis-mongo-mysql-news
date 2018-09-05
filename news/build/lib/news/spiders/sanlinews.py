#-*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
import time
import re
from news.items import NewsItem


class qb(Spider):
    name='sanlinews'
    start_urls=[
        'http://www.setn.com/ViewAll.aspx?PageGroupID=1',#即时
        'http://www.setn.com/ViewAll.aspx?PageGroupID=0&p=1',#热门
        'http://www.setn.com/ViewAll.aspx?PageGroupID=0&p=2',#热门
        'http://www.setn.com/ViewAll.aspx?PageGroupID=0&p=3',#热门
        'http://www.setn.com/ViewAll.aspx?PageGroupID=0&p=4',#热门
        'http://www.setn.com/ViewAll.aspx?PageGroupID=0&p=5',#热门
        'http://www.setn.com/ViewAll.aspx?PageGroupID=6&p=1',#政治
        'http://www.setn.com/ViewAll.aspx?PageGroupID=6&p=2',#政治
        'http://www.setn.com/ViewAll.aspx?PageGroupID=6&p=3',#政治
        'http://www.setn.com/ViewAll.aspx?PageGroupID=6&p=4',#政治
        'http://www.setn.com/ViewAll.aspx?PageGroupID=6&p=5',#政治
        'http://www.setn.com/ViewAll.aspx?PageGroupID=41&p=1',#社会
        'http://www.setn.com/ViewAll.aspx?PageGroupID=41&p=2',#社会
        'http://www.setn.com/ViewAll.aspx?PageGroupID=41&p=3',#社会
        'http://www.setn.com/ViewAll.aspx?PageGroupID=41&p=4',#社会
        'http://www.setn.com/ViewAll.aspx?PageGroupID=41&p=5',#社会
        'http://www.setn.com/ViewAll.aspx?PageGroupID=5&p=1',#国际
        'http://www.setn.com/ViewAll.aspx?PageGroupID=5&p=2',#国际
        'http://www.setn.com/ViewAll.aspx?PageGroupID=5&p=3',#国际
        'http://www.setn.com/ViewAll.aspx?PageGroupID=5&p=4',#国际
        'http://www.setn.com/ViewAll.aspx?PageGroupID=5&p=5',#国际
        'http://www.setn.com/ViewAll.aspx?PageGroupID=7&p=1',#科技
        'http://www.setn.com/ViewAll.aspx?PageGroupID=7&p=2',#科技
        'http://www.setn.com/ViewAll.aspx?PageGroupID=7&p=3',#科技
        'http://www.setn.com/ViewAll.aspx?PageGroupID=7&p=4',#科技
        'http://www.setn.com/ViewAll.aspx?PageGroupID=7&p=5',#科技
        'http://www.setn.com/ViewAll.aspx?PageGroupID=2&p=1',#财经
        'http://www.setn.com/ViewAll.aspx?PageGroupID=2&p=2',#财经
        'http://www.setn.com/ViewAll.aspx?PageGroupID=2&p=3',#财经
        'http://www.setn.com/ViewAll.aspx?PageGroupID=2&p=4',#财经
        'http://www.setn.com/ViewAll.aspx?PageGroupID=2&p=5',#财经
        'http://www.setn.com/ViewAll.aspx?PageGroupID=31&p=1',#HOT焦点
        'http://www.setn.com/ViewAll.aspx?PageGroupID=31&p=2',#HOT焦点
        'http://www.setn.com/ViewAll.aspx?PageGroupID=31&p=3',#HOT焦点
        'http://www.setn.com/ViewAll.aspx?PageGroupID=31&p=4',#HOT焦点
        'http://www.setn.com/ViewAll.aspx?PageGroupID=31&p=5',#HOT焦点
        ]
    base_url='http://www.setn.com/'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//div[@class="row NewsList"]/div/div/div/div/div[1]/h4/a/@href').extract()
        title = response.xpath('//div[@class="row NewsList"]/div/div/div/div/div[1]/h4/a/text()').extract()
        categ = response.xpath('//div[@class="row NewsList"]/div/div/div/div/div[2]/a/text()').extract()
        for i in range(len(links)):
            if 'http' not in links[i]:
                url = 'http://www.setn.com' + links[i]
            else:
                url = links[i]
            tit = title[i]
            yield Request(url, meta={
                'title':tit,
                'home_url':response.url,
                'category':categ[i],
            }, callback=self.parse_item)

    def parse_item(self, response):
        title = response.meta['title']
        category = response.meta['category']
        home_url = response.meta['home_url']
        app_name = '三立新闻'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_url = ''
        describe = ''
        pubTime = response.xpath('//time[@class="page-date"]/text()').extract()[0]
        pubTime = pubTime.replace('/', '-')
        try:
            try:
                content = response.xpath('//div[@id="Content1"]').extract()
                contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                content = re.findall('>(.*?)<', contentt)
                contentdata = ''
                for i in range(0, len(content)):
                    contentdata += content[i]
                content = contentdata
            except:
                content = response.xpath('//div[@id="Content2"]').extract()
                contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                content = re.findall('>(.*?)<', contentt)
                contentdata = ''
                for i in range(0, len(content)):
                    contentdata += content[i]
                content = contentdata
        except:
            content = response.xpath('//p/text()').extract()
            contentt = ''
            for i in range(len(content)):
                contentt += content[i]
            content = contentt
        pic_more_url = re.findall('src="(.*?)"', contentt)
        pic_more_url1 = []
        if len(pic_more_url) > 0:
            for i in range(0, len(pic_more_url)):
                pic_more_url1.append(pic_more_url[i])
            pic_more_url = str(set(pic_more_url1))
        else:
            pic_more_url = ''
        author = ''
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
        print "发布时间", pubTime
        print "爬取时间", crawlTime
        timeArray = time.strptime(pubTime, "%Y-%m-%d %H:%M:%S")
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
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
            print "okokokokokokokokokok"
            if item['publishedDate'] != '':
                yield item
