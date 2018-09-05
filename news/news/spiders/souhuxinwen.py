#-*- coding: utf-8 -*-
from scrapy.spider import Spider
import scrapy
import sys
import json,time
from lxml.etree import HTML
from news.items import NewsItem
reload(sys)
sys.setdefaultencoding('utf8')

class souhu(Spider):
    name = 'souhuxinwen'
    page = 1
    num = 1
    Ttime = int(round(time.time() * 1000))
    start_urls = [
        'https://api.k.sohu.com/api/search/v5/search.go?rt=json&pageNo=' + str(num) +'&words=%E4%B9%A0%E8%BF%91%E5%B9%B3&keyword=%E4%B9%A0%E8%BF%91%E5%B9%B3&p1=NjQwOTIwNDUwMDQxODQ0MTI2MQ%3D%3D&pageSize=20&type=0&pid=&token=&gid=x011060802ff0decee47cd839000939fef9711202659&apiVersion=40&sid=10&u=1&bid=&keyfrom=input&autoCorrection=&refertype=1&versionName=6.0.4&os=android&picScale=16&h=&_=' + str(Ttime)
       ]
    t = '''
            rt	json
        pageNo	2
        words	习近平
        keyword	习近平
        p1	NjQwOTIwNDUwMDQxODQ0MTI2MQ==
        pageSize	20
        type	0
        pid	
        token	
        gid	x011060802ff0decee47cd839000939fef9711202659
        apiVersion	40
        sid	10
        u	1
        bid	
        keyfrom	input
        autoCorrection	
        refertype	1
        versionName	6.0.4
        os	android
        picScale	16
        h	
        _	1528163152979
    '''
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        try:
            data = json.loads(response.body)
            data =data['resultList']
            tt = len(data)
            for i in range(len(data)):
                title = data[i]['title']
                try:
                    desc = data[i]['description']
                except:
                    desc = ''
                publish = data[i]['updateTime']
                id = data[i]['newsId']
                try:
                    pic = data[i]['pics']
                except:
                    pic = ''
                url = 'https://api.k.sohu.com/api/news/v5/article.go?channelId=&apiVersion=40&gid=-1&imgTag=1&newsId=' + str(id) + '&openType=&u=1&p1=NjQwOTIwNDUwMDQxODQ0MTI2MQ%3D%3D&pid=-1&recommendNum=3&refer=130&rt=json&showSdkAd=1&moreCount=8&articleDebug=0&_=' + str(self.Ttime)
                yield scrapy.Request(url,meta={
                    'title':title,
                    'describe':desc,
                    'publish':publish,
                    'pic':pic
                }, callback=self.parse_item)
            if tt > 0:
                self.num += 1
                url = 'https://api.k.sohu.com/api/search/v5/search.go?rt=json&pageNo=' + str(self.num) +'&words=%E4%B9%A0%E8%BF%91%E5%B9%B3&keyword=%E4%B9%A0%E8%BF%91%E5%B9%B3&p1=NjQwOTIwNDUwMDQxODQ0MTI2MQ%3D%3D&pageSize=20&type=0&pid=&token=&gid=x011060802ff0decee47cd839000939fef9711202659&apiVersion=40&sid=10&u=1&bid=&keyfrom=input&autoCorrection=&refertype=1&versionName=6.0.4&os=android&picScale=16&h=&_=' + str(self.Ttime)
                yield scrapy.Request(url, callback=self.parse)
        except:
            pass


    def parse_item(self,response):
        title = response.meta['title']
        describe = response.meta['describe']
        publishedDate = response.meta['publish']
        pic_url = response.meta['pic']
        app_name = '搜狐新闻'
        author = ''
        home_url = 'https://api.k.sohu.com/'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)/1000))
        category = '要闻'
        data = json.loads(response.body)
        content = data['content']
        selector = HTML(content)
        content = selector.xpath('//text()')
        content = ''.join(content)
        content = content.replace('\t','').replace('\n','').replace('\r','')
        pic_more_url = data['photos']
        pic = []
        for i in range(len(pic_more_url)):
            pic.append(str(pic_more_url[i]['pic']))
        pic_more_url = pic
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        if timeStamp >= self.timeStamp:
            numappName = self.readjson()
            if len(numappName) == 0:
                items = {
                    'title':title
                }
                with open('souhuxinwen.json', 'a+') as fp:
                    line = json.dumps(dict(items), ensure_ascii=False) + '\n'
                    fp.write(line)
                yield item
            else:
                for i in range(len(numappName)):
                    if numappName[i]['title'] == item['title']:
                        return
                else:
                    items = {
                        'title': item['title']
                    }
                    with open('souhuxinwen.json', 'a+') as fp:
                        line = json.dumps(dict(items), ensure_ascii=False) + '\n'
                        fp.write(line)
                    yield item

    def readjson(self):
        s = []
        file_object = open('souhuxinwen.json', 'r')
        try:
            while True:
                line = file_object.readline()
                data = json.loads(line)
                s.append(data)
        finally:
            return s

