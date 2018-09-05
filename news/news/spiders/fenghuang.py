#coding=utf-8
import json
import scrapy
import time,re,time
from news.items import NewsItem
from news.DataResource import TransportData
from lxml.etree import HTML

class fenghuang(scrapy.Spider):
    name = 'fenghuang'
    Ttime = int(round(time.time() * 1000))
    count = 0
    page = 1
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-01', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def start_requests(self):
        t = self.Ttime
        token = self.md5(t)
        url ='https://api.3g.ifeng.com/client_search_list?k=习近平&page=%s&gv=5.6.9&av=5.6.8&uid=123&deviceid=123&proid=ifengnewsdiscovery&os=ios_19&df=androidphone&vt=5&screen=720x1280&nw=wifi&token=%s&date=%s&callback=1&callback=window.jsonp.cb1'%(self.page,token,t)
        yield scrapy.Request(url,callback=self.parse)


    def parse(self, response):
        data = response.body.replace('window.jsonp.cb1(','').replace(')','')
        data = json.loads(data)
        data = data['data']
        num = 0
        for i in range(len(data)):
            title = data[i]['title'].replace('<em>','').replace('</em>','')
            pubt = data[i]['createTime'].replace('/','-')
            url = data[i]['link']['url']
            try:
                pic_url = data[i]['thumbnail']
            except:
                pic_url = ''
            timeArray = time.strptime(pubt, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            if timeStamp >= self.timeStamp:
                num += 1
                yield scrapy.Request(url,meta={
                    'pic_url':pic_url,
                    'title':title,
                    'pubt':pubt
                },callback=self.parse_item)
        if num > 0:
            self.page += 1
            t = self.Ttime
            token = self.md5(t)
            url = 'https://api.3g.ifeng.com/client_search_list?k=习近平&page=%s&gv=5.6.9&av=5.6.8&uid=123&deviceid=123&proid=ifengnewsdiscovery&os=ios_19&df=androidphone&vt=5&screen=720x1280&nw=wifi&token=%s&date=%s&callback=1&callback=window.jsonp.cb1' % (
            self.page, token, t)
            yield scrapy.Request(url, callback=self.parse)


    def parse_item(self,response):
        title = response.meta['title']
        pic_url = response.meta['pic_url']
        publishedDate = response.meta['pubt']
        app_name = '凤凰新闻'
        describe =  ''
        home_url = 'https://api.3g.ifeng.com/'
        category = '头条'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        data = json.loads(response.body)
        content =data['body']['text']
        contentt = content.replace('\t', '').replace('\n', '').replace('\r', '')
        text = HTML(content)
        try:
            pic_more_url = text.xpath('//p/img/@src')
        except:
            pic_more_url = ''
        content = re.findall('>(.*?)<', contentt)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        try:
            author = data['body']['source']
        except:
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
        yield item

    def md5(self,page):
        import hashlib
        t = 'IFENG' + str(page)
        m = hashlib.md5()
        m.update(t)
        return m.hexdigest()