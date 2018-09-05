#coding=utf-8
import json
import scrapy
import time,re,time
from news.items import NewsItem


class ydzx(scrapy.Spider):
    name='ydzxnews'
    start_urls=[
        #娱乐
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c3&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517188240125',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c3&cstart=10&cend=20&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517188240128',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c3&cstart=20&cend=30&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517188240129',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c3&cstart=30&cend=40&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517188240130',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c3&cstart=40&cend=50&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517188240131',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c3&cstart=50&cend=60&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517188240132',
        #体育
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c9&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517193983454',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c9&cstart=10&cend=20&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517193983457',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c9&cstart=20&cend=30&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517193983458',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c9&cstart=30&cend=40&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517193983459',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c9&cstart=40&cend=50&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517193983459',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c9&cstart=50&cend=60&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517193983459',
        #军事
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c7&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194497427',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c7&cstart=10&cend=20&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194497430',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c7&cstart=20&cend=30&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194497431',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c7&cstart=30&cend=40&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194497432',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c7&cstart=40&cend=50&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194497433',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c7&cstart=50&cend=60&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194497434',
        #体育
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c2&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194604343',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c2&cstart=10&cend=20&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194604346',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c2&cstart=20&cend=30&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194604347',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c2&cstart=30&cend=40&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194604348',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c2&cstart=40&cend=50&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194604349',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c2&cstart=50&cend=60&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194604350',
        #财经
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c5&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194673075',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c5&cstart=10&cend=20&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194673078',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c5&cstart=20&cend=30&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194673079',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c5&cstart=30&cend=40&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194673080',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c5&cstart=40&cend=50&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194673081',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c5&cstart=50&cend=60&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194673082',
        #NBA
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=sc4&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194775137',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=sc4&cstart=10&cend=20&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194775140',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=sc4&cstart=20&cend=30&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194775141',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=sc4&cstart=30&cend=40&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194775142',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=sc4&cstart=40&cend=50&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194775143',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=sc4&cstart=50&cend=60&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194775144',
        #汽车
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c11&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194875329',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c11&cstart=10&cend=20&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194875332',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c11&cstart=20&cend=30&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194875333',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c11&cstart=30&cend=40&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194875334',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c11&cstart=40&cend=50&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194875335',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=c11&cstart=50&cend=60&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517194875336',
        #视频
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=u13746&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195187853',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=u13746&cstart=10&cend=20&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195187856',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=u13746&cstart=20&cend=30&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195187857',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=u13746&cstart=30&cend=40&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195187858',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=u13746&cstart=40&cend=50&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195187859',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=u13746&cstart=50&cend=60&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195187860',
        #热点
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=hot&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195303945',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=hot&cstart=10&cend=20&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195405518',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=hot&cstart=20&cend=30&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195405519',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=hot&cstart=30&cend=40&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195405520',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=hot&cstart=40&cend=50&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195405521',
        'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=hot&cstart=50&cend=60&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=1517195405522',
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        data=json.loads(response.body)
        data=data['result']
        for i in range(0,len(data)):
            title = data[i]['title']
            pubTime = data[i]['date']
            url = data[i]['docid']
            pic_url = data[i]['image_urls']
            describe = data[i]['summary']
            try:
                category = data[i]['category']
            except:
                category = '要闻'
            url = 'http://www.yidianzixun.com/article/'+url
            # print title
            # print pubTime
            # print url
            # print pic_url
            # print describe
            # print category
            yield scrapy.Request(url,meta={
                'title':title,
                'pubTime':pubTime,
                'pic_url':pic_url,
                'describe':describe,
                'category':category,
                'home_url':response.url
            },callback=self.parse_item,dont_filter=True)


    def parse_item(self,response):
        title = response.meta['title']
        publishedDate = response.meta['pubTime']
        pic_url = response.meta['pic_url']
        for i in range(0,len(pic_url)):
            if 'http' not in  pic_url[i]:
                pic_urlt=''
            else:
                pic_urlt=str(pic_url)
        describe = response.meta['describe']
        category = response.meta['category']
        home_url = response.meta['home_url']
        app_name='一点资讯_b'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        try:
            try:
                content = response.xpath('//div[@id="imedia-article"]').extract()
                contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                content = re.findall('>(.*?)<', contentt)
                contentdata = ''
                for i in content:
                    contentdata += i
                content = contentdata
            except:
                content = response.xpath('//div[@class="content-bd"]').extract()
                contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                content = re.findall('>(.*?)<', contentt)
                contentdata = ''
                for i in content:
                    contentdata += i
                content = contentdata

            pic_more_url = re.findall('<imgsrc="(.*?)"',contentt)
            pic_more_url1 =[]
            for i in range(0,len(pic_more_url)):
                if 'http' not in pic_more_url[i]:
                    pic_more_urlt = 'http:' + pic_more_url[i]
                    pic_more_url1.append(pic_more_urlt)
                else:
                    pic_more_url1.append(pic_more_url[i])

            pic_more_url = str(set(pic_more_url1))
        except:
            content = response.xpath('//div[@class="video-wrapper"]').extract()
            contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('<videosrc="(.*?)"',contentt)[0]
            pic_more_url =''
        try:
            author = response.xpath('//a[@class="doc-source"]/text()').extract()[0]
        except:
            author = ''
        print "app名称", app_name
        print "主图片url", pic_urlt
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
        item['pic_url'] = pic_urlt
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
            self.count +=1
            item['count']= self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item
