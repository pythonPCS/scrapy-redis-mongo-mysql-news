#coding=utf-8
from news.items import NewsItem
import scrapy
import time,re,json

class dw(scrapy.Spider):
    name = 'deguozhisheng'
    start_urls = [
        'http://www.dw.com/zh/%E5%9C%A8%E7%BA%BF%E6%8A%A5%E5%AF%BC/%E6%97%B6%E6%94%BF%E9%A3%8E%E4%BA%91/s-1681?&zhongwen=simp',#时政风云
        'http://www.dw.com/zh/%E5%9C%A8%E7%BA%BF%E6%8A%A5%E5%AF%BC/%E7%BB%8F%E6%B5%8E%E7%BA%B5%E6%A8%AA/s-1682?&zhongwen=simp',#经济纵横
        'http://www.dw.com/zh/%E5%9C%A8%E7%BA%BF%E6%8A%A5%E5%AF%BC/%E6%96%87%E5%8C%96%E7%BB%8F%E7%BA%AC/s-1683?&zhongwen=simp',#文化经纬
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        links = response.xpath('//div[@id="bodyContent"]/div[1]/div/div/div/a/@href').extract()
        title = response.xpath('////div[@id="bodyContent"]/div[1]/div/div/div/a/h2/text()').extract()
        # pic = response.xpath('////div[@id="bodyContent"]/div[1]/div/div/div/a/div[1]/img/@src').extract()
        # desc = response.xpath('//div[@id="bodyContent"]/div[1]/div/div/div/a/p/text()').extract()
        for i in range(len(links)):
            url = 'http://www.dw.com' + links[i]
            tit = title[i].replace('\t', '').replace('\n', '').replace('\r', '')
            yield scrapy.Request(url, meta={
                'title': tit,
                'home_url': response.url
            }, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        title = response.meta['title']
        home_url = response.meta['home_url']
        pic_url = ''
        describe = ''
        app_name = '德国之声'
        pubt = response.xpath('//div[@class="group"]/ul/li[1]').extract()[0]
        publishedDate = pubt.replace('\t', '').replace('\n', '').replace('\r', '').replace('<strong>日期</strong>', '').replace('<li>', '').replace('</li>', '')
        t = publishedDate.split('.')
        t1 = t[0]
        t2 = t[1]
        t3 = t[2]
        publishedDate = t3 + '-' + t2 + '-' + t1 + ' 00:00:00'
        try:
            author = response.xpath('//div[@class="group"]/ul/li[2]').extract()[0]
            author = author.replace('\t', '').replace('\n', '').replace('\r', '').replace('<strong>作者</strong>', '').replace('<li>', '').replace('</li>', '')
        except:
            author = ''
        author = ''
        content = response.xpath('//div[@class="col3"]/div[@class="group"]').extract()
        content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', content)
        contentdata = ''
        for i in range(0, len(content)):
            contentdata += content[i]
        content = contentdata
        pic_more_url = ''
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if 's-1681' in home_url:
            category = '时政风云'
        elif 's-1682' in home_url:
            category = '经济纵横'
        else:
            category = '文化经纬'
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





