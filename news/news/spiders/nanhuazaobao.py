#coding=utf-8
import scrapy
import re, time, json
from news.items import NewsItem

class nanhuazaobao(scrapy.Spider):
    name = 'nanhuazaobao'
    start_urls = [
        'https://data.scmp.com/api/rest/app/v2/page.json?type=home&id=int&option[image_styles]=750x470%2C250x250%2Csquare%2C750x470_lq%2C250x250_lq%2Csquare_lq&hash=75320813329b2599df4bf9d7f6b9e9a833fe2a77a0e09faa4540eb6fa8e7aa07',
        # 'https://data.scmp.com/api/rest/app/v2/page.json?type=home&id=latest&option[image_styles]=750x470%2C250x250%2Csquare%2C750x470_lq%2C250x250_lq%2Csquare_lq&hash=170e31731993ddef96df8a0ea32e4e2d30c156f52f70e00d4bd9f123e623366a',
        # 'https://data.scmp.com/api/rest/app/v2/page.json?type=trending&id=pageviews&option[since]=-1days&option[sections]=&option[image_styles]=750x470%2C250x250%2Csquare%2C750x470_lq%2C250x250_lq%2Csquare_lq&hash=e1b89e6866bf51306d8a98eae705a82d6bdd73e9696533e3b3613f12184adcd8',
        # 'https://data.scmp.com/api/rest/app/v2/page.json?type=section&id=2&option[image_styles]=750x470%2C250x250%2Csquare%2C750x470_lq%2C250x250_lq%2Csquare_lq&hash=b9a2dc7417c0014596505716570d97cf3609de837e0754a3b017e61b30a3a915',
        # 'https://data.scmp.com/api/rest/app/v2/page.json?type=section&id=4&option[image_styles]=750x470%2C250x250%2Csquare%2C750x470_lq%2C250x250_lq%2Csquare_lq&hash=bc3e96e76bcf5c6fc18dbe2726c76ab90965ce5f81bdf78db58480004e5d60b4'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        links = re.findall('"url":"(.*?)",',response.body)
        for i in range(len(links)):
            url = links[i]
            yield scrapy.Request(url,meta={
                'home_url': response.url
            }, callback=self.parse_item)

    def parse_item(self, response):
        try:
            title = response.xpath('//h1/text()').extract()[0]
            app_name = '南华早报'
            describe = ''
            author = ''
            pic_url = ''
            crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            home_url = response.meta['home_url']
            publishedDate = response.xpath('//div[@class="node-updated"]/span/text()').extract()[0]
            publishedDate = publishedDate.replace('UPDATED : ', '').replace('Monday, ', '')
            publishedDate = publishedDate.replace('Sunday, ', '').replace('Tuesday, ', '')
            publishedDate = publishedDate.replace('Wednesday, ', '').replace('Thursday, ', '')
            publishedDate = publishedDate.replace('Friday, ', '').replace('Saturday, ', '')
            t = publishedDate.split(',')
            t1 = t[0]
            t11 = t1.split(' ')[0]
            t12 = t1.split(' ')[1]
            if 'June' in t12:
                tt = '6'
            elif 'January' in t12:
                tt = '1'
            elif 'Jan' in t12:
                tt = '1'
            elif 'February' in t12:
                tt = '2'
            elif 'Feb' in t12:
                tt = '2'
            elif 'March' in t12:
                tt = '3'
            elif 'Mar' in t12:
                tt = '3'
            elif 'April' in t12:
                tt = '4'
            elif 'Apr' in t12:
                tt = '4'
            elif 'May' in t12:
                tt = '5'
            elif 'July' in t12:
                tt = '7'
            elif 'August' in t12:
                tt = '8'
            elif 'Aug' in t12:
                tt = '8'
            elif 'September' in t12:
                tt = '9'
            elif 'Sept' in t12:
                tt = '9'
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
            t2 = t[1].replace(' ', '')
            t3 = t[2].replace(' ', '')
            if 'am' in t3:
                t3 = t3.replace('am', '') + ':00'
            elif 'pm' in t3:
                t3 = t3.replace('pm', '')
                t3 = t3.split(':')
                t31 = t3[0]
                t31 = str(int(t31) + 12)
                t32 = t3[1]
                t3 = t31 + ':' + t32 + ':00'
            publishedDate = t2 + '-' + str(tt) + '-' + t11 + ' ' + t3
            content = response.xpath('//div[@class="pane-content"]').extract()
            content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            content = re.findall('>(.*?)<', content)
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
            pic_more_url = ''
            if 'id=int' in home_url:
                category = 'TOP STORIES'
            elif 'id=latest' in home_url:
                category = 'Live'
            elif 'id=pageviews' in home_url:
                category = 'Trending'
            elif 'id=2' in home_url:
                category = 'HongKong'
            elif 'id=4' in home_url:
                category = 'China'
            else:
                category = 'China'
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
                yield item
        except:
            pass