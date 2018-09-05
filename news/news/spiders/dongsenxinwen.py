#coding=utf-8
import scrapy
import time
import json
import re
from news.items import NewsItem

class dsxw(scrapy.Spider):
    name = 'dongsenxinwen'
    allowed_domains = ['news.ebc.net.tw']
    start_urls = [
        'https://news.ebc.net.tw/'
    ]
    base_url = 'https://news.ebc.net.tw'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        """
        因为内容为json格式，但json格式不规则，故分三步采集，每次运行一次url
        :param response:
        :return:
        """
        #热门新闻
        # url='https://news.ebc.net.tw/api.js.php?callback=getHottestNews_callback'
        # formdata={
        #     "action": "getAllHottestNews",
        #     "cid": "0",
        #     "hot": "1",
        #     "last_id": "0",
        #     "pages": "0",
        #     "ad_shows": "",
        #     "secret": "5b7dc7d488775ea127836640ac978eca"
        # }
        #心情新闻
        # url='https://news.ebc.net.tw/api.js.php?callback=getMoodNews_callback'
        # formdata={
        #     "action": "getMoodNews",
        #     "heart": "0",
        #     "pages": "0",
        #     "secret": "bd40486ccc43149ac9a6321564430319"
        # }
        # 速报看这里
        # url='https://news.ebc.net.tw/api.js.php?callback=getAllComplainNews_callback'
        # formdata={
        #     "action": "getAllComplainNews",
        #     "cid": "0",
        #     "hot": "1",
        #     "last_id": "0",
        #     "pages": "0",
        #     "ad_shows": "",
        #     "secret": "54da6bf10b3b04fb9c556a484d066c8a"
        # }
        #新闻总览  国际
        listt = ['7', '29', '2', '1']   # 1:政治 7：国际 29：两岸  2：财经
        for i in range(0, len(listt)):
            url = 'https://news.ebc.net.tw/api.js.php?callback=getNews_callback'
            formdata = {
                "action": "getNews",
                "cid": "%s" %listt[i],
                "last_id": "0",
                "ad_shows": "",
                "pages": "0",
                "secret": "215f93cb26bbc4e3d395e9f6df9f105c"
            }
            if listt[i] == '1':
                category = u'财经'.encode('utf-8')
            elif listt[i] == '7':
                category = u'国际'.encode('utf-8')
            elif listt[i] == '29':
                category = u'两岸'.encode('utf-8')
            else:
                category = u'政治'.encode('utf-8')
            yield scrapy.FormRequest(url, meta={
                'category': category
            }, formdata=formdata, callback=self.parse_item)

    def parse_item(self, response):
        data = response.body
        category = response.meta['category']
        data = data.replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '').replace('//NOCachegetNews_callback(', '').replace(')', '')
        data = json.loads(data)
        try:
            for i in data:
                url = self.base_url + i['url']
                try:
                    summary = i['daital']
                except:
                    summary = ''
                yield scrapy.Request(url, meta={
                    'title': i['title'],
                    'pic_url': i['imgpath'],
                    'home_url': response.url,
                    'summary': summary,
                    'category': category
                }, callback=self.parse_one)
        except:
            pass

    def parse_one(self,response):
        title = response.meta['title']
        pic_url = response.meta['pic_url']
        describe = response.meta['summary']
        home_url = response.meta['home_url']
        pubTime = response.xpath('//div[@class="float_left size12 Gray ml15 mt10"]/text()').extract()[0]
        content = response.xpath('//div[@id="contentBody"]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        app_name = '东森新闻'
        pic_more_url = response.xpath('//div[@id="contentBody"]/img/@src').extract()
        more_url = ''
        for i in range(0, len(pic_more_url)):
            more_url += pic_more_url[i]+' ; '
        pic_more_url = more_url
        author = ''
        category = response.meta['category']
        publishedDate = pubTime.replace(u'東森新聞','').replace(' ','')
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
        acceptable_title = []
        try:
            t1 = publishedDate.split(' ')[0]
            t2 = publishedDate.split(' ')[1]
            t = t1 + ' ' + t2
            timeArray = time.strptime(t, "%Y-%m-%d %H:%M")
        except:
            t = publishedDate.split(' ')[0]
            timeArray = time.strptime(t, "%Y-%m-%d")
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            acceptable_title.append(title)
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            self.count += 1
            item['count'] = self.count
            yield item

        if len(acceptable_title) > 0:
            url = 'https://news.ebc.net.tw/api.js.php?callback=getNews_callback'
            formdata = {
                "action": "getNews",
                "cid": "0",
                "last_id": "0",
                "ad_shows": "",
                "pages": "2",
                "secret": "58d37d1d160d0cfb4d345ca42b76ada4"
            }
            yield scrapy.FormRequest(url, formdata=formdata, callback=self.parse_item)
