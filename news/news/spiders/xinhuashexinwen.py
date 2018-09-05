#-*- coding: utf-8 -*-
from scrapy.spider import Spider
import scrapy
from urlparse import urljoin
from scrapy.selector import Selector
from scrapy.http import Request
import time
import json
from selenium import webdriver
import re
import sys
# 全部爬取
from news.DataResource import TransportData
from news.items import NewsItem
import requests
import lxml.html as lh
reload(sys)
sys.setdefaultencoding('utf8')

class xhs(scrapy.Spider):
    name = 'xinhuashe'
    header = {
        "User-Agent": "android-16-720x1184-GALAXY NEXUS",
        "content-type": "application/json"
    }
    start_urls = [
        'https://zhongguowangshi.com/'
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    tt = str(int(round(time.time() * 1000)))

    def parse(self, response):
        listnum = ['470','470','470','23140','23140','23140','462','462','462','463','463','463','16534','16534','16534']   #470  要闻  23140学习  462 国际 463财经
        formdata = [
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "470","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4001","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 1,"clientLatitude": 31.247196038642187},#要闻
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "470","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4001","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 2,"clientLatitude": 31.247196038642187},#要闻
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "470","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4001","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 3,"clientLatitude": 31.247196038642187},#要闻
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "462","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 1,"clientLatitude": 31.247196038642187},#国际
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "462","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 2,"clientLatitude": 31.247196038642187},#国际
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "462","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 3,"clientLatitude": 31.247196038642187},#国际
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "463","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 1,"clientLatitude": 31.247196038642187},#财经
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "463","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 2,"clientLatitude": 31.247196038642187},#财经
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "463","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 3,"clientLatitude": 31.247196038642187},#财经
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "23140","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 1,"clientLatitude": 31.247196038642187},#学习
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "23140","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 2,"clientLatitude": 31.247196038642187},#学习
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "23140","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 3,"clientLatitude": 31.247196038642187},#学习
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "16534","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 1,"clientLatitude": 31.247196038642187},#推荐
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "16534","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 2,"clientLatitude": 31.247196038642187},#推荐
            {"userID": "0","clientLongitude": 121.49237750590044,"clientApp": "104","city": "null","clientHeight": 1280,"count": 0,"province": "null","excludeRecommend": 0,"clientDev": "0","columnid": "16534","clientModel": "SM-G9350","clientToken": "4062c95015dbaed2529aebd399ca0d77","clientDate": self.tt,"clientOS": "5.1.1","clientVer": "4.0.6","clientMarket": "198","clientType": 2,"clientPrison": "0","clientBundleID": "net.xinhuamm.mainclient","clientNet": "wifi","columntype": "4002","clientId": "4062c95015dbaed2529aebd399ca0d77","clientLable": "867637959598351","clientWidth": 720,"pn": 3,"clientLatitude": 31.247196038642187},#推荐
            ]
        for i in range(0,len(formdata)):
            header = {
                "User-Agent": "android-16-720x1184-GALAXY NEXUS",
                "content-type": "application/json"
            }
            if listnum[i] =='470':
                category = '要闻'.encode('utf-8')
            elif listnum[i] =='462':
                category = '国际'.encode('utf-8')
            elif listnum[i] == '463':
                category = '财经'.encode('utf-8')
            elif listnum[i] == '16534':
                category = '推荐'.encode('utf-8')
            else:
                category = '学习'.encode('utf-8')
            url = 'https://xhpfmapi.zhongguowangshi.com/v400/core/indexlist'
            data = requests.post(url,data=json.dumps(formdata[i]), headers=self.header)
            data = json.loads(data.content)
            data = data['data']['data']
            for i in data:
                id = i['id']
                title = i['topic']
                print title
                url = 'https://xhpfmapi.zhongguowangshi.com/v500/news/%s.js?ts=0'%id
                try:
                    publishedDate = i['releasedate']
                    if ':' in publishedDate:
                        publishedDate = str(self.time_str) + ' ' + publishedDate
                    else:
                        publishedDate = '20' + publishedDate
                except:
                    publishedDate = ''
                try:
                    pic_url = i['shareImage']
                except:
                    pic_url = ''
                try:
                    pic_more_url = i['detailImg']
                except:
                    pic_more_url = ''
                yield scrapy.Request(url, meta={
                    'category': category,
                    'title': title,
                    'publishedDate': publishedDate,
                    'pic_url': pic_url,
                    'pic_more_url': pic_more_url,
                    'home_url': response.url
                }, callback=self.parse_item, dont_filter=True)


    def parse_item(self,response):
        title = response.meta['title']
        pic_url = response.meta['pic_url']
        pic_more_url = response.meta['pic_more_url']
        publishedDate = response.meta['publishedDate']
        category = response.meta['category']
        describe = ''
        data = response.body.replace('var XinhuammNews =','')
        data = json.loads(data)
        content = data['content']
        publishedDate = data['releasedate']
        contentt = content.replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', contentt)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        home_url = response.meta['home_url']
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        app_name = '新华社'
        author = ''
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
        item['count'] = self.count
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
        try:
            try:
                publishedDate_stamp = int(time.mktime(time.strptime(publishedDate, "%Y-%m-%d %H:%M")))
            except:
                publishedDate_stamp = int(time.mktime(time.strptime(publishedDate, "%Y-%m-%d")))
        except:
            publishedDate_stamp = int(time.mktime(time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")))
        if publishedDate_stamp > self.timeStamp:
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate_stamp)))
            self.count += 1
            item['publishedDate'] = publishedDate
            yield item
