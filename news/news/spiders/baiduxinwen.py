#coding=utf-8
import time,re,json
import scrapy
from news.items import NewsItem

class baidu(scrapy.Spider):
    name = 'baiduxinwen'
    Ttime = int(round(time.time()*1000))
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def start_requests(self):
        url = 'https://news.baidu.com/sn/api/feed_channellist?pd=newsplus&os=android&sv=7.1.2.0&from=app&_uid=g8SNu0um2ulx8HuKlu2ci0is2tl5aB8o_iSW8_uNSiiOO2tgga2qi_u62ig8uvihA&_ua=_aBDCgaH-i46ywoUfpw1z4aBsiz5aX8D4a2Ai6DDB&_ut=5yG_YtM1vC_bhvhJgODpOYhuA&_from=1019026r&_cfrom=1019026r&_network=1_0&cen=uid_ua_ut'
        paramsnum = ['本地','科技','财经','国内','国际']
        datanum = ['102','8','6','2','1']
        for i in range(len(paramsnum)):
            params = {
                "cuid": "3ADAC23BAEBDC750FF38B3810FA334A1|918510050145753",
                "category_name": "%s"%paramsnum[i],
                "display_time": "%s"%self.Ttime,
                "action": "0",
                "category_id": "%s"%datanum[i],
                "ver": "6",
                "loc_ll": "116.365283,39.969771",
                "mid": "357541050015819_70:05:14:7d:2a:5f",
                "wf": "1"
            }
            yield scrapy.FormRequest(url, meta={
                'category': paramsnum[i],
                'datatime':datanum[i]
            }, formdata=params, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        data = data['data']['news']
        num = 0
        timett = data[len(data)-1]['pulltime']
        for i in range(len(data)):
            title = data[i]['title']
            url = data[i]['url']
            pubt = data[i]['pulltime']
            try:
                desc = data[i]['abs']
            except:
                desc = ''
            if int(float(pubt)/1000) >= self.timeStamp:
                num += 1
                pubt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(float(pubt)/1000)))
                yield scrapy.Request(url, meta={
                    'title': title,
                    'pubt': pubt,
                    'desc': desc,
                    'category': response.meta['category']
                }, callback=self.parse_item)
        if num > 0:
            numtime = response.meta['datatime']
            url = 'https://news.baidu.com/sn/api/feed_channellist?pd=newsplus&os=android&sv=7.1.2.0&from=app&_uid=g8SNu0um2ulx8HuKlu2ci0is2tl5aB8o_iSW8_uNSiiOO2tgga2qi_u62ig8uvihA&_ua=_aBDCgaH-i46ywoUfpw1z4aBsiz5aX8D4a2Ai6DDB&_ut=5yG_YtM1vC_bhvhJgODpOYhuA&_from=1019026r&_cfrom=1019026r&_network=1_0&cen=uid_ua_ut'
            params = {
                "cuid": "3ADAC23BAEBDC750FF38B3810FA334A1|918510050145753",
                "category_name": "%s" % response.meta['category'],
                "display_time": "%s"%timett ,
                "action": "0",
                "category_id": "%s" %numtime,
                "ver": "6",
                "loc_ll": "116.365283,39.969771",
                "mid": "357541050015819_70:05:14:7d:2a:5f",
                "wf": "1"
            }
            yield scrapy.FormRequest(url, meta={
                'category': response.meta['category'],
                'datatime': response.meta['datatime']
            }, formdata=params, callback=self.parse)

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



