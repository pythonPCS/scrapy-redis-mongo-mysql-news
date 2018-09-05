#coding=utf-8
import json
import scrapy
import time,re,time
from news.items import NewsItem
from news.DataResource import TransportData

class fenghuang(scrapy.Spider):
    name = 'fenghuangxinwen'
    start_urls = [
        'http://api.iclient.ifeng.com/ClientNews?id=SYLB10,SYDT10&page=1&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#头条
        'http://api.iclient.ifeng.com/ClientNews?id=SYLB10,SYDT10&page=2&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#头条
        'http://api.iclient.ifeng.com/ClientNews?id=SYLB10,SYDT10&page=3&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#头条
        'http://api.iclient.ifeng.com/ClientNews?id=SYLB10,SYDT10&page=4&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#头条
        'http://api.iclient.ifeng.com/ClientNews?id=SYLB10,SYDT10&page=5&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#头条
        'http://api.iclient.ifeng.com/ClientNews?id=TWOSES,FOCUSTWOSES&page=1&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#两会
        'http://api.iclient.ifeng.com/ClientNews?id=TWOSES,FOCUSTWOSES&page=2&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#两会
        'http://api.iclient.ifeng.com/ClientNews?id=TWOSES,FOCUSTWOSES&page=3&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#两会
        'http://api.iclient.ifeng.com/ClientNews?id=TWOSES,FOCUSTWOSES&page=4&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#两会
        'http://api.iclient.ifeng.com/ClientNews?id=TWOSES,FOCUSTWOSES&page=5&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#两会
        'http://api.iclient.ifeng.com/ClientNews?id=19METTING&page=1&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#新时代
        'http://api.iclient.ifeng.com/ClientNews?id=19METTING&page=2&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#新时代
        'http://api.iclient.ifeng.com/ClientNews?id=19METTING&page=3&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#新时代
        'http://api.iclient.ifeng.com/ClientNews?id=19METTING&page=4&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#新时代
        'http://api.iclient.ifeng.com/ClientNews?id=19METTING&page=5&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#新时代
        'http://api.iclient.ifeng.com/ClientNews?id=YAOWEN223&page=1&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#要闻
        'http://api.iclient.ifeng.com/ClientNews?id=YAOWEN223&page=2&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#要闻
        'http://api.iclient.ifeng.com/ClientNews?id=YAOWEN223&page=3&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#要闻
        'http://api.iclient.ifeng.com/ClientNews?id=YAOWEN223&page=4&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#要闻
        'http://api.iclient.ifeng.com/ClientNews?id=YAOWEN223&page=5&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#要闻
        'http://api.iclient.ifeng.com/ClientNews?id=CJ33,FOCUSCJ33,HNCJ33&page=1&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#财经
        'http://api.iclient.ifeng.com/ClientNews?id=CJ33,FOCUSCJ33,HNCJ33&page=2&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#财经
        'http://api.iclient.ifeng.com/ClientNews?id=CJ33,FOCUSCJ33,HNCJ33&page=3&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#财经
        'http://api.iclient.ifeng.com/ClientNews?id=CJ33,FOCUSCJ33,HNCJ33&page=4&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#财经
        'http://api.iclient.ifeng.com/ClientNews?id=CJ33,FOCUSCJ33,HNCJ33&page=5&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#财经
        'http://api.iclient.ifeng.com/ClientNews?id=CJ33,FOCUSCJ33,HNCJ33&page=6&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#财经
        'http://api.iclient.ifeng.com/ClientNews?id=LS153,FOCUSLS153&page=1&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#历史
        'http://api.iclient.ifeng.com/ClientNews?id=LS153,FOCUSLS153&page=2&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#历史
        'http://api.iclient.ifeng.com/ClientNews?id=LS153,FOCUSLS153&page=3&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#历史
        'http://api.iclient.ifeng.com/ClientNews?id=LS153,FOCUSLS153&page=4&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#历史
        'http://api.iclient.ifeng.com/ClientNews?id=LS153,FOCUSLS153&page=5&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#历史
        # 'http://api.iclient.ifeng.com/ClientNews?id=GJPD,FOCUSGJPD&page=1&newShowType=1&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#国际
        'http://api.iclient.ifeng.com/irecommendList?userId=867637959598351&count=6&gv=5.2.0&av=5.2.0&uid=867637959598351&deviceid=867637959598351&proid=ifengnews&os=android_22&df=androidphone&vt=5&screen=720x1280&publishid=5008',#推荐
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        data = json.loads(response.body)
        try:
            data = data[0]['item']
            for i in range(0,len(data)):
                title = data[i]['title']
                urlt = data[i]['link']['weburl']
                yield scrapy.Request(urlt,meta={
                    'title':title,
                    'home_url':response.url
                },callback=self.parse_item,dont_filter=True)
        except:
            data = data['item']
            for i in range(0,len(data)):
                title = data[i]['title']
                urlt = data[i]['link']['weburl']
                yield scrapy.Request(urlt,meta={
                    'title':title,
                    'home_url':response.url
                },callback=self.parse_item,dont_filter=True)

    def parse_item(self,response):
        app_name = '凤凰新闻'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_url = ''
        title = response.meta['title']
        home_url = response.meta['home_url']
        author = ''
        describe = ''
        try:
            publishedDate = response.xpath('//p[@class="n-i-time"]/text()').extract()[0]
        except:
            publishedDate = '2018-05-01 00:00:00'
        try:
            content = response.xpath('//div[@class="n-words"]').extract()
            contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('>(.*?)<', contentt)
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
            pic_more_url = response.xpath('//img[@class="z-img lazy"]/@src').extract()
            pic_more_url1 = []
            for i in range(0, len(pic_more_url)):
                if 'http' not in pic_more_url[i]:
                    pic_more_urlt = 'http:' + pic_more_url[i]
                    pic_more_url1.append(pic_more_urlt)
                else:
                    pic_more_url1.append(pic_more_url[i])

            pic_more_url = str(set(pic_more_url1))
            if 'SYLB10,SYDT10' in home_url:
                category = u'头条'.encode('utf-8')
            elif 'TWOSES,FOCUSTWOSES' in home_url:
                category = u'要闻'.encode('utf-8')
            elif '19METTING' in home_url:
                category = u'新时代'.encode('utf-8')
            elif 'YAOWEN223' in home_url:
                category = u'要闻'.encode('utf-8')
            elif 'CJ33,FOCUSCJ33,HNCJ33' in home_url:
                category = u'财经'.encode('utf-8')
            elif 'LS153,FOCUSLS153' in home_url:
                category = u'历史'.encode('utf-8')
            elif 'GJPD,FOCUSGJPD' in home_url:
                category = u'国际'.encode('utf-8')
            else:
                category = u'推荐'.encode('utf-8')
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
            item = NewsItem()
            item['app_name'] = app_name
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
            timeArray = time.strptime(publishedDate, "%Y/%m/%d %H:%M")
            timenum = int(time.mktime(timeArray))
            if timenum >= self.timeStamp:
                publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
                item['publishedDate'] = publishedDate
                self.count += 1
                item['count'] = self.count
                yield item
        except:
            pass

