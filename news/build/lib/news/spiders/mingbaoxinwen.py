#-*- coding: utf-8 -*-
from scrapy.spiders import Spider
import json
import time
import re
from news.items import NewsItem
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class mingbao(Spider):
    name = 'mingbaoxinwen'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    tdata = time_str.replace('-','')
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    start_urls = [
        'https://newsapp.mingpao.com/php/api/app_articlesearch.php?p=pns&date=%s&section=S00001&size=20&page=1'%tdata,#要闻
        'https://newsapp.mingpao.com/php/api/app_articlesearch.php?p=pns&date=%s&section=S00002&size=20&page=1'%tdata,#港闻
        'https://newsapp.mingpao.com/php/api/app_articlesearch.php?p=pns&date=%s&section=S00004&size=20&page=1'%tdata,#经济
        'https://newsapp.mingpao.com/php/api/app_articlesearch.php?p=pns&date=%s&section=S00012&size=20&page=1'%tdata,#观点
        'https://newsapp.mingpao.com/php/api/app_articlesearch.php?p=pns&date=%s&section=S00013&size=20&page=1'%tdata,#中国
        'https://newsapp.mingpao.com/php/api/app_articlesearch.php?p=pns&date=%s&section=S00014&size=20&page=1'%tdata,#国际
        'https://newsapp.mingpao.com/php/api/app_articlesearch.php?p=ins&date=%s&section=S00001&size=20&page=1'%tdata,
        'https://newsapp.mingpao.com/php/api/app_articlesearch.php?p=ins&date=%s&section=S00004&size=20&page=1'%tdata,
        'https://newsapp.mingpao.com/php/api/app_articlesearch.php?p=ins&date=%s&section=S00005&size=20&page=1'%tdata
    ]

    def parse(self, response):
        print response.body
        # data = json.loads(response.body.replace('\t','').replace('\n','').replace('\r',''))
        # data = data['data_Result']
        # data = response.body['data_Result']
        title = re.findall('"TITLE":"(.*?)",',response.body)
        url = re.findall('"LINK":"(.*?)",',response.body)
        cate = re.findall('"CATEGORY":"(.*?)",',response.body)
        pubt = re.findall('"PUBDATE":"(.*?)",',response.body)
        desc = re.findall('"DESCRIPTION":"(.*?)",',response.body)
        # author = re.findall('"AUTHOR":"(.*?)",',response.body)
        for i in range(len(url)):
            yield scrapy.Request(url[i].replace('\/','/'), meta={
                'title': title[i],
                'describe': desc[i],
                'pubt': pubt[i],
                'category': cate[i],
                'home_url': url[i].replace('\/','/')
            }, callback=self.parse_item, dont_filter=True)

    def parse_item(self,response):
        title = response.meta['title']
        category = response.meta['category']
        home_url = response.meta['home_url']
        describe = response.meta['describe']
        publishedDate = response.meta['pubt']
        author = ''
        app_name = '明报新闻'
        pic_url = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        try:
            content = response.xpath('//article').extract()
            content = content[0].replace('\t','').replace('\n','').replace('\r','')
            content = re.findall('>(.*?)<', content)
            contentt = ''
            for i in range(len(content)):
                contentt += content[i]
            content = contentt
        except:
            content = response.xpath('//p/text()').extract()
            contentt = ''
            for i in range(len(content)):
                contentt += content[i]
            content = contentt
        pic_more_url = ''
        if category == '':
            category = '要闻'
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
        self.count += 1
        item['count'] = self.count
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item





