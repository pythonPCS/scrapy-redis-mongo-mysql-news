#coding=utf-8
import scrapy
import json,re,time
from news.items import NewsItem
from lxml.etree import HTML

class eluosi(scrapy.Spider):
    name = 'eluosiweixing'
    start_urls = [
        'http://sputniknews.cn/china/',#中国
        'http://sputniknews.cn/russia/',
        'http://sputniknews.cn/russia_china_relations/',
        'http://sputniknews.cn/politics/',
        'http://sputniknews.cn/economics/',
        'http://sputniknews.cn/military/',
        'http://sputniknews.cn/society/',
        'http://sputniknews.cn/science/',
        'http://sputniknews.cn/radio/'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-01', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = response.xpath('//ul[@class="b-stories__list"]/li/a/@href').extract()
        pic = response.xpath('//ul[@class="b-stories__list"]/li/a/img/@src').extract()
        title = response.xpath('//ul[@class="b-stories__list"]/li/div/div[2]/h2/a/text()').extract()
        pubt = response.xpath('//ul[@class="b-stories__list"]/li/div/span/text()').extract()
        desc = response.xpath('//ul[@class="b-stories__list"]/li/div/div[2]/div/p/text()').extract()
        for i in range(len(links)):
            url = 'http://sputniknews.cn' + links[i]
            pic_url = pic[i]
            tit = title[i]
            published = pubt[i]
            try:
                describe = desc[i]
            except:
                describe = ''
            yield scrapy.Request(url, meta={
                'title': tit,
                'pic_url':pic_url,
                'publishedDate':published,
                'describe':describe,
                'home_url':response.url
            }, callback=self.parse_item, dont_filter=True)


    def parse_item(self, response):
        title = response.meta['title']
        pic_url = response.meta['pic_url']
        publishedDate = response.meta['publishedDate']
        p = publishedDate.split(' ')
        p1 = p[0]
        p2 = p[1]
        publishedDate = p2.replace('年', '-').replace('月', '-').replace('日', ' ') + p1 + ':00'
        describe = response.meta['describe']
        app_name = '俄罗斯卫星中文网'
        author = ''
        home_url = response.meta['home_url']
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content = response.xpath('//div[@itemprop="articleBody"]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '')
        Sector = HTML(content)
        content = content.replace(' ','')
        pic_more_url = Sector.xpath('//img/@src')
        pic = []
        for i in range(len(pic_more_url)):
            pic.append(pic_more_url[i])
        pic_more_url = str(pic)
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in range(0, len(content)):
            contentdata += content[i]
        content = contentdata
        if 'china' in home_url:
            category = '中国'
        elif 'russia' in home_url:
            category = '俄罗斯'
        elif 'politics' in home_url:
            category = '政治'
        elif 'economics' in home_url:
            category = '经济'
        elif 'military' in home_url:
            category = '军事'
        elif 'society' in home_url:
            category = '社会'
        elif 'science' in home_url:
            category = '科学'
        elif 'radio' in home_url:
            category = '广播'
        else:
            category = '俄中关系'
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
            numappName = self.readjson()
            if len(numappName) == 0:
                items = {
                    'url': response.url,
                    'title':item['title']
                }
                with open('eluosiweixing.json', 'a+') as fp:
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
                        'title':item['title']
                    }
                    with open('eluosiweixing.json', 'a+') as fp:
                        line = json.dumps(dict(items), ensure_ascii=False) + '\n'
                        fp.write(line)
                    yield item

    def readjson(self):
        s = []
        file_object = open('eluosiweixing.json', 'r')
        try:
            while True:
                line = file_object.readline()
                data = json.loads(line)
                s.append(data)
        finally:
            return s




