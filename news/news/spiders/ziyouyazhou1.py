#coding=utf-8
import scrapy
import time,re
from news.items import NewsItem

class ziyouyazhou(scrapy.Spider):
    name = 'ziyouyazhou1'
    start_urls = [
        'https://www.rfa.org/mandarin/search?search_text%3Autf8%3Austring=%E4%B9%A0%E8%BF%91%E5%B9%B3&submit.x=15&submit.y=9'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//div[@class="searchresult"]/div[1]/a/@href').extract()
        title = response.xpath('//div[@class="searchresult"]/div[1]/a/span/text()').extract()
        pubt = response.xpath('//div[@class="searchresult"]/div[2]/text()').extract()
        for i in range(len(links)):
            tit = title[i]
            url = links[i]
            pubtlish = pubt[i]
            print url
            print tit
            print pubtlish
            yield scrapy.Request(url, meta={
                'title': tit,
                'pubt': pubtlish,
                'describe': '',
                'home_url': 'https://www.rfa.org'
            }, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        home_url = response.meta['home_url']
        app_name = '自由亚洲电台'
        pic_url = ''
        author = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        describe = ''
        title = response.xpath('//h1/text()').extract()[0]
        content = response.xpath('//div[@id="storytext"]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in range(0, len(content)):
            contentdata += content[i]
        content = contentdata
        publishedDate = response.meta['pubt']
        try:
            pic_more_url = response.xpath('//div[@id="headerimg"]/img/@src').extract()[0]
        except:
            pic_more_url = ''
        if 'Xinwen' in home_url:
            category = u'要闻'.encode('utf-8')
        elif 'gangtai' in home_url:
            category = u'港台'.encode('utf-8')
        elif 'shaoshuminzu' in home_url:
            category = u'少数民族'.encode('utf-8')
        elif 'jingmao' in home_url:
            category = u'经贸'.encode('utf-8')
        elif 'zhengzhi' in home_url:
            category = u'政治'.encode('utf-8')
        elif 'renquanfazhi' in home_url:
            category = u'人权法制'.encode('utf-8')
        elif 'meiti' in home_url:
            category = u'媒体'.encode('utf-8')
        elif 'shehui' in home_url:
            category = u'社会'.encode('utf-8')
        elif 'guojishijiao' in home_url:
            category = u'国际'.encode('utf-8')
        elif 'junshiwaijiao' in home_url:
            category = u'军事外交'.encode('utf-8')
        else:
            category = u'要闻'.encode('utf-8')
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item





