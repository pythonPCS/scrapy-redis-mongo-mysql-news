#coding=utf-8
import re,time,json
from news.items import NewsItem
import scrapy
from news.DataResource import TransportData
class zsdzb(scrapy.Spider):
    name='zhongshidianzi'
    start_urls=[
        # 'http://www.chinatimes.com/politic/total/?page=2',#政治
        # 'http://www.chinatimes.com/world/total?page=2',#国际
        'http://www.chinatimes.com/chinese/total?page=2',#两岸
        # 'http://www.chinatimes.com/armament/total/?page=2',#军事
        # 'http://www.chinatimes.com/money/realtimenews?page=2',#财经
    ]
    base_url='http://www.chinatimes.com'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self,response):
        for i in range(1,5):
            if 'realtimenews' in response.url:
                url='http://www.chinatimes.com/politic/total/?page=%s'%i
            elif 'politic' in response.url:
                url='http://www.chinatimes.com/life/total?page=%s'%i
            elif 'star' in response.url:
                url='http://www.chinatimes.com/star/total?page=%s'%i
            elif 'life' in response.url:
                url='http://www.chinatimes.com/life/total?page=%s'%i
            elif 'society' in response.url:
                url='http://www.chinatimes.com/society/total?page=%s'%i
            elif 'world' in response.url:
                url='http://www.chinatimes.com/world/total?page=%s'%i
            elif 'chinese' in response.url:
                url='http://www.chinatimes.com/chinese/total?page=%s'%i
            elif 'sports' in response.url:
                url='http://www.chinatimes.com/sports/total?page=%s'%i
            elif 'armament' in response.url:
                url='http://www.chinatimes.com/armament/total/?page=%s'%i
            elif 'travel' in response.url:
                url='http://www.chinatimes.com/travel/travel-hotnews?page='
            elif 'health' in response.url:
                url='http://www.chinatimes.com/healthcare/total?page=%s'%i
            elif 'opinion' in response.url:
                url='http://opinion.chinatimes.com/total/?page=%s'%i
            elif 'money' in response.url:
                url='http://www.chinatimes.com/money/realtimenews?page=%s'%i
            elif 'hottopic' in response.url:
                url='http://hottopic.chinatimes.com/total/?page=%s'%i
            elif 'tube' in response.url:
                url='http://tube.chinatimes.com/total?page=%s'%i
            elif 'styletc' in response.url:
                url='http://styletc.chinatimes.com/list/%s'%i
            elif 'hottv' in response.url:
                url='http://hottv.chinatimes.com/total/?page=%s'%i
            else:
                url=''
            yield scrapy.Request(url,callback=self.parse_one)

    def parse_one(self,response):
        links_url = response.xpath('//li[@class="clear-fix"]/h3/a/@href').extract()
        for i in range(len(links_url)):
            url = 'http://www.chinatimes.com' + links_url[i]
            yield scrapy.Request(url,callback=self.parse_two)

    def parse_two(self,response):
        title = response.xpath('//h1').extract()
        title = title[0].replace('\t','').replace('\n','').replace('\r','').replace(' ','')
        title = re.findall('>(.*?)<',title)
        tit = ''
        for i in range(len(title)):
            tit += title[i]
        title = tit
        app_name = '中时电子报'
        pic_url = ''
        describe = ''
        author = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url = 'http://www.chinatimes.com'
        if 'realtimenews' in response.url:
            category=u'即时'.encode('utf-8')
        elif 'politic' in response.url:
            category = u'政治'.encode('utf-8')
        elif 'world' in response.url:
            category = u'国际'.encode('utf-8')
        elif 'chinese' in response.url:
            category = u'两岸'.encode('utf-8')
        elif 'money' in response.url:
            category = u'财经'.encode('utf-8')
        else:
            category = u'即时'.encode('utf-8')
        publishedDate = response.xpath('//time/text()').extract()[0].replace('\t', '').replace('\n', '').replace('\r','').replace(' ', '').replace('年', '-').replace('月', '-').replace('日', ' ')
        try:
            content=response.xpath('//article[@class="arttext marbotm clear-fix"]').extract()
            content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('>(.*?)<', content)
            contentdata = ''
            for i in range(0,len(content)):
                contentdata += content[i]
            content = contentdata
        except:
            content=response.xpath('//div[@class="page-cnt clear-fix"]/article').extract()
            content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('>(.*?)<', content)
            contentdata = ''
            for i in range(0,len(content)):
                contentdata += content[i]
            content = contentdata
        try:
            pic_more_url=response.xpath('//div[@class="picbox2"]/a/@href').extract()
            pic_more_url=pic_more_url[0]
        except:
            content = response.xpath('//article').extract()
            content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            pic_more_url=re.findall('<imgsrc="(.*?)"',content)
            pic_more_url1=[]
            for i in range(0,len(pic_more_url)):
                pic_more_url1.append(pic_more_url[i])
            pic_more_url=str(set(pic_more_url1))
        print "标题", title
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
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            self.count = self.count + 1
            item['count'] = self.count
            yield item


