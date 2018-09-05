#coding=utf-8
import scrapy
import json, re, time
from news.items import NewsItem
from lxml.etree import HTML
class yindushibao(scrapy.Spider):
    name = 'yindushibao'
    start_urls = [
        'http://timesofindia.indiatimes.com/feeds/newslistingfeedmc/feedtype-sjson,msid-1081479906,tag-alrt,uid-Entertainment-01,category-Entertainment-01,t-f.cms?platform=android&andver=498&adreqfrm=sec',
        'https://timesofindia.indiatimes.com/feeds/homenewslistingfeed/feedtype-sjson,msid-51396865,tag-strt,uid-Top-01.cms?platform=android&andver=498&adreqfrm=home',
        'http://timesofindia.indiatimes.com/feeds/newslistingfeedmc/feedtype-sjson,msid--2128932452,tag-alrt,uid-City-01,category-City-01,t-f.cms?platform=android&andver=498&adreqfrm=sec',
        'http://timesofindia.indiatimes.com/feeds/newslistingfeedmc/feedtype-sjson,msid-4440100,tag-alrt,uid-India-01.cms?platform=android&andver=498&adreqfrm=sec',
        'http://timesofindia.indiatimes.com/feeds/newslistingfeed/feedtype-sjson,msid-62542876,tag-alrt,uid-StateElec2017-01,category-KarnatakaElect2018-01.cms?platform=android&andver=498&adreqfrm=sec',
        'http://timesofindia.indiatimes.com/feeds/newslistingfeedmc/feedtype-sjson,msid-1898184,tag-alrtdf,uid-World-01.cms?platform=android&andver=498&adreqfrm=sec',
        'http://timesofindia.indiatimes.com/feeds/newslistingfeedmc/feedtype-sjson,msid-30359486,tag-alrtdf,uid-World-01,category-WorldUS-01.cms?platform=android&andver=498&adreqfrm=sec'
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
            data = data['items']
        except:
            data = data['items']
        for i in range(len(data)):
            try:
                title = data[i]['hl']
                url = data[i]['wu']
                try:
                    pubt = data[i]['upd']
                except:
                    pubt = data[i]['lpt']
                if float(pubt)/1000 >= self.timeStamp:
                    publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(pubt)/1000))
                    yield scrapy.Request(url,meta={
                        'title':title,
                        'home_url': response.url,
                        'pubt':publishedDate
                    }, callback=self.parse_item)
            except:
                pass

    def parse_item(self, response):
        title = response.meta['title']
        home_url = response.meta['home_url']
        app_name = '印度时报'
        pic_url = ''
        describe = ''
        author = ''
        publishedDate = response.meta['pubt']
        content = response.xpath('//div[@class="Normal"]').extract()
        try:
            contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace('　　', '').replace(' ', '')
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
            content = contentt.replace('<p>', '').replace('</p>', '').replace(' ', '').replace('\t', '')
            content = content.replace('\n', '').replace('\r', '')
        pic_more_url = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        category = ''

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