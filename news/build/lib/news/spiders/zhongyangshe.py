#coding=utf-8
import time,re,json
import scrapy
from news.items import NewsItem

class baidu(scrapy.Spider):
    name = 'zhongyangshe'
    start_urls = [
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/firstnews.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/Index_TopNews.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/aipl.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/aopl.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/acn.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/afe.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/video.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/NewsTopic.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/ait.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/ahel.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/asoc.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/aloc.json',
        'http://appweb.cna.com.tw/JsonData/CnaApp_2016mobile/acul.json',
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        data = response.body.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
        print data
        # data = json.loads(response.body.replace('\t','').replace('\n','').replace('\r','').replace(' ',''))
        # data = data['NewsItems']
        # for i in range(len(data)):
        #     category = data[i]['ClassName']
        #     url = data[i]['PageUrl']
        #     title = data[i]['HeadLine']
        #     pubt = data[i]['CreateTime']
        #     try:
        #         pic = data[i]['Source']
        #     except:
        #         pic = ''
        #     yield scrapy.Request(url,meta={
        #         'title':title,
        #         'pic':pic,
        #         'category':category,
        #         'pubt':pubt
        #     },callback=self.parse_one)
        category = re.findall('"ClassName":"(.*?)",',data)
        url = re.findall('"PageUrl":"(.*?)",',data)
        title = re.findall('"HeadLine":"(.*?)",',data)
        pic = re.findall('"Source":"(.*?)",',data)
        for i in range(len(url)):
            cate = category[i]
            tit = title[i]
            links = url[i]
            picc = pic[i]
            yield scrapy.Request(links, meta={
                'title':tit,
                'pic':picc,
                'category':cate
            }, callback=self.parse_one, dont_filter=True)

    def parse_one(self,response):
        title = response.meta['title']
        category = response.meta['category']
        pic_url = response.meta['pic']
        app_name = '中央社'
        describe = ''
        home_url = 'http://appweb.cna.com.tw/'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        author = ''
        try:
            content = response.xpath('//p/text()').extract()
            contentt = ''
            for i in range(len(content)):
                contentt += content[i]
            content = contentt
        except:
            content = ''
        try:
            pic_more_url = response.xpath('//div[@class="newsPhoto"]/a/img/@src').extract()[0]
        except:
            pic_more_url = ''
        pubt = response.xpath('//div[@class="newsTime"]').extract()
        pubt = pubt[0].replace('\t','').replace('\n','').replace('\r','')
        pubt = re.findall('>(.*?)<',pubt)
        publishedDate = ''
        for i in range(len(pubt)):
            publishedDate += pubt[i]
        publishedDate = publishedDate.split('更新')[0]
        publishedDate = publishedDate.replace('發稿：','').replace('/','-')
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
