#coding=utf-8
import scrapy
import time,re
from news.items import NewsItem

class ziyouyazhou(scrapy.Spider):
    name = 'ziyouyazhou'
    start_urls = [
        'https://www.rfa.org/mandarin/Xinwen/story_archive?b_start:int=0',#要闻
        'https://www.rfa.org/mandarin/yataibaodao/gangtai/story_archive?b_start:int=0',#港台
        'https://www.rfa.org/mandarin/yataibaodao/shaoshuminzu/story_archive?b_start:int=0',#少数民族
        'https://www.rfa.org/mandarin/yataibaodao/jingmao/story_archive?b_start:int=0',#经贸
        'https://www.rfa.org/mandarin/yataibaodao/zhengzhi/story_archive?b_start:int=0',#政治
        'https://www.rfa.org/mandarin/yataibaodao/renquanfazhi/story_archive?b_start:int=0',#人权法治
        'https://www.rfa.org/mandarin/yataibaodao/meiti/story_archive?b_start:int=0',#媒体网络
        'https://www.rfa.org/mandarin/yataibaodao/junshiwaijiao/story_archive?b_start:int=0',#军事外交
        'https://www.rfa.org/mandarin/pinglun/story_archive?b_start:int=0',#评论
        'https://www.rfa.org/mandarin/duomeiti/story_archive?b_start:int=0',#多媒体
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-13', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//div[@class="searchresult"]/div[1]/a/@href').extract()
        if len(links) != 0:
            for i in range(len(links)):
                url = links[i]
                yield scrapy.Request(url, meta={
                    'home_url': response.url
                }, callback=self.parse_item,dont_filter=True)
        else:
            links = response.xpath('//div[@class="sectionteaser"]/h2/a/@href').extract()
            if len(links) > 0:
                for i in range(len(links)):
                    url = links[i]
                    yield scrapy.Request(url, meta={
                        'home_url': response.url
                    }, callback=self.parse_item, dont_filter=True)
            else:
                print "文章连接错误！"


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
        publishedDate = response.xpath('//span[@id="story_date"]/text()').extract()[0]
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item





