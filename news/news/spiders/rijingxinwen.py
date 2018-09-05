#coding=utf-8
import scrapy
import json,re,time
from news.items import NewsItem
from lxml.etree import HTML

class rijing(scrapy.Spider):
    name = 'rijingxinwen'
    start_urls = [
        'https://cn.nikkei.com/politicsaeconomy.html?limitstart=0',#政经观察
        'https://cn.nikkei.com/politicsaeconomy.html?start=10',#政经观察
        'https://cn.nikkei.com/china.html?limitstart=0',#中国
        'https://cn.nikkei.com/china.html?start=10',#中国
        'https://cn.nikkei.com/industry.html?limitstart=0',#产品聚焦
        'https://cn.nikkei.com/industry.html?start=10',#产品聚焦
        'https://cn.nikkei.com/columnviewpoint.html?limitstart=0',#专栏/观点
        'https://cn.nikkei.com/columnviewpoint.html?start=10',#专栏/观点
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-01', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//dl[@class="newsContent02"]/dt/a/@href').extract()
        title = response.xpath('//dl[@class="newsContent02"]/dt/a/text()').extract()
        pubt = response.xpath('//dl[@class="newsContent02"]/dt/span/text()').extract()
        desc = response.xpath('//dl[@class="newsContent02"]/dd/div/text()').extract()
        if len(links) == len(desc):
            for i in range(len(desc)):
                url = 'https://cn.nikkei.com' + links[i]
                tit = title[i]
                describe = desc[i]
                publish = pubt[i].replace('(','').replace(')','').replace('/','-')
                yield scrapy.Request(url , meta={
                    'title': tit,
                    'describe': describe,
                    'published': publish,
                    'home_url': response.url
                }, callback=self.parse_item, dont_filter=True)
        else:
            for i in range(len(desc)):
                url = 'https://cn.nikkei.com' + links[i]
                tit = title[i]
                describe = ''
                publish = pubt[i].replace('(','').replace(')','').replace('/','-')
                yield scrapy.Request(url, meta={
                    'title': tit,
                    'describe': describe,
                    'published': publish,
                    'home_url': response.url
                }, callback=self.parse_item)

    def parse_item(self, response):
        title = response.meta['title']
        describe = response.meta['describe']
        home_url = response.meta['home_url']
        publishedDate = response.meta['published']
        app_name = '日经新闻网'
        pic_url = ''
        author = ''
        if 'politicsaeconomy' in home_url:
            category = '政经观察'
        elif 'china' in home_url:
            category = '中国'
        elif 'industry' in home_url:
            category = '产品聚焦'
        elif 'columnviewpoint' in home_url:
            category = '专栏/观点'
        else:
            category = '政经观察'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content = response.xpath('//div[@id="contentDiv"]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '')
        Sector = HTML(content)
        content = content.replace(' ', '')
        pic_more_url = Sector.xpath('//img/@src')
        pic = []
        if len(pic_more_url) > 2:
            for i in range(len(pic_more_url)):
                try:
                    pic.append('https://cn.nikkei.com' + pic_more_url[i+2])
                except:
                    pic_more_url = str(pic)
                    break
        else:
            pic_more_url = ''
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in range(0, len(content)):
            contentdata += content[i]
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d")
        timenum = int(time.mktime(timeArray))
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            numappName = self.readjson()
            if len(numappName) == 0:
                items = {
                    'url': response.url,
                    'title': item['title']
                }
                with open('rijingxinwenwang.json', 'a+') as fp:
                    line = json.dumps(dict(items), ensure_ascii=False) + '\n'
                    fp.write(line)
                yield item
            else:
                for i in range(len(numappName)):
                    if numappName[i]['url'] == response.url or numappName[i]['title'] == item['title']:
                        return
                else:
                    items = {
                        'url': response.url,
                        'title': item['title']
                    }
                    with open('rijingxinwenwang.json', 'a+') as fp:
                        line = json.dumps(dict(items), ensure_ascii=False) + '\n'
                        fp.write(line)
                    yield item

    def readjson(self):
        s = []
        file_object = open('rijingxinwenwang.json', 'r')
        try:
            while True:
                line = file_object.readline()
                data = json.loads(line)
                s.append(data)
        finally:
            return s



