#coding=utf-8
import scrapy
import time
import json
import re
from news.items import NewsItem
from news.DataResource import TransportData
class nanfangzhoumo(scrapy.Spider):
    name = 'nanfangzhoumo'
    start_urls = [
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=0&cat_id%5B%5D=5282&hash=1be58c23b2598f9e7448f1312da25073',#推荐
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=1&cat_id%5B%5D=5282&hash=1be58c23b2598f9e7448f1312da25073',#推荐
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=2&cat_id%5B%5D=5282&hash=1be58c23b2598f9e7448f1312da25073',#推荐
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=3&cat_id%5B%5D=5282&hash=1be58c23b2598f9e7448f1312da25073',#推荐
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=0&cat_id%5B%5D=5269&hash=1be58c23b2598f9e7448f1312da25073',#时局
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=1&cat_id%5B%5D=5269&hash=1be58c23b2598f9e7448f1312da25073',#时局
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=2&cat_id%5B%5D=5269&hash=1be58c23b2598f9e7448f1312da25073',#时局
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=3&cat_id%5B%5D=5269&hash=1be58c23b2598f9e7448f1312da25073',#时局
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=0&cat_id%5B%5D=5274&hash=1be58c23b2598f9e7448f1312da25073',#经济
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=1&cat_id%5B%5D=5274&hash=1be58c23b2598f9e7448f1312da25073',#经济
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=2&cat_id%5B%5D=5274&hash=1be58c23b2598f9e7448f1312da25073',#经济
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=3&cat_id%5B%5D=5274&hash=1be58c23b2598f9e7448f1312da25073',#经济
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=0&cat_id%5B%5D=5271&hash=1be58c23b2598f9e7448f1312da25073',#防务
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=1&cat_id%5B%5D=5271&hash=1be58c23b2598f9e7448f1312da25073',#防务
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=2&cat_id%5B%5D=5271&hash=1be58c23b2598f9e7448f1312da25073',#防务
        'http://www.infzm.com/mobile/get_list_by_cat_ids?count=10&platform=android&version=5.4.2&start=3&cat_id%5B%5D=5271&hash=1be58c23b2598f9e7448f1312da25073',#防务
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        title = response.xpath('//item/@subject').extract()
        published = response.xpath('//item/@publish_time').extract()
        url = response.xpath('//snsShare/@url').extract()
        describe = response.xpath('//introtext').extract()
        category = response.xpath('//item/@source').extract()
        for i in range(0,len(url)):
            tit = title[i]
            pub = published[i]
            urlt = url[i]
            try:
                if category[i] ==u'Hi，南周'.encode('utf-8') :
                    category =u'推荐'.encode('utf-8')
                    cate = category
                elif category[i] ==u'作品上架'.encode('utf-8'):
                    category = u'推荐'.encode('utf-8')
                    cate = category
                else:
                    cate = category[i]
            except:
                cate = u'推荐'.encode('utf-8')
            desc = describe[i].replace('</introtext>','').replace('<introtext>','')
            yield scrapy.Request(urlt,meta={
                'title':tit,
                'publish':pub,
                'describe':desc,
                'category':cate,
                'home_url':response.url
            },callback=self.parse_item)

    def parse_item(self,response):
        title = response.meta['title']
        describe =response.meta['describe']
        home_url = response.meta['home_url']
        app_name = '南方周末'
        pic_url = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        category = response.meta['category']
        publishedDate = response.xpath('//em[@class="pubTime"]').extract()
        publishedDate = publishedDate[0].replace('\t','').replace('\n','').replace('\r','').replace('<em class="pubTime">','').replace('</em>','').replace(u'最后更新：','')
        publishedDate = publishedDate.replace('                    ','').replace('                ','')
        content = response.xpath('//section[@id="articleContent"]').extract()
        contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', contentt)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        author = ''
        pic_more_url = re.findall('<img(.*?)src="(.*?)"', contentt)
        pic_more_url1 = []
        for i in range(0, len(pic_more_url)):
            if 'http' not in pic_more_url[i][1]:
                pic_more_urlt = 'http:' + pic_more_url[i][1]
                pic_more_url1.append(pic_more_urlt)
            else:
                pic_more_url1.append(pic_more_url[i][1])
        pic_more_url = str(set(pic_more_url1))
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
        item['count'] = self.count
        item['publishedDate'] = publishedDate
        item['crawlTime'] = crawlTime
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
        timenum = int(time.mktime(timeArray))
        # existing_title = TransportData.getData('app_nanfangzhoumo', title)
        # # 符合要求，可以入库的title list
        # if existing_title:
        #     return
        # else:
        if timenum >= self.timeStamp:
            self.count += 1
            item['count'] = self.count
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timenum)))
            item['publishedDate'] = publishedDate
            yield item
