#coding=utf-8
import scrapy
import re,time
from news.items import NewsItem

class tianxiazazhi(scrapy.Spider):
    name = 'tianxiazazhimeiribao'
    start_urls = [
        'https://www.cw.com.tw/masterChannel.action?idMasterChannel=7',#产业
        'https://www.cw.com.tw/masterChannel.action?idMasterChannel=9',#国际
        'https://www.cw.com.tw/masterChannel.action?idMasterChannel=12',#环境

    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-13', "%Y-%m-%d")
    # a = "2018-04-05 00:00:00"
    # timeArray = time.strptime(a,"%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        links = response.xpath('//div[@class="articleGroup"]/section/div[2]/h3/a/@href').extract()
        title = response.xpath('//div[@class="articleGroup"]/section/div[2]/h3/a/text()').extract()
        desc  = response.xpath('//div[@class="articleGroup"]/section/div[2]/p/text()').extract()
        pubt  = response.xpath('//div[@class="articleGroup"]/section/div[2]/time/text()').extract()
        pic  = response.xpath('//div[@class="articleGroup"]/section/div[1]/a/img/@src').extract()
        for i in range(0,len(links)):
            url = links[i]
            tit = title[i].replace(' ','')
            describe = desc[i]
            pubtime = pubt[i]
            try:
                pic_url = pic[i]
            except:
                pic_url = ''
            timeArray = time.strptime(pubtime, "%Y-%m-%d")
            publishedDate = time.mktime(timeArray)
            if publishedDate >= self.timeStamp:
                publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))

                yield scrapy.Request(url,meta={
                    'title':tit,
                    'describe':describe,
                    'pubtime':publishedDate,
                    'pic_url':pic_url,
                    'home_url':response.url
                },callback=self.parse_item,dont_filter=True)


    def parse_item(self,response):
        title = response.meta['title'].replace('\n','').replace('\r','').replace('\t','')
        publishedDate = response.meta['pubtime']
        home_url = response.meta['home_url']
        describe = response.meta['describe']
        pic_url = response.meta['pic_url']
        app_name =  u'天下杂志每日报'.encode('utf-8')
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content = response.xpath('//section[@id="emailshow"]').extract()
        contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', contentt)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        author = ''
        pic_more_url = re.findall('<img(.*?)src="(.*?)">',contentt)
        pic_more_url1 = []
        for i in range(0,len(pic_more_url)):
            pic_more_url.append(pic_more_url[i][1])
        pic_more_url = str(set(pic_more_url1))
        if '7' in home_url:
            category = u'产业'.encode('utf-8')
        elif '7' in home_url:
            category = u'国际'.encode('utf-8')
        elif '12' in home_url:
            category = u'环境'.encode('utf-8')
        else:
            category = u'服务'.encode('utf-8')

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
        self.count += 1
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
        item['count'] = self.count
        item['publishedDate'] = publishedDate
        item['crawlTime'] = crawlTime
        yield item