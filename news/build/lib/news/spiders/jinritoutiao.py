#coding=utf-8
import json
import scrapy
import time,re,time
from news.items import NewsItem
from news.DataResource import TransportData
class jrtt(scrapy.Spider):
    name='jinritoutiao'
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    start_urls = [
        'https://ic.snssdk.com/api/news/feed/v51/?category=news_world&concern_id=6215497896255556098&refer=1&count=20&max_behot_time=' + str(time.strftime("%Y-%m-%d %H:%M:%S")) + '&loc_mode=7&tt_from=pre_load_more&iid=27913719571&device_id=42569103355&ac=wifi&channel=google&aid=13&app_name=news_article&version_code=609&version_name=6.0.9&device_platform=android&ab_version=293083,295237,283499,294017,291433,229305,290123,283849,277471,296213,294340,256772,295827,292992,295553,239098,286955,294504,288547,288955,290969,281389,295562,276205,289786,285344,295821,257280,281472,294388,295253,295754,295746,296108,240865,280773,293348,292434,294357,293126,293255,251712,296169,295029,31650,292322,289003,291513,275224,293805,258356,247850,281300,249045,294400,294217,294899,287591,288416,260654,292291,294856,293694,252766,249828,246859,294360&ab_client=a1,c4,e1,f2,g2,f7&ab_group=100167&ab_feature=102749,94563&abflag=3&ssmix=a&device_type=MI%202S&device_brand=Xiaomi&language=zh&os_api=21&os_version=5.0.2&uuid=862620027634098&openudid=e2e9e0c39ccae150&manifest_version_code=609&resolution=720*1280&dpi=320&update_version_code=6091',
        'https://ic.snssdk.com/api/news/feed/v51/?category=news_hot&concern_id=6215497896255556098&refer=1&count=20&max_behot_time=0&loc_mode=7&tt_from=pre_load_more&iid=27913719571&device_id=42569103355&ac=wifi&channel=google&aid=13&app_name=news_article&version_code=609&version_name=6.0.9&device_platform=android&ab_version=293083,295237,283499,294017,291433,229305,290123,283849,277471,296213,294340,256772,295827,292992,295553,239098,286955,294504,288547,288955,290969,281389,295562,276205,289786,285344,295821,257280,281472,294388,295253,295754,295746,296108,240865,280773,293348,292434,294357,293126,293255,251712,296169,295029,31650,292322,289003,291513,275224,293805,258356,247850,281300,249045,294400,294217,294899,287591,288416,260654,292291,294856,293694,252766,249828,246859,294360&ab_client=a1,c4,e1,f2,g2,f7&ab_group=100167&ab_feature=102749,94563&abflag=3&ssmix=a&device_type=MI%202S&device_brand=Xiaomi&language=zh&os_api=21&os_version=5.0.2&uuid=862620027634098&openudid=e2e9e0c39ccae150&manifest_version_code=609&resolution=720*1280&dpi=320&update_version_code=6091',     # 热点
        'https://ic.snssdk.com/api/news/feed/v51/?category=news_world&concern_id=6215497896255556098&refer=1&count=20&max_behot_time=0&loc_mode=7&tt_from=pre_load_more&iid=27913719571&device_id=42569103355&ac=wifi&channel=google&aid=13&app_name=news_article&version_code=609&version_name=6.0.9&device_platform=android&ab_version=293083,295237,283499,294017,291433,229305,290123,283849,277471,296213,294340,256772,295827,292992,295553,239098,286955,294504,288547,288955,290969,281389,295562,276205,289786,285344,295821,257280,281472,294388,295253,295754,295746,296108,240865,280773,293348,292434,294357,293126,293255,251712,296169,295029,31650,292322,289003,291513,275224,293805,258356,247850,281300,249045,294400,294217,294899,287591,288416,260654,292291,294856,293694,252766,249828,246859,294360&ab_client=a1,c4,e1,f2,g2,f7&ab_group=100167&ab_feature=102749,94563&abflag=3&ssmix=a&device_type=MI%202S&device_brand=Xiaomi&language=zh&os_api=21&os_version=5.0.2&uuid=862620027634098&openudid=e2e9e0c39ccae150&manifest_version_code=609&resolution=720*1280&dpi=320&update_version_code=6091',   #国际
        'https://ic.snssdk.com/api/news/feed/v51/?category=nineteenth&concern_id=6215497896255556098&refer=1&count=20&max_behot_time=0&loc_mode=7&tt_from=pre_load_more&iid=27913719571&device_id=42569103355&ac=wifi&channel=google&aid=13&app_name=news_article&version_code=609&version_name=6.0.9&device_platform=android&ab_version=293083,295237,283499,294017,291433,229305,290123,283849,277471,296213,294340,256772,295827,292992,295553,239098,286955,294504,288547,288955,290969,281389,295562,276205,289786,285344,295821,257280,281472,294388,295253,295754,295746,296108,240865,280773,293348,292434,294357,293126,293255,251712,296169,295029,31650,292322,289003,291513,275224,293805,258356,247850,281300,249045,294400,294217,294899,287591,288416,260654,292291,294856,293694,252766,249828,246859,294360&ab_client=a1,c4,e1,f2,g2,f7&ab_group=100167&ab_feature=102749,94563&abflag=3&ssmix=a&device_type=MI%202S&device_brand=Xiaomi&language=zh&os_api=21&os_version=5.0.2&uuid=862620027634098&openudid=e2e9e0c39ccae150&manifest_version_code=609&resolution=720*1280&dpi=320&update_version_code=6091',   #新时代
        'https://ic.snssdk.com/api/news/feed/v51/?category=news_finance&concern_id=6215497896255556098&refer=1&count=20&max_behot_time=0&loc_mode=7&tt_from=pre_load_more&iid=27913719571&device_id=42569103355&ac=wifi&channel=google&aid=13&app_name=news_article&version_code=609&version_name=6.0.9&device_platform=android&ab_version=293083,295237,283499,294017,291433,229305,290123,283849,277471,296213,294340,256772,295827,292992,295553,239098,286955,294504,288547,288955,290969,281389,295562,276205,289786,285344,295821,257280,281472,294388,295253,295754,295746,296108,240865,280773,293348,292434,294357,293126,293255,251712,296169,295029,31650,292322,289003,291513,275224,293805,258356,247850,281300,249045,294400,294217,294899,287591,288416,260654,292291,294856,293694,252766,249828,246859,294360&ab_client=a1,c4,e1,f2,g2,f7&ab_group=100167&ab_feature=102749,94563&abflag=3&ssmix=a&device_type=MI%202S&device_brand=Xiaomi&language=zh&os_api=21&os_version=5.0.2&uuid=862620027634098&openudid=e2e9e0c39ccae150&manifest_version_code=609&resolution=720*1280&dpi=320&update_version_code=6091', #财经
        'https://ic.snssdk.com/api/news/feed/v51/?category=news_military&concern_id=6215497896255556098&refer=1&count=20&max_behot_time=0&loc_mode=7&tt_from=pre_load_more&iid=27913719571&device_id=42569103355&ac=wifi&channel=google&aid=13&app_name=news_article&version_code=609&version_name=6.0.9&device_platform=android&ab_version=293083,295237,283499,294017,291433,229305,290123,283849,277471,296213,294340,256772,295827,292992,295553,239098,286955,294504,288547,288955,290969,281389,295562,276205,289786,285344,295821,257280,281472,294388,295253,295754,295746,296108,240865,280773,293348,292434,294357,293126,293255,251712,296169,295029,31650,292322,289003,291513,275224,293805,258356,247850,281300,249045,294400,294217,294899,287591,288416,260654,292291,294856,293694,252766,249828,246859,294360&ab_client=a1,c4,e1,f2,g2,f7&ab_group=100167&ab_feature=102749,94563&abflag=3&ssmix=a&device_type=MI%202S&device_brand=Xiaomi&language=zh&os_api=21&os_version=5.0.2&uuid=862620027634098&openudid=e2e9e0c39ccae150&manifest_version_code=609&resolution=720*1280&dpi=320&update_version_code=6091',#军事
        'https://ic.snssdk.com/api/news/feed/v51/?category=positive&concern_id=6215497896255556098&refer=1&count=20&max_behot_time=0&loc_mode=7&tt_from=pre_load_more&iid=27913719571&device_id=42569103355&ac=wifi&channel=google&aid=13&app_name=news_article&version_code=609&version_name=6.0.9&device_platform=android&ab_version=293083,295237,283499,294017,291433,229305,290123,283849,277471,296213,294340,256772,295827,292992,295553,239098,286955,294504,288547,288955,290969,281389,295562,276205,289786,285344,295821,257280,281472,294388,295253,295754,295746,296108,240865,280773,293348,292434,294357,293126,293255,251712,296169,295029,31650,292322,289003,291513,275224,293805,258356,247850,281300,249045,294400,294217,294899,287591,288416,260654,292291,294856,293694,252766,249828,246859,294360&ab_client=a1,c4,e1,f2,g2,f7&ab_group=100167&ab_feature=102749,94563&abflag=3&ssmix=a&device_type=MI%202S&device_brand=Xiaomi&language=zh&os_api=21&os_version=5.0.2&uuid=862620027634098&openudid=e2e9e0c39ccae150&manifest_version_code=609&resolution=720*1280&dpi=320&update_version_code=6091',     #正能量
        'https://ic.snssdk.com/api/news/feed/v51/?category=news_history&concern_id=6215497896255556098&refer=1&count=20&max_behot_time=0&loc_mode=7&tt_from=pre_load_more&iid=27913719571&device_id=42569103355&ac=wifi&channel=google&aid=13&app_name=news_article&version_code=609&version_name=6.0.9&device_platform=android&ab_version=293083,295237,283499,294017,291433,229305,290123,283849,277471,296213,294340,256772,295827,292992,295553,239098,286955,294504,288547,288955,290969,281389,295562,276205,289786,285344,295821,257280,281472,294388,295253,295754,295746,296108,240865,280773,293348,292434,294357,293126,293255,251712,296169,295029,31650,292322,289003,291513,275224,293805,258356,247850,281300,249045,294400,294217,294899,287591,288416,260654,292291,294856,293694,252766,249828,246859,294360&ab_client=a1,c4,e1,f2,g2,f7&ab_group=100167&ab_feature=102749,94563&abflag=3&ssmix=a&device_type=MI%202S&device_brand=Xiaomi&language=zh&os_api=21&os_version=5.0.2&uuid=862620027634098&openudid=e2e9e0c39ccae150&manifest_version_code=609&resolution=720*1280&dpi=320&update_version_code=6091', #历史
    ]

    def parse(self, response):
        data = json.loads(response.body)
        data = data['data']
        accept_title = []
        for i in range(0,len(data)):
            content =json.loads(data[i]['content'])
            try:
                desc = content['abstract']
            except:
                desc = ''
            try:
                title = content['title']
            except:
                title = ''
            try:
                url = content['share_url']
            except:
                url = ''
            if 'group' in url:
                url = re.findall('/group/(.*?)/',url)[0]
                url = 'http://m.toutiao.com/a' + url + '/'
            try:
                publishedDate = content['publish_time']
            except:
                publishedDate = 0
            publishedDated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
            print publishedDated
            if publishedDate >= self.timeStamp:
                publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(publishedDate)))
                accept_title.append(title)
                try:
                    yield scrapy.Request(url,meta={
                        "describe":desc,
                        'title':title,
                        'publishedDate':publishedDate,
                        'home_url':response.url
                    }, callback=self.parse_item, dont_filter=True)
                except:
                    print "url有问题!"
        if len(accept_title) > 0:
            num = json.loads(data[len(data)-1]['content'])['behot_time']
            numt = re.findall('max_behot_time=(.*?)&',str(response.url))[0]
            numtt = 'max_behot_time=' + numt
            numttt = 'max_behot_time=' + str(num)
            url = str(response.url).replace(numtt,numttt)
            print "下一页:",url
            yield scrapy.Request(url,callback=self.parse)

    def parse_item(self, response):
        describe = response.meta['describe']
        title = response.meta['title']
        home_url = response.meta['home_url']
        publishedDate = response.meta['publishedDate']
        pic_url = ''
        app_name = '今日头条'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        html = str(response.body).replace('\t', '').replace('\n', '').replace('\r', '')
        pic_more_url = re.findall('&quot;http://(.*?)&quot', html)
        pic_more_url1 = []
        for i in range(0, len(pic_more_url)):
            pic_more_urlt = 'http://' + pic_more_url[i]
            pic_more_url1.append(pic_more_urlt)
        pic_more_url = str(set(pic_more_url1))
        try:
            try:
                try:
                    content = response.xpath('//div[@class="content"]').extract()
                    content = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
                    content = re.findall('>(.*?)<', content)
                    contentdata = ''
                    for i in content:
                        contentdata += i
                    content = contentdata
                except:
                    html = str(response.body).replace('\t', '').replace('\n', '').replace('\r', '')
                    content = re.findall("content: '(.*?)'", html)[0]

            except:
                content = response.xpath('//p').extract()
                contentt = ''
                for i in range(0,len(content)):
                    contentt += content[i]
                content = contentt
        except:
            content = describe
        try:
            author = response.xpath('//span[@class="origin"]/text()').extract()[0]
        except:
            author = ''
        if 'news_hot' in home_url:
            category = '热点'.encode('utf-8')
        elif 'nineteenth' in home_url:
            category = '新时代'.encode('utf-8')
        elif 'news_finance' in home_url:
            category = '财经'.encode('utf-8')
        elif 'news_military' in home_url:
            category = '军事'.encode('utf-8')
        elif 'news_world' in home_url:
            category = '国际'.encode('utf-8')
        elif 'positive' in home_url:
            category = '正能量'.encode('utf-8')
        elif 'news_history' in home_url:
            category = '历史'.encode('utf-8')
        else:
            category = '推荐'.encode('utf-8')
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
                'title':item['title']
            }

            with open('jinritoutiao.json', 'a+') as fp:
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
                    'title':item['title']
                }
                with open('jinritoutiao.json', 'a+') as fp:
                    line = json.dumps(dict(items), ensure_ascii=False) + '\n'
                    fp.write(line)
                yield item

    def readjson(self):
        s = []
        file_object = open('jinritoutiao.json', 'r')
        try:
            while True:
                line = file_object.readline()
                data = json.loads(line)
                s.append(data)
        finally:
            return s







