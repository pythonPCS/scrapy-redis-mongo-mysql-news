#-*- coding: utf-8 -*-
from scrapy.spider import Spider
import scrapy
import sys
import json,time,re
from news.items import NewsItem
import random

reload(sys)
sys.setdefaultencoding('utf8')

class xinwen(Spider):
    name = 'tengxunxinwen'
    start_urls = [
        'https://r.inews.qq.com/getQQNewsUnreadList?rtAd=1&lc_ids=&forward=1&page=6&last_id=20180602A1IG9G00&newsTopPage=5&picType=0,1,2,0,0,2,2,1,2,0,0,2,0,1,0,0,2,2,0,2&user_chlid=news_news_19,news_news_bj,news_news_ent,news_news_sports,news_news_mil,news_news_nba,news_news_world&last_time=1528079861&channelPosition=0&chlid=news_news_top&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&omgid=9815f276f473194ffe286608f2d6b5ba263b001021181e&uid=5544c78435fe1eac&devid=867514021468675&appver=19_android_5.6.02&qn-rid=1208a091-bdbd-40b2-9ee9-90759cb7584e&qn-sig=fd43538cc388872084f05a293eadece1',
        'https://r.inews.qq.com/getQQNewsUnreadList?rtAd=1&lc_ids=&forward=1&page=7&last_id=20180602A1IG9G00&newsTopPage=5&picType=0,1,2,0,0,2,2,1,2,0,0,2,0,1,0,0,2,2,0,2&user_chlid=news_news_19,news_news_bj,news_news_ent,news_news_sports,news_news_mil,news_news_nba,news_news_world&last_time=1528079861&channelPosition=0&chlid=news_news_top&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&omgid=9815f276f473194ffe286608f2d6b5ba263b001021181e&uid=5544c78435fe1eac&devid=867514021468675&appver=19_android_5.6.02&qn-rid=1208a091-bdbd-40b2-9ee9-90759cb7584e&qn-sig=fd43538cc388872084f05a293eadece1',
        'https://r.inews.qq.com/getQQNewsUnreadList?rtAd=1&lc_ids=&forward=1&page=6&last_id=20180602A1IG9G00&newsTopPage=5&picType=0,1,2,0,0,2,2,1,2,0,0,2,0,1,0,0,2,2,0,2&user_chlid=news_news_19,news_news_bj,news_news_ent,news_news_sports,news_news_mil,news_news_nba,news_news_world&last_time=1528079861&channelPosition=0&chlid=news_news_19&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&omgid=9815f276f473194ffe286608f2d6b5ba263b001021181e&uid=5544c78435fe1eac&devid=867514021468675&appver=19_android_5.6.02&qn-rid=1208a091-bdbd-40b2-9ee9-90759cb7584e&qn-sig=fd43538cc388872084f05a293eadece1',
        'https://r.inews.qq.com/getQQNewsUnreadList?rtAd=1&lc_ids=&forward=1&page=7&last_id=20180602A1IG9G00&newsTopPage=5&picType=0,1,2,0,0,2,2,1,2,0,0,2,0,1,0,0,2,2,0,2&user_chlid=news_news_19,news_news_bj,news_news_ent,news_news_sports,news_news_mil,news_news_nba,news_news_world&last_time=1528079861&channelPosition=0&chlid=news_news_19&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&omgid=9815f276f473194ffe286608f2d6b5ba263b001021181e&uid=5544c78435fe1eac&devid=867514021468675&appver=19_android_5.6.02&qn-rid=1208a091-bdbd-40b2-9ee9-90759cb7584e&qn-sig=fd43538cc388872084f05a293eadece1',
        'https://r.inews.qq.com/getQQNewsUnreadList?rtAd=1&lc_ids=&forward=1&page=6&last_id=20180602A1IG9G00&newsTopPage=5&picType=0,1,2,0,0,2,2,1,2,0,0,2,0,1,0,0,2,2,0,2&user_chlid=news_news_19,news_news_bj,news_news_ent,news_news_sports,news_news_mil,news_news_nba,news_news_world&last_time=1528079861&channelPosition=0&chlid=news_news_world&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&omgid=9815f276f473194ffe286608f2d6b5ba263b001021181e&uid=5544c78435fe1eac&devid=867514021468675&appver=19_android_5.6.02&qn-rid=1208a091-bdbd-40b2-9ee9-90759cb7584e&qn-sig=fd43538cc388872084f05a293eadece1',
        'https://r.inews.qq.com/getQQNewsUnreadList?rtAd=1&lc_ids=&forward=1&page=7&last_id=20180602A1IG9G00&newsTopPage=5&picType=0,1,2,0,0,2,2,1,2,0,0,2,0,1,0,0,2,2,0,2&user_chlid=news_news_19,news_news_bj,news_news_ent,news_news_sports,news_news_mil,news_news_nba,news_news_world&last_time=1528079861&channelPosition=0&chlid=news_news_world&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&omgid=9815f276f473194ffe286608f2d6b5ba263b001021181e&uid=5544c78435fe1eac&devid=867514021468675&appver=19_android_5.6.02&qn-rid=1208a091-bdbd-40b2-9ee9-90759cb7584e&qn-sig=fd43538cc388872084f05a293eadece1',
        'https://r.inews.qq.com/getQQNewsUnreadList?rtAd=1&lc_ids=&forward=1&page=6&last_id=20180602A1IG9G00&newsTopPage=5&picType=0,1,2,0,0,2,2,1,2,0,0,2,0,1,0,0,2,2,0,2&user_chlid=news_news_19,news_news_bj,news_news_ent,news_news_sports,news_news_mil,news_news_nba,news_news_world&last_time=1528079861&channelPosition=0&chlid=news_news_mil&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&omgid=9815f276f473194ffe286608f2d6b5ba263b001021181e&uid=5544c78435fe1eac&devid=867514021468675&appver=19_android_5.6.02&qn-rid=1208a091-bdbd-40b2-9ee9-90759cb7584e&qn-sig=fd43538cc388872084f05a293eadece1',
        'https://r.inews.qq.com/getQQNewsUnreadList?rtAd=1&lc_ids=&forward=1&page=7&last_id=20180602A1IG9G00&newsTopPage=5&picType=0,1,2,0,0,2,2,1,2,0,0,2,0,1,0,0,2,2,0,2&user_chlid=news_news_19,news_news_bj,news_news_ent,news_news_sports,news_news_mil,news_news_nba,news_news_world&last_time=1528079861&channelPosition=0&chlid=news_news_mil&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&omgid=9815f276f473194ffe286608f2d6b5ba263b001021181e&uid=5544c78435fe1eac&devid=867514021468675&appver=19_android_5.6.02&qn-rid=1208a091-bdbd-40b2-9ee9-90759cb7584e&qn-sig=fd43538cc388872084f05a293eadece1',
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        data = json.loads(response.body)
        data = data['newslist']
        for i in range(len(data)):
            title = data[i]['title']
            desc = data[i]['abstract']
            pubt = data[i]['timestamp']
            url = data[i]['surl']
            yield scrapy.Request(url,meta={
                'title':title,
                'desc':desc,
                'pubt':pubt,
                'home_url':response.url
            },callback=self.parse_item)

    def parse_item(self,response):
        title = response.meta['title']
        describe = response.meta['desc']
        publishedDate = response.meta['pubt']
        pic_url = ''
        app_name = '腾讯新闻'
        author = ''
        home_url = response.meta['home_url']
        category = '要闻'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        content = re.findall('"cnt_html":"(.*?)"',str(response.body))
        content =content[0].decode('unicode_escape').replace('\t','').replace('\n','').replace('\r','').replace('<P>','').replace('<\/P>','')
        pic_more_url = ''
        publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
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