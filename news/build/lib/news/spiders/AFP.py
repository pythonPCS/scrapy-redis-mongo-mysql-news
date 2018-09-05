#coding=utf-8
import scrapy
import json, re, time
from news.items import NewsItem
import datetime

class AFP(scrapy.Spider):
    name = 'afpnews'
    start_urls = [
        'http://www.afpbb.com/sdata/detail_afp_json_v1_phone_4c43ffbac73aaf2877096fcf3df445a5.json'
    ]

    def parse(self, response):
        data = json.loads(response.body)
        data = data['news']
        for i in range(len(data)):
            title = data[i]['title']
            url = data[i]['link']
            pubt = data[i]['pubDate']
            pubt = pubt.split(', ')[1].replace('+0900','')
            t = pubt.split(' ')
            t1 = t[0]
            t2 = t[1]
            t3 = t[2]
            t4 = t[3]
            t12 = t2
            if 'June' in t12:
                tt = '06'
            elif 'Jun' in t12:
                tt = '06'
            elif 'January' in t12:
                tt = '01'
            elif 'Jan' in t12:
                tt = '01'
            elif 'February' in t12:
                tt = '02'
            elif 'Feb' in t12:
                tt = '02'
            elif 'March' in t12:
                tt = '03'
            elif 'Mar' in t12:
                tt = '03'
            elif 'April' in t12:
                tt = '04'
            elif 'Apr' in t12:
                tt = '04'
            elif 'May' in t12:
                tt = '05'
            elif 'July' in t12:
                tt = '07'
            elif 'August' in t12:
                tt = '08'
            elif 'Aug' in t12:
                tt = '08'
            elif 'September' in t12:
                tt = '09'
            elif 'Sept' in t12:
                tt = '09'
            elif 'October' in t12:
                tt = '10'
            elif 'Oct' in t12:
                tt = '10'
            elif 'November' in t12:
                tt = '11'
            elif 'Nov' in t12:
                tt = '11'
            elif 'December' in t12:
                tt = '12'
            elif 'Dec' in t12:
                tt = '12'
            pubt = t3 + '-' + tt + '-' + t1 + ' ' + t4
            try:
                desc = data[i]['description']
            except:
                desc = ''
            try:
                pic_url = data[i]['image']
            except:
                pic_url = ''
            yield scrapy.Request(url, meta={
                'title': title,
                'pic_url': pic_url,
                'describe': desc,
                'pubt': pubt
            }, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        title = response.meta['title']
        pic_url = response.meta['pic_url']
        describe = response.meta['describe']
        publishedDate = response.meta['pubt']
        app_name = 'AFP news'
        author = ''
        home_url = 'http://www.afpbb.com'
        category = 'News'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_more_url = ''
        content = response.xpath('//div[@class="article-body clear"]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in content:
            contentdata += i
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