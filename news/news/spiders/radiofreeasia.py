#coding=utf-8
import scrapy
import time,re
from news.items import NewsItem

class radiofreeasia(scrapy.Spider):
    name = 'radiofreeasia'
    start_urls = [
        'https://www.rfa.org/mandarin/Xinwen',#要闻
        'https://www.rfa.org/mandarin/yataibaodao/gangtai',#港台
        'https://www.rfa.org/mandarin/yataibaodao/zhengzhi',#政治
        'https://www.rfa.org/mandarin/yataibaodao/shehui',#社会
        'https://www.rfa.org/mandarin/guojishijiao',#国际
        'https://www.rfa.org/mandarin/yataibaodao/renquanfazhi',#人权法治
    ]

    def parse(self, response):
        links = response.xpath('//div[@class="sectionteaser"]/h2/a/@href').extract()
        for i in range(0,len(links)):
            url = links[i]
            yield scrapy.Request(url,meta={
                'home_url':response.url
            },callback=self.parse_item)


    def parse_item(self,response):
        home_url = response.meta['home_url']
        app_name = 'radiofreeasia'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_url = ''
        describe = ''
        author = ''
        content = response.xpath('//div[@id="storytext"]').extract()
        # content = "".join(content)
        # content = content.replace("\n", "").replace(" ", "")
        content=content.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in range(0, len(content)):
            contentdata += content[i]
        content = contentdata
        title = response.xpath('//h1/text()').extract()[0]
        publishedDate = response.xpath('//span[@id="story_date"]/text()').extract()[0]
        try:
            pic_more_url = response.xpath('//div[@id="headerimg"]/img/@src').extract()[0]
        except:
            pic_more_url = ''
        if 'Xinwen' in home_url:
            category = u'要闻'.encode('utf-8')
        elif 'gangtai' in home_url:
            category = u'港台'.encode('utf-8')
        elif 'zhengzhi' in home_url:
            category = u'政治'.encode('utf-8')
        elif 'shehui' in home_url:
            category = u'社会'.encode('utf-8')
        elif 'guojishijiao' in home_url:
            category = u'国际'.encode('utf-8')
        else:
            category = u'人权法治'.encode('utf-8')

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
