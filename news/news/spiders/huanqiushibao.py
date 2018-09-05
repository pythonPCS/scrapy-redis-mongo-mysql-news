#coding=utf-8
import time,re,json
from news.items import NewsItem
import scrapy

class huanqiu(scrapy.Spider):
    name = 'huanqiushibao'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def start_requests(self):
        url = [
            'http://api.hqtime.huanqiu.com/api/news/list/general/hot/1',
            'http://api.hqtime.huanqiu.com/api/news/list/general/hot/2',
            'http://api.hqtime.huanqiu.com/api/news/list/general/international/1',
            'http://api.hqtime.huanqiu.com/api/news/list/general/international/2',
            'http://api.hqtime.huanqiu.com/api/news/list/general/military/1',
            'http://api.hqtime.huanqiu.com/api/news/list/general/military/2',
            'http://api.hqtime.huanqiu.com/api/news/list/general/taihai/1',
            'http://api.hqtime.huanqiu.com/api/news/list/general/taihai/2',
            'http://api.hqtime.huanqiu.com/api/news/list/general/overseas/1',
            'http://api.hqtime.huanqiu.com/api/news/list/general/overseas/2',
            'http://api.hqtime.huanqiu.com/api/news/list/general/finance/1',
            'http://api.hqtime.huanqiu.com/api/news/list/general/finance/2'
            ]
        params = {
            "clientversion": "v1"
        }
        for i in range(len(url)):
            yield scrapy.Request(url[i], headers=params, callback=self.parse, dont_filter=True)

    def parse(self, response):
        data = json.loads(response.body)
        data = data['data'][0]['group_data']
        for i in range(len(data)):
            url = data[i]['source_url']
            title = data[i]['title']
            pubt = data[i]['time_publish']
            if float(pubt) >= self.timeStamp:
                yield scrapy.Request(url, meta={
                    'title':title,
                    'pubt':pubt,
                    'home_url':response.url
                }, callback=self.parse_item)

    def parse_item(self, response):
        title = response.meta['title']
        publishedDate = response.meta['pubt']
        publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
        app_name = '环球时报'
        author = ''
        describe = ''
        pic_url = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url = response.meta['home_url']
        if 'hot' in home_url:
            category = '热点'
        elif 'international' in home_url:
            category = '国际'
        elif 'military' in home_url:
            category = '军事'
        elif 'taihai' in home_url:
            category = '台湾'
        elif 'overseas' in home_url:
            category = '海外看中国'
        elif 'finance' in home_url:
            category = '财经'
        else:
            category = '热点'
        try:
            content = response.xpath('//div[@id="articleText"]').extract()
            content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('>(.*?)<', content)
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
        except:
            content = response.xpath('//p').extract()
            contentt = ''
            for i in range(len(content)):
                contentt += content[i]
            content = contentt.replace('<p>', '').replace('</p>', '').replace(' ', '').replace('\t', '')
            content = content.replace('\n', '').replace('\r', '')
            # content = re.findall('>(.*?)<', content)
            # contentdata = ''
            # for i in content:
            #     contentdata += i
            # content = contentdata
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