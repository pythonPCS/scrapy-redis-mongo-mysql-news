#-*- coding: utf-8 -*-
from scrapy.spider import Spider
import scrapy
import sys
import json,time,re
from news.items import NewsItem
reload(sys)
sys.setdefaultencoding('utf8')

class renminribao(scrapy.Spider):
    name = 'renmin'
    page = 1
    start_urls = [
        'http://app.peopleapp.com/Api/600/HomeApi/searchHotWord?city=北京市&citycode=010&count=20&device=670997f3-a0ee-374d-9271-fa02707b8b0d&device_model=Nexus 4&device_os=Android 4.4&device_product=LGE&device_size=768*1184&device_type=1&district=海淀区&fake_id=8533258&interface_code=621&keyword=习近平&latitude=39.96389&longitude=116.358495&page=%s&province=北京市&province_code=1528163652000&userId=0&version=6.2.1&securitykey=b5e1fd6b496267493431cdb9a0d3100c'%page
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-08', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        data = json.loads(response.body)
        data = data['data']
        num = 0
        for i in range(len(data)):
            title = data[i]['title']
            pic_url = data[i]['share_image']
            published = data[i]['news_time']
            url = data[i]['share_url']
            print published
            timeArray = time.strptime(published, "%Y-%m-%d %H-%M-%S")
            timeStamp = int(time.mktime(timeArray))
            if timeStamp >= self.timeStamp:
                num += 1
                yield scrapy.Request(url,meta={
                    'title':title,
                    'pic_url':pic_url,
                    'published':published,
                    'home_url':response.url
                }, callback=self.parse_item)
        if num >= 0:
            self.page += 1
            t = self.md5(self.page)
            url =  'http://app.peopleapp.com/Api/600/HomeApi/searchHotWord?city=北京市&citycode=010&count=20&device=670997f3-a0ee-374d-9271-fa02707b8b0d&device_model=Nexus 4&device_os=Android 4.4&device_product=LGE&device_size=768*1184&device_type=1&district=海淀区&fake_id=8533258&interface_code=621&keyword=习近平&latitude=39.96389&longitude=116.358495&page=%s&province=北京市&province_code=1528163652000&userId=0&version=6.2.1&securitykey=%s'%(self.page,t)
            yield scrapy.Request(url,callback=self.parse)


    def parse_item(self,response):
        title = response.meta['title']
        pic_url = response.meta['pic_url']
        publishedDate = response.meta['published']
        p = publishedDate.split(' ')
        p1 = p[0]
        p2 = p[1]
        p2 =p2.replace('-',':')
        publishedDate = p1 + ' ' + p2
        home_url = response.meta['home_url']
        app_name = '人民日报'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        author = ''
        category = '首页新闻'
        describe = ''
        try:
            content = response.xpath('//div[@class="article long-article"]').extract()
            content = content[0].replace('\t', '').replace('\n', '').replace('\r', '')
            content = re.findall('>(.*?)<',content)
            contentt = ''
            for i in range(len(content)):
                contentt += content[i]
            content = contentt
        except:
            content = ''
        pic_more_url = ''
        print response.body
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
        self.count += 1
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
        item['count'] = self.count
        yield item

    def md5(self,page):
        import hashlib
        t = '北京市|010|20|670997f3-a0ee-374d-9271-fa02707b8b0d|Nexus 4|Android 4.4|LGE|768*1184|1|海淀区|8533258|621|习近平|39.96389|116.358495|' + str(page) + '|北京市|1528163652000|0|6.2.1rmrbsecurity$#%sut49fbb427a508bcc'
        m = hashlib.md5()
        m.update(t)
        return m.hexdigest()





