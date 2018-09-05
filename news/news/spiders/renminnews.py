#coding=utf-8
import scrapy
import time
import json
import re
from news.items import NewsItem

class rmrb(scrapy.Spider):
    name = 'renminnews'
    Ttime = int(round(time.time()*1000))
    count = 0
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def start_requests(self):
        t1 = '1|||03847eef-3885-36cd-87ce-d10d6ed86ce0|Nexus 5|Android 4.4.4|LGE|1080*1776|1||6863551|1776|1080|620|0.0|0.0|' + '1' + '|北京市|' + str(self.Ttime) + '|1|0|20|0|0|6.2.0rmrbsecurity$#%sut49fbb427a508bcc'
        t2 = '1|||03847eef-3885-36cd-87ce-d10d6ed86ce0|Nexus 5|Android 4.4.4|LGE|1080*1776|1||6863551|1776|1080|620|0.0|0.0|' + '2' + '|北京市|' + str(self.Ttime) + '|1|0|20|0|0|6.2.0rmrbsecurity$#%sut49fbb427a508bcc'
        tt1 = self.md5(t1)
        tt2 = self.md5(t2)
        url =[
            'http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=1&city=&citycode=&device=03847eef-3885-36cd-87ce-d10d6ed86ce0&device_model=Nexus 5&device_os=Android 4.4.4&device_product=LGE&device_size=1080*1776&device_type=1&district=&fake_id=6863551&image_height=1776&image_wide=1080&interface_code=620&latitude=0.0&longitude=0.0&page=1&province=北京市&province_code=%s&refresh_tag=1&refresh_time=0&show_num=20&update_time=0&userId=0&version=6.2.0&securitykey=%s'%(self.Ttime,tt1),
            'http://app.peopleapp.com/Api/600/HomeApi/getContentList?category_id=1&city=&citycode=&device=03847eef-3885-36cd-87ce-d10d6ed86ce0&device_model=Nexus 5&device_os=Android 4.4.4&device_product=LGE&device_size=1080*1776&device_type=1&district=&fake_id=6863551&image_height=1776&image_wide=1080&interface_code=620&latitude=0.0&longitude=0.0&page=2&province=北京市&province_code=%s&refresh_tag=1&refresh_time=0&show_num=20&update_time=0&userId=0&version=6.2.0&securitykey=%s'%(self.Ttime,tt2)
        ]
        for i in range(len(url)):
            yield scrapy.Request(url[i], callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        data = data['data']
        accept_title = []
        for i in range(0,len(data)):
            title = data[i]['title']
            url = data[i]['share_url']
            pic_url = data[i]['share_image']
            pubtime = data[i]['news_time'].split(' ')
            pubtime1 = pubtime[0]
            try:
                pubtime2 = pubtime[1].replace('-',":")
                publishedDate = pubtime1 + ' ' + pubtime2
            except:
                publishedDate = pubtime1 + ' 00:00:00'
            timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
            publishedDate = time.mktime(timeArray)
            if publishedDate >= self.timeStamp:
                accept_title.append(title)
                publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(publishedDate))
                yield scrapy.Request(url,meta={
                    'title':title,
                    'publishedDate':publishedDate,
                    'home_url':response.url,
                    'pic_url':pic_url
                },callback=self.parse_item)

        if len(accept_title) > 0:
            num = re.findall('page=(.*?)&',str(response.url))
            num0 = 'page=' + num[0]
            numt = int(num[0]) + 1
            t = '1|||03847eef-3885-36cd-87ce-d10d6ed86ce0|Nexus 5|Android 4.4.4|LGE|1080*1776|1||6863551|1776|1080|620|0.0|0.0|' + str(numt) + '|北京市|' + str(self.Ttime) + '|1|0|20|0|0|6.2.0rmrbsecurity$#%sut49fbb427a508bcc'
            keynum = self.md5(t)
            num1 = 'page=' + str(int(num[0]) + 1)
            key = str(response.url).split('securitykey=')[0]
            url = (key + 'securitykey=' + keynum).replace(num0,num1)
            yield scrapy.Request(url,callback=self.parse)

    def parse_item(self,response):
        title = response.meta['title']
        publishedDate = response.meta['publishedDate']
        home_url = response.meta['home_url']
        describe = ''
        app_name = '人民日报'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        pic_url = response.meta['pic_url']
        author = ''
        category = u'首页新闻'.encode('utf-8')
        try:
            try:
                content = response.xpath('//div[@class="article"]').extract()
                contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                content = re.findall('>(.*?)<', contentt)
                contentdata = ''
                for i in content:
                    contentdata += i
                content = contentdata
                pic_more_url = re.findall('imgsrc="(.*?)"',content)
                pic_more_url1 = []
                for i in range(0,len(pic_more_url)):
                    pic_more_url1.append(pic_more_url[i])
                pic_more_url = str(set(pic_more_url1))
            except:
                content = response.xpath('//div[@class="article long-article"]').extract()
                contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                content = re.findall('>(.*?)<', contentt)
                contentdata = ''
                for i in content:
                    contentdata += i
                content = contentdata
                pic_more_url = re.findall('imgsrc="(.*?)"', content)
                pic_more_url1 = []
                for i in range(0, len(pic_more_url)):
                    pic_more_url1.append(pic_more_url[i])
                pic_more_url = str(set(pic_more_url1))
        except:
            content = ''
            pic_more_url = ''
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
        numappName = self.readjson()
        if len(numappName) == 0:
            items = {
                'url': response.url,
                'title': item['title']
            }
            with open('renminribao.json', 'a+') as fp:
                line = json.dumps(dict(items), ensure_ascii=False) + '\n'
                fp.write(line)
            yield item
        else:
            for i in range(len(numappName)):
                if numappName[i]['url'] == response.url or numappName[i]['title'] == item['title']:
                    return
            else:
                items = {
                    'url': response.url,
                    'title': item['title']
                }
                with open('renminribao.json', 'a+') as fp:
                    line = json.dumps(dict(items), ensure_ascii=False) + '\n'
                    fp.write(line)
                yield item

    def readjson(self):
        s = []
        file_object = open('renminribao.json', 'r')
        try:
            while True:
                line = file_object.readline()
                data = json.loads(line)
                s.append(data)
        finally:
            return s


    def md5(self,t):
            import hashlib
            m = hashlib.md5()
            m.update(t)
            return m.hexdigest()