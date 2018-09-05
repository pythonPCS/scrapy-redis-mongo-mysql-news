#coding=utf-8
import scrapy
import time,re
from news.items import NewsItem
import json
from Cryptodome.Cipher import AES
from binascii import b2a_hex, a2b_hex
from binascii import b2a_hex, a2b_hex


class wangyi(scrapy.Spider):
    name = 'wyxinwen'
    # start_urls = [
    #     'http://c.m.163.com/nc/article/list/T1414142214384/0-20.html',
    #     'http://c.m.163.com/nc/article/list/T1414142214384/20-20.html',
    #     'http://c.m.163.com/nc/article/list/T1414142214384/40-20.html'
    # ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    time_str1 = time.strftime("%Y-%m-%d %H:%M:%S")
    timeArray1 = time.strptime(time_str1, "%Y-%m-%d %H:%M:%S")
    timeStamp1 = int(time.mktime(timeArray1))

    def start_requests(self):
        t = str(self.timeStamp1)
        key = self.aes(t)
        url = 'http://c.m.163.com/recommend/getSubDocPic?tid=T1348647909107&from=toutiao&offset=1&size=10&fn=1&LastStdTime=0&spestr=shortnews&prog=bjrec_toutiao_v0e&passport=&devId=w5IMJr/VJZP4nluUZXnpaw==&lat=&lon=&version=36.0&net=wifi&ts=' + str(t) + '&sign=' + key + '&encryption=1&canal=baidu_cpd1_news&mac=Ft/gmnuXr4kqb/B9ZJB26CKCZ0vHdesSTBiDEVNplbY=&open=&openpath='
        url = [
            'http://c.m.163.com/dlist/article/dynamic?from=T1467284926140&offset=0&size=20&fn=1&LastStdTime=0&passport=&devId=w5IMJr/VJZP4nluUZXnpaw==&lat=v7YkY/cxMW8TiRWiqv8p5A==&lon=cu7pkk2XGKh9YksCMSg2BQ==&version=36.0&net=wifi&ts= '+ str(t) + '&sign=' + key + '&encryption=1&canal=baidu_cpd1_news&mac=Ft/gmnuXr4kqb/B9ZJB26CKCZ0vHdesSTBiDEVNplbY=&open=&openpath=',
            'http://c.m.163.com/dlist/article/dynamic?from=T1467284926140&offset=20&size=20&fn=1&LastStdTime=0&passport=&devId=w5IMJr/VJZP4nluUZXnpaw==&lat=v7YkY/cxMW8TiRWiqv8p5A==&lon=cu7pkk2XGKh9YksCMSg2BQ==&version=36.0&net=wifi&ts= '+ str(t) + '&sign=' + key + '&encryption=1&canal=baidu_cpd1_news&mac=Ft/gmnuXr4kqb/B9ZJB26CKCZ0vHdesSTBiDEVNplbY=&open=&openpath=',
            'http://c.m.163.com/dlist/article/dynamic?from=T1467284926140&offset=40&size=20&fn=1&LastStdTime=0&passport=&devId=w5IMJr/VJZP4nluUZXnpaw==&lat=v7YkY/cxMW8TiRWiqv8p5A==&lon=cu7pkk2XGKh9YksCMSg2BQ==&version=36.0&net=wifi&ts= '+ str(t) + '&sign=' + key + '&encryption=1&canal=baidu_cpd1_news&mac=Ft/gmnuXr4kqb/B9ZJB26CKCZ0vHdesSTBiDEVNplbY=&open=&openpath=',
            'http://c.m.163.com/dlist/article/dynamic?from=T1348648756099&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=w5IMJr/VJZP4nluUZXnpaw==&lat=v7YkY/cxMW8TiRWiqv8p5A==&lon=cu7pkk2XGKh9YksCMSg2BQ==&version=36.0&net=wifi&ts= '+ str(t) + '&sign=' + key + '&encryption=1&canal=baidu_cpd1_news&mac=Ft/gmnuXr4kqb/B9ZJB26CKCZ0vHdesSTBiDEVNplbY=&open=&openpath=',
            'http://c.m.163.com/dlist/article/dynamic?from=T1348648756099&offset=20&size=10&fn=1&LastStdTime=0&passport=&devId=w5IMJr/VJZP4nluUZXnpaw==&lat=v7YkY/cxMW8TiRWiqv8p5A==&lon=cu7pkk2XGKh9YksCMSg2BQ==&version=36.0&net=wifi&ts= '+ str(t) + '&sign=' + key + '&encryption=1&canal=baidu_cpd1_news&mac=Ft/gmnuXr4kqb/B9ZJB26CKCZ0vHdesSTBiDEVNplbY=&open=&openpath=',
            'http://c.m.163.com/dlist/article/dynamic?from=T1348648756099&offset=40&size=10&fn=1&LastStdTime=0&passport=&devId=w5IMJr/VJZP4nluUZXnpaw==&lat=v7YkY/cxMW8TiRWiqv8p5A==&lon=cu7pkk2XGKh9YksCMSg2BQ==&version=36.0&net=wifi&ts= '+ str(t) + '&sign=' + key + '&encryption=1&canal=baidu_cpd1_news&mac=Ft/gmnuXr4kqb/B9ZJB26CKCZ0vHdesSTBiDEVNplbY=&open=&openpath=',
            'http://c.m.163.com/dlist/article/dynamic?from=T1348648141035&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=w5IMJr/VJZP4nluUZXnpaw==&lat=v7YkY/cxMW8TiRWiqv8p5A==&lon=cu7pkk2XGKh9YksCMSg2BQ==&version=36.0&net=wifi&ts= '+ str(t) + '&sign=' + key + '&encryption=1&canal=baidu_cpd1_news&mac=Ft/gmnuXr4kqb/B9ZJB26CKCZ0vHdesSTBiDEVNplbY=&open=&openpath=',
            'http://c.m.163.com/dlist/article/dynamic?from=T1348648141035&offset=20&size=10&fn=1&LastStdTime=0&passport=&devId=w5IMJr/VJZP4nluUZXnpaw==&lat=v7YkY/cxMW8TiRWiqv8p5A==&lon=cu7pkk2XGKh9YksCMSg2BQ==&version=36.0&net=wifi&ts= '+ str(t) + '&sign=' + key + '&encryption=1&canal=baidu_cpd1_news&mac=Ft/gmnuXr4kqb/B9ZJB26CKCZ0vHdesSTBiDEVNplbY=&open=&openpath=',
            'http://c.m.163.com/dlist/article/dynamic?from=T1348648141035&offset=40&size=10&fn=1&LastStdTime=0&passport=&devId=w5IMJr/VJZP4nluUZXnpaw==&lat=v7YkY/cxMW8TiRWiqv8p5A==&lon=cu7pkk2XGKh9YksCMSg2BQ==&version=36.0&net=wifi&ts= '+ str(t) + '&sign=' + key + '&encryption=1&canal=baidu_cpd1_news&mac=Ft/gmnuXr4kqb/B9ZJB26CKCZ0vHdesSTBiDEVNplbY=&open=&openpath=',
            'http://c.m.163.com/nc/article/list/T1414142214384/0-20.html',
            'http://c.m.163.com/nc/article/list/T1414142214384/20-20.html',
            'http://c.m.163.com/nc/article/list/T1414142214384/40-20.html',
            'http://c.m.163.com/nc/article/list/T1368497029546/0-20.html',
            'http://c.m.163.com/nc/article/list/T1368497029546/20-20.html',
            'http://c.m.163.com/nc/article/list/T1368497029546/40-20.html'
        ]
        category = [
            '要闻', '要闻', '要闻',
            '财经', '财经', '财经',
            '军事', '军事', '军事',
            '新时代', '新时代', '新时代',
            '历史', '历史', '历史']
        for i in range(len(url)):
            yield scrapy.Request(url[i],meta={
                'category': category[i]
            }, callback=self.parse, dont_filter=True)

    def parse(self, response):
        data = json.loads(response.body)
        try:
            try:
                try:
                    try:
                        data =data['T1467284926140']
                    except:
                        data = data['T1348648756099']
                except:
                    data = data['T1348648141035']
            except:
                data = data['T1414142214384']
        except:
            data = data['T1368497029546']

        for i in range(len(data)):
            num = data[i]['docid']
            title = data[i]['title']
            pubt = data[i]['ptime']
            url = 'http://c.m.163.com/nc/article/preload/%s/full.html'%num
            try:
                pic_url = data[i]['imgsrc']
            except:
                pic_url = ''
            yield scrapy.Request(url, meta={
                'title': title,
                'pic_url': pic_url,
                'pubt': pubt,
                'num': num,
                'category': response.meta['category']
            }, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        title = response.meta['title']
        pic_url = response.meta['pic_url']
        publishedDate = response.meta['pubt']
        app_name = '网易新闻'
        describe = ''
        num = response.meta['num']
        data = json.loads(response.body)
        data = data[num]
        content = data['body']
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        pic_more_url = ''
        author = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url = ''
        category = response.meta['category']
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item

    def md5(self,data):
        data = '357541050015819' + data
        import hashlib
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def aes(self, data):
        # CBC模式加密
        # 初始化AES，引入初始向量
        str = self.md5(data)
        key = 'neteasenewsboard'
        AESCipher = AES.new(key, AES.MODE_ECB)
        # 加密
        cipher = AESCipher.encrypt(str)
        return b2a_hex(cipher)

