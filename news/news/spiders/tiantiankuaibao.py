#coding=utf-8
import json
import requests
#coding=utf-8
import scrapy
import time
import json
import re
from news.items import NewsItem
from news.DataResource import TransportData

class tiantian(scrapy.Spider):
    name = 'tiantiankuaibao'
    Ttime = int(round(time.time() * 1000))
    start_urls = [
        'https://r.cnews.qq.com'
    ]
    count = 0
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        url = 'https://r.cnews.qq.com/searchByType?devid=864699038349266'
        params = {
            "REQBuildTime":"%s"%self.Ttime,
            "adcode":"110108",
            "ssid":"tmliu",
            "source":"",
            "omgid":"ecdaba5753005f4be4f95cac85563d10f7e80010213113",
            "REQExecTime":"%s"%self.Ttime,
            "qqnetwork":"wifi",
            "commonsid":"c3dd54a003fb4bb89d4b8bdf80f23fda",
            "curTab":"kuaibao",
            "kingCardType":"0",
            "picSizeMode":"0",
            "commonGray":"1_3%7C2_1%7C12_1%7C16_1%7C22_0%7C14_0%7C17_0%7C19_1",
            "currentTab":"kuaibao",
            "is_wap":"0",
            "lastCheckCardType":"0",
            "omgbizid":"afa8d326e9dc2b441dfb950abf1d92b714870080213504",
            "page":"1",
            "type":"aggregate",
            "imsi":"460078108159178",
            "bssid":"24%3A05%3A0f%3A8a%3Abd%3Af3",
            "query":"习近平",
            "muid":"211471387078276596",
            "curChannel":"daily_timeline",
            "activefrom":"icon",
            "unixtimesign":"1528248088989",
            "qimei":"864699038349266",
            "Cookie":"%26lskey%3D%26luin%3D%26skey%3D%26uin%3D%26logintype%3D0",
            "chlid":"",
            "rawQuery":"",
            "imsi_history":"460078108159178",
            "qn-sig":"c744f26a575fe7a08f7c0c32c3a43d34",
            "qn-rid":"19649191-e9b9-4d33-9a4d-4923bbb1ffb1",
            "hw_fp":"xiaomi%2Ftiffany%2Ftiffany%3A7.1.2%2FN2G47H%2F8.3.15%3Auser%2Frelease-keys",
            "mid":"08bd609c01ab23254e488078e3c8d396d9a0737e",
            "devid":"864699038349266",
            "mac":"F4%3AF5%3ADB%3A23%3A21%3A26",
            "store":"73387",
            "screen_height":"1920",
            "apptype":"android",
            "origin_imei":"864699038349266",
            "hw":"Xiaomi_MI5X",
            "appversion":"4.8.10",
            "appver":"25_areading_4.8.10",
            "uid":"c955f03805f6ce81",
            "screen_width":"1080",
            "sceneid":"",
            "android_id":"c955f03805f6ce81"
        }
        headers = {
            "Content-Type":"application/x-www-form-urlencoded"
        }
        data = requests.post(url,data=params,headers=headers)
        data = json.loads(data.content)
        data = data['new_list']['data']
        for i in range(len(data)):
            title = data[i]['article']['title']
            url = data[i]['article']['short_url']
            pubt = data[i]['article']['time']
            desc = data[i]['article']['abstract']
            yield scrapy.Request(url,meta={
                'title':title,
                'pubt':pubt,
                'desc':desc
            },callback=self.parse_item,dont_filter=True)

    def parse_item(self,response):
        title = response.meta['title']
        publishedDate = response.meta['pubt']
        describe = response.meta['desc']
        app_name = '天天快报'
        pic_url = ''
        author = ''
        home_url = 'https://r.cnews.qq.com'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content = response.xpath('//div[@class="content-box"]/p/text()').extract()
        con = ''
        for i in range(len(content)):
            con += content[i]
        content = con
        category = '要闻'
        pic_more_url = response.xpath('//div[@class="content-box"]/p/img/@src').extract()
        picc = []
        for i in range(len(pic_more_url)):
            picc.append(pic_more_url[i])
        pic_more_url = picc

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
        item['pic_url'] = str(pic_url)
        item['pic_more_url'] = str(pic_more_url)
        item['author'] = author
        item['url'] = url
        item['category'] = category
        item['title'] = title
        item['describe'] = describe
        item['content'] = content
        item['home_url'] = home_url
        item['publishedDate'] = publishedDate
        item['crawlTime'] = crawlTime
        self.count += 1
        item['count'] = self.count
        yield item
