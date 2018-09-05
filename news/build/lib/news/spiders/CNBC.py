#coding=utf-8
import time,re,json
from news.items import NewsItem
import scrapy

class cnbc(scrapy.Spider):
    name = 'cnbc'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-1', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def start_requests(self):
        category = [
            'immigration-border-crisis', 'brexit-referendum',
            'puerto-rico-crisis', 'legal-pot', 'europess-border-crisis',
            'hazing-in-america'
                    ]
        for i in range(len(category)):
            url = 'https://deviceservices.nbcnews.com/portal/taxonomy/dreamypal?type=storyline&asset=android_adaptive&slug=%s&_devicefeed_=%s'%(category[i], category[i])
            yield scrapy.Request(url, meta={
                'category': category[i]
            }, callback=self.parse_item)

    def parse_item(self, response):
        category = response.meta['category']
        app_name = 'CNBC'
        data = json.loads(response.body)
        data = data['entries']
        for i in range(len(data)):
            url = data[i]['id']
            pubt = data[i]['published']
            title = data[i]['title']
            try:
                content = data[i]['content']
            except:
                content = ''
            yield scrapy.Request(url,meta={
                'pubt': pubt,
                'category': category,
                'app_name': app_name,
                'content':content,
                'title':title
            }, callback=self.parse_one)

    def parse_one(self, response):
        category = response.meta['category']
        app_name = response.meta['app_name']
        publishedDate = response.meta['pubt']
        publishedDate = publishedDate.replace('T',' ').replace('Z','')
        pic_url = ''
        author = ''
        describe = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url = 'http://devicestransform-stg.elasticbeanstalk.com/'
        # title = response.xpath('//h1/text()').extract()[0]
        title = response.meta['title']
        pic_more_url = ''
        content = response.meta['content']
        if len(content) <= 100:
            content = response.xpath('//p').extract()
            contentt = ''
            for i in range(len(content)):
                contentt += content[i]
            content = contentt.replace('<p>', '').replace('</p>', '').replace('\t', '')
        content = content.replace('\n', '').replace('\r', '')
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata

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