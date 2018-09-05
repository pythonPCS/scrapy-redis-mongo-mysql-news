#coding=utf-8
import scrapy
import time
import json,re
from news.items import NewsItem

class yidianzixun(scrapy.Spider):
    name = 'yidianzixun'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    Ttime = int(round(time.time() * 1000))
    time1 = time.strftime("%Y-%m-%d %H:%M:%S")
    time2 = time.strptime(time1, "%Y-%m-%d %H:%M:%S")
    time3 = int(time.mktime(time2))

    def start_requests(self):
        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            "Host": "www.yidianzixun.com",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://www.yidianzixun.com/"
        }
        # cookies ={
        #     "__guid": "147975473.3220507777170205000.1522825147643.9363",
        #     "JSESSIONID": "6a5877478c64c1897d198643d5242c4d09ad1ad0060bf25f664e1196e0094558",
        #     "wuid": "152259561985043",
        #     "wuid_createAt": "%s"%self.time1,
        #     "weather_auth": "2",
        #     "Hm_lvt_15fafbae2b9b11d280c79eff3b840e45": "%s"%self.time3,
        #     "Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45": "%s"%self.time3,
        #     "CNZZDATA1255169715": "1404781070-1528763939-http%253A%252F%252Fwww.so.com%252F%7C1528763939",
        #     "cn_1255169715_dplus": "%7B%22distinct_id%22%3A%20%22163f1ba7075a0-0206ae93d5cb3-5d4e211f-100200-163f1ba7076850%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201528769010%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201528769010%7D%7D",
        #     "UM_distinctid": "163f1ba7075a0-0206ae93d5cb3-5d4e211f-100200-163f1ba7076850",
        #     "monitor_count": "2",
        #     "captcha": "s%3Ab7f2a366cba5cab9fb4f1fd4d18a9f21.yjcDBE7X4llvMo8rnLo5OAvkOE3DWjm6OldniVRU2Ts",
        #     "sptoken": "Uhoy~U%3B%3AU8%3AU48261efeced332cc9f20413132c69381cad5f53f4bfc428ed84627675ba90e48"
        #     }
        cookies = [
            {
            "__guid": "147975473.3220507777170205000.1522825147643.9363",
            "JSESSIONID": "6a5877478c64c1897d198643d5242c4d09ad1ad0060bf25f664e1196e0094558",
            "wuid": "152259561985043",
            "wuid_createAt": "%s"%self.time1,
            "weather_auth": "2",
            "captcha": "s%3A65772dc0d08723dd86b4c515d69b3fac.HHd0I2DHiMQ0tmk64BursHkHNS5%2FAwvZno27bwff2NE",
            "Hm_lvt_15fafbae2b9b11d280c79eff3b840e45": "%s"%self.time3,
            "Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45": "%s"%self.time3,
            "CNZZDATA1255169715": "1404781070-1528763939-http%253A%252F%252Fwww.so.com%252F%7C1528763939",
            "cn_1255169715_dplus": "%7B%22distinct_id%22%3A%20%22163f1ba7075a0-0206ae93d5cb3-5d4e211f-100200-163f1ba7076850%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201528769010%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201528769010%7D%7D",
            "UM_distinctid": "163f1ba7075a0-0206ae93d5cb3-5d4e211f-100200-163f1ba7076850",
            "monitor_count": "2",
            "sptoken": "Uhoy~U%3AU%3B%3AU48261efeced332cc9f20413132c69381cad5f53f4bfc428ed84627675ba90e48"
        },
            {
            "__guid": "147975473.3220507777170205000.1522825147643.9363",
            "JSESSIONID": "6a5877478c64c1897d198643d5242c4d09ad1ad0060bf25f664e1196e0094558",
            "wuid": "152259561985043",
            "wuid_createAt": "%s"%self.time1,
            "weather_auth": "2",
            "captcha": "s%3A98b6fc3c076533eaa1dac72062fb09ce.MbsdYjMxJgyHzlJwv9n1Lz2bpnNVxDkjXpw19PRTgTc",
            "Hm_lvt_15fafbae2b9b11d280c79eff3b840e45": "1528768916,1528769011,1528772021,1528772151",
            "Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45": "%s"%self.time3,
            "CNZZDATA1255169715": "1404781070-1528763939-http%253A%252F%252Fwww.so.com%252F%7C1528766868",
            "cn_1255169715_dplus": "%7B%22distinct_id%22%3A%20%22163f1ba7075a0-0206ae93d5cb3-5d4e211f-100200-163f1ba7076850%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201528772204%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201528772204%7D%7D",
            "UM_distinctid": "163f1ba7075a0-0206ae93d5cb3-5d4e211f-100200-163f1ba7076850",
            "monitor_count": "6",
            "sptoken": "U8%3B9223%3E%3B%3E2%3FU%3AU%3B%3AU48261efeced332cc9f20413132c69381cad5f53f4bfc428ed84627675ba90e48"
        },
            {
                "__guid": "147975473.3220507777170205000.1522825147643.9363",
                "JSESSIONID": "6a5877478c64c1897d198643d5242c4d09ad1ad0060bf25f664e1196e0094558",
                "wuid": "152259561985043",
                "wuid_createAt": "%s"%self.time1,
                "weather_auth": "2",
                "captcha": "s%3A59db0a30fa30fdd09d4238aae224e068.t9Ar9fI0XSGYSe7VBAKsaBF7M6RBftHTnkAv3hq0fng",
                "Hm_lvt_15fafbae2b9b11d280c79eff3b840e45": "1528768916,1528769011,1528772021,1528772151",
                "Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45": "%s"%self.time3,
                "CNZZDATA1255169715": "1404781070-1528763939-http%253A%252F%252Fwww.so.com%252F%7C1528772293",
                "cn_1255169715_dplus": "%7B%22distinct_id%22%3A%20%22163f1ba7075a0-0206ae93d5cb3-5d4e211f-100200-163f1ba7076850%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201528772601%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201528772601%7D%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201528772720%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201528772720%7D",
                "UM_distinctid": "163f1ba7075a0-0206ae93d5cb3-5d4e211f-100200-163f1ba7076850",
                "monitor_count": "8",
                "sptoken":"Ube~U%3AU%3B%3AU48261efeced332cc9f20413132c69381cad5f53f4bfc428ed84627675ba90e48"
            }
        ]
        urlt = [
             'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=best&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=%s'%self.Ttime,
             'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=21388941485&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=%s'%self.Ttime,
             'http://www.yidianzixun.com/home/q/news_list_for_channel?channel_id=hot&cstart=0&cend=10&infinite=true&refresh=1&__from__=pc&multi=5&appid=web_yidian&_=%s'%self.Ttime,
             ]
        for j in range(0, len(urlt)):
            datay = requests.get(urlt[j], cookies=cookies[j], headers=headers)
            data = datay.content
            data = json.loads(data)
            data = data['result']
            try:
                for i in range(0, len(data)):
                    title = data[i]['title']
                    try:
                        pubTime = data[i]['date']
                    except:
                        pubTime = ''
                    url = data[i]['docid']
                    try:
                        pic_url = data[i]['image_urls'][0]
                        if 'http' not in pic_url:
                            pic_url = 'http://i1.go2yd.com/image.php?type=thumbnail_336x216&url=' + pic_url
                    except:
                        pic_url = ''
                    try:
                        describe = data[i]['summary']
                    except:
                        describe = ''
                    try:
                        category = data[i]['category']
                    except:
                        category = '要闻'
                    url = 'http://www.yidianzixun.com/article/' + url
                    yield scrapy.Request(url, meta={
                        'title': title,
                        'pubTime': pubTime,
                        'pic_url': pic_url,
                        'describe': describe,
                        'category': category,
                        "home_url":"www.yidianzi.com"
                    }, callback=self.parse, dont_filter=True)
            except:
                pass

    def parse(self, response):
        title = response.meta['title']
        publishedDate = response.meta['pubTime']
        pic_url = response.meta['pic_url']
        describe = response.meta['describe']
        category = response.meta['category']
        home_url = response.meta['home_url']
        app_name = '一点资讯'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        try:
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
                pic_more_url = re.findall('<imgsrc="(.*?)"', contentt)
                pic_more_url1 = []
                for i in range(0, len(pic_more_url)):
                    if 'http' not in pic_more_url[i]:
                        pic_more_urlt = 'http:' + pic_more_url[i]
                        pic_more_url1.append(pic_more_urlt)
                    else:
                        pic_more_url1.append(pic_more_url[i])
                pic_more_url = str(set(pic_more_url1))
            except:
                content = response.xpath('//div[@class="video-wrapper"]').extract()
                contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                content = re.findall('<videosrc="(.*?)"', contentt)[0]
                pic_more_url = ''
        except:
            content = response.xpath('//p').extract()
            contentt = ''
            for i in range(0, len(content)):
                contentt += content[i].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
            t = re.findall('>(.*?)<', contentt)
            contenttt = ''
            for i in range(0, len(t)):
                contenttt += t[i]
            content = contenttt
            pic_more_url = ''
        try:
            author = response.xpath('//a[@class="doc-source"]/text()').extract()[0]
        except:
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


