#coding=utf-8
import time,re,json
import scrapy
from news.items import NewsItem

class baidu(scrapy.Spider):
    name = 'baidu'
    Ttime = int(round(time.time()*1000))
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def start_requests(self):
        import requests
        url = 'https://news.baidu.com/sn/api/feed_feedlist?pd=newsplus&os=android&sv=7.1.2.0&from=app&_uid=g8SNu0um2ulx8HuKlu2ci0is2tl5aB8o_iSW8_uNSiiOO2tgga2qi_u62ig8uvihA&_ua=_aBDCgaH-i46ywoUfpw1z4aBsiz5aX8D4a2AiqqHB&_ut=5yG_YtM1vC_bhvhJgODpOYhuA&_from=1019026r&_cfrom=1019026r&_network=1_0&cen=uid_ua_ut'
        params = {
            "ln": "20",
            "os": "android",
            "display_time": "%s"%self.Ttime,
            "from": "app",
            "ver": "6",
            "withtoppic": "0",
            "network": {"wifi_aps": {"ap_mac": "70:05:14:7d:2a:5f", "is_connected": True, "ap_name": "", "rssi": -33},
                        "ipv4": "172.18.173.37", "cellular_id": "-1", "operator_type": 99, "connection_type": 100},
            "pd": "newsplus",
            "user_category": "",
            "cuid": "3ADAC23BAEBDC750FF38B3810FA334A1|918510050145753",
            "action": "0",
            "device": {"screen_size": {"height": 1184, "width": 768}, "model": "Nexus 4",
                       "udid": {"android_id": "6140f143b1a4dd1e", "mac": "70:05:14:7d:2a:5f",
                                "imei": "357541050015819"}, "vendor": "LGE", "device_type": 1,
                       "os_version": {"micro": 0, "minor": 4, "major": 4}, "os_type": 1},
            "sv": "7.1.2.0",
            "gps": '{"timestamp":1528790165,"longitude":"116.365275","coordinate_type":3,"latitude":"39.969771"}',
            "mid": "357541050015819_70:05:14:7d:2a:5f",
            "loc_ll": "116.365275,39.969771",
            "wf": "1",
        }
        data = requests.post(url, data=params)
        data = json.loads(data.content)
        data = data['data']['news']
        for i in range(len(data)):
            title = data[i]['title']
            url = data[i]['url']
            pubt = data[i]['pulltime']
            pubtt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(float(pubt) / 1000)))
            print pubtt
            try:
                desc = data[i]['abs']
            except:
                desc = ''
            if int(float(pubt) / 1000) >= self.timeStamp:
                pubt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(float(pubt) / 1000)))
                yield scrapy.Request(url, meta={
                    'title': title,
                    'pubt': pubt,
                    'desc': desc,
                    'category':'推荐'
                }, callback=self.parse_item)


    def parse_item(self, response):
        title = response.meta['title']
        publishedDate = response.meta['pubt']
        describe = response.meta['desc']
        app_name = '百度新闻'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url = 'https://news.baidu.com/'
        author = ''
        pic_url = ''
        category = response.meta['category']
        content = response.xpath('//p/text()').extract()
        contentt = ''
        for i in range(len(content)):
            contentt += content[i]
        content = contentt.replace('\t', '').replace('\n', '').replace('\r', '')
        pic_more_url = re.findall('<img src="(.*?)"', response.body)
        pic = []
        for i in range(len(pic_more_url)):
            pic.append(pic_more_url[i])
        pic_more_url = str(pic)
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
        self.count += 1
        item['count'] = self.count
        yield item



