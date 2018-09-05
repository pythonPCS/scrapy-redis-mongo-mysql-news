#coding=utf-8
import json,re,time
import scrapy
from news.items import NewsItem
from news.DataResource import TransportData

class zgjw(scrapy.Spider):
    name='zhongguojinwen'
    start_urls=[
        'http://feeds.feedburner.com/bnews-guoji', #国际新闻
        'http://feeds.feedburner.com/kzgnews',     #中国新闻
        'http://feeds.feedburner.com/bannednews',  #中国禁闻
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self,response):
        html = response.body
        tt = re.findall('<div class="postcopyright">(.*?)<a href="(.*?)">(.*?)</a>', html)
        for i in range(0,len(tt)):
            url=tt[i][1]
            title=tt[i][2]
            yield scrapy.Request(url,meta={
                'home_url':response.url,
                'title':title
            },callback=self.parse_item)

    def parse_item(self,response):
        home_url=response.meta['home_url']
        title=response.meta['title']
        pubTime=re.findall('<div class="postmeat ac">(.*?)<a',response.body)[0]
        pubTime=pubTime.replace(u'年','-').replace(u'月','-').replace(u'日','').replace('&nbsp;','')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        describe=''
        app_name='中国禁闻'
        pic_url=''
        content=response.xpath('//div[@class="entry"]').extract()
        contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', contentt)
        pic_more_url = re.findall('<img(.*?)src="(.*?)"',contentt)
        pic_more_url1 = []
        for i in range(0, len(pic_more_url)):
            pic_more_url1.append(pic_more_url[i][1])
        pic_more_url = str(set(pic_more_url1))
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        author = ''
        if u'neimunews' in home_url:
            category = u'中共高层内幕'.encode('utf-8')
        elif u'bnews-guoji' in home_url:
            category = u'国际新闻'.encode('utf-8')
        elif u'kzgnews' in home_url:
            category = u'中国新闻'.encode('utf-8')
        elif u'bannednews' in home_url:
            category = u'中国禁闻'.encode('utf-8')
        else:
            category = u'中国禁闻'.encode('utf-8')
        publishedDate = pubTime
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
        print pubTime
        # t1 = pubTime.split(' ')[0]
        # t2 = pubTime.split(' ')[1]
        # pubTime = t1 + ' ' + t2
        # timeArray = time.strptime(pubTime, "%Y-%m-%d %H:%M")
        # publishedDate = time.mktime(timeArray)

        try:
            t1 = pubTime.split(' ')[0]
            t2 = pubTime.split(' ')[1]
            t = t1 + ' ' + t2
            timeArray = time.strptime(t, "%Y-%m-%d %H:%M")
        except:
            t = pubTime.split(' ')[0]
            timeArray = time.strptime(t, "%Y-%m-%d")
        publishedDate = time.mktime(timeArray)
        if publishedDate >= self.timeStamp:
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            item['publishedDate'] = publishedDate
            self.count = self.count + 1
            item['count'] = self.count
            yield item

