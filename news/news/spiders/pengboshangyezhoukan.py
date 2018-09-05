#coding=utf-8
import scrapy
import re,json,time
from news.items import NewsItem
from lxml.etree import HTML

class pengbo(scrapy.Spider):
    name = 'pengbo'
    time_str1 = time.strftime("%Y-%m-%d %H:%M:%S")
    timeArray1 = time.strptime(time_str1, "%Y-%m-%d %H:%M:%S")
    timeStamp1 = int(time.mktime(timeArray1))
    start_urls = [
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_1600/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#专访
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_18/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#特写
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_244/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#观点
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_12/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#金融
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_11/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#科技
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_19/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#全球
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_1490/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#AI
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_20/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#公司
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_21/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#政策
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_13/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#生活
        'http://content.cdn.bb.bbwc.cn/slateInterface/v9/app_1/android/tag/cat_304/articlelist?updatetime=%s&appVersion=4.5.7'%timeStamp1,#能源
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        data = json.loads(response.body)
        data = data['articletag'][0]['article']
        for i in range(len(data)):
            title = data[i]['title']
            print title
            pubt = data[i]['updatetime']
            publishedDater = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(pubt)))
            print publishedDater
            describe = data[i]['desc']
            url = data[i]['phonepagelist'][0]['url']
            category = data[i]['catname']
            if int(pubt) >= self.timeStamp:
                publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(pubt)))
                yield scrapy.Request(url, meta={
                    'title':title,
                    'describe':describe,
                    'pubt':publishedDate,
                    'home_url':response.url,
                    'category':category
                }, callback=self.parse_item)

    def parse_item(self, response):
        title = response.meta['title']
        describe = response.meta['describe']
        publishedDate = response.meta['pubt']
        author = ''
        pic_url = ''
        app_name = '彭博商业周刊'
        home_url = response.meta['home_url']
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if 'cat_1600/' in home_url:
            category = '专访'
        elif 'cat_18/' in home_url:
            category = '特写'
        elif 'cat_244/' in home_url:
            category = '观点'
        elif 'cat_12/' in home_url:
            category = '金融'
        elif 'cat_11/' in home_url:
            category = '科技'
        elif 'cat_19/' in home_url:
            category = '全球'
        elif 'cat_1490/' in home_url:
            category = 'AI'
        elif 'cat_20/' in home_url:
            category = '公司'
        elif 'cat_21/' in home_url:
            category = '政策'
        elif 'cat_13/' in home_url:
            category = '生活'
        else:
            category = '能源'
        category = response.meta['category']
        try:
            content = response.xpath('//div[@class="bottom-content"]').extract()
            contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('>(.*?)<', contentt)
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
        except:
            content = response.xpath('//p').extract()
            contentt = ''
            for i in range(len(content)):
                contentt += content[i]
            content = contentt
            contentt = content.replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('>(.*?)<', contentt)
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
        pic_more_url = ''
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
