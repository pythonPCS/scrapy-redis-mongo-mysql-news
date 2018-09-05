#-*- coding: utf-8 -*-
from scrapy.spider import Spider
import scrapy
import sys
import json,time,re
from news.items import NewsItem
reload(sys)
sys.setdefaultencoding('utf8')

class xinwenwang(scrapy.Spider):
    name = 'zhongguoxinwen'
    page = 1
    start_urls = [
        'http://dw.chinanews.com/chinanews/getNewsList.json?version_chinanews=6.3.13&deviceId_chinanews=864454030661742&platform_chinanews=android&source=chinanews&area=%E5%8C%97%E4%BA%AC%E5%B8%82&language=chs&pageSize=10&searchType=9&searchWord=%E4%B9%A0%E8%BF%91%E5%B9%B3&pageIndex=' + str(page)  + '&dtp=1'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        data = json.loads(response.body)
        data = data['data']
        num = 0
        for i in range(len(data)):
            title = data[i]['title']
            pic = data[i]['picture']
            id = data[i]['id']
            try:
                pubt = data[i]['freshTime']
            except:
                pubt = data[i]['pubtime']
            timeArray = time.strptime(pubt, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            if timeStamp >= self.timeStamp:
                num += 1
                url = 'http://dw.chinanews.com/chinanews/newsContent.json?version_chinanews=6.3.13&deviceId_chinanews=864454030661742&platform_chinanews=android&source=chinanews&language=chs&user=&id=%s&pageSize=3&dtp=1'%id
                yield scrapy.Request(url,meta={
                    'title':title,
                    'pic':pic,
                    'pubt':pubt
                },callback=self.parse_item)
            # if len(data) > 0 :
            if num >= 0:
                self.page += 1
                url = 'http://dw.chinanews.com/chinanews/getNewsList.json?version_chinanews=6.3.13&deviceId_chinanews=864454030661742&platform_chinanews=android&source=chinanews&area=%E5%8C%97%E4%BA%AC%E5%B8%82&language=chs&pageSize=10&searchType=9&searchWord=%E4%B9%A0%E8%BF%91%E5%B9%B3&pageIndex=' + str(self.page)  + '&dtp=1'
                yield scrapy.Request(url, callback=self.parse)


    def parse_item(self,response):
        title = response.meta['title']
        pic_url = response.meta['pic']
        publishedDate = response.meta['pubt']
        app_name = '中国新闻网'
        category = '要闻'
        describe = ''
        author = ''
        home_url = 'http://dw.chinanews.com'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        data = json.loads(response.body)
        content = data['data']['content']
        contentt = content.replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', contentt)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        pic_more_url = data['data']['picture']
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
        yield item



