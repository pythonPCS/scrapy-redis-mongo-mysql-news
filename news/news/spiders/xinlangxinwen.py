#coding=utf-8
import scrapy
from news.items import NewsItem
import json,re,time
class xinlang(scrapy.Spider):
    name = 'xinlang'
    start_urls = [
        'http://newsapi.sina.cn/?resource=hbpage&newsId=HB-1-snhs/index-search&lq=1&page=1&newpage=0&keyword=%E4%B9%A0%E8%BF%91%E5%B9%B3&lDid=9777f76f-d895-4801-b7ae-2edaef39eaba&oldChwm=12040_0006&city=WMXX2971&loginType=0&authToken=4dd0e751f289161adeec2bb997181325&link=&authGuid=6409396086577890289&ua=Xiaomi-MI+5s__sinanews__6.8.9__android__6.0.1&deviceId=7cd27e609fa72795&connectionType=2&resolution=1080x1920&weiboUid=&mac=02%3A00%3A00%3A00%3A00%3A00&osVersion=6.0.1&chwm=12040_0006&weiboSuid=&andId=fcdf1040e0f0ec2a&from=6068995012&sn=322185b8&aId=01AuLIAggwvv6q8bymRfRsl8NQvpxv4XcbyMun5eSkTzeJ0S4.&deviceIdV1=7cd27e609fa72795&osSdk=23&abver=1528118872689&accessToken=&abt=314_302_297_281_275_269_267_255_253_251_249_241_237_231_229_228_226_217_215_207_203_191_189_187_153_149_143_141_135_128_113_111_65_57_45_37_21_18_16_13&seId=f295bff3b2&imei=864454030661742&deviceModel=Xiaomi__Xiaomi__MI+5s&location=39.963886%2C116.358482&authUid=0&urlSign=1bd4875da4&rand=25',
        'http://newsapi.sina.cn/?resource=hbpage&newsId=HB-1-snhs/index-search&lq=1&page=2&newpage=0&keyword=%E4%B9%A0%E8%BF%91%E5%B9%B3&lDid=9777f76f-d895-4801-b7ae-2edaef39eaba&oldChwm=12040_0006&city=WMXX2971&loginType=0&authToken=4dd0e751f289161adeec2bb997181325&link=&authGuid=6409396086577890289&ua=Xiaomi-MI+5s__sinanews__6.8.9__android__6.0.1&deviceId=7cd27e609fa72795&connectionType=2&resolution=1080x1920&weiboUid=&mac=02%3A00%3A00%3A00%3A00%3A00&osVersion=6.0.1&chwm=12040_0006&weiboSuid=&andId=fcdf1040e0f0ec2a&from=6068995012&sn=322185b8&aId=01AuLIAggwvv6q8bymRfRsl8NQvpxv4XcbyMun5eSkTzeJ0S4.&deviceIdV1=7cd27e609fa72795&osSdk=23&abver=1528118872689&accessToken=&abt=314_302_297_281_275_269_267_255_253_251_249_241_237_231_229_228_226_217_215_207_203_191_189_187_153_149_143_141_135_128_113_111_65_57_45_37_21_18_16_13&seId=f295bff3b2&imei=864454030661742&deviceModel=Xiaomi__Xiaomi__MI+5s&location=39.963886%2C116.358482&authUid=0&urlSign=1bd4875da4&rand=25',
        'http://newsapi.sina.cn/?resource=hbpage&newsId=HB-1-snhs/index-search&lq=1&page=3&newpage=0&keyword=%E4%B9%A0%E8%BF%91%E5%B9%B3&lDid=9777f76f-d895-4801-b7ae-2edaef39eaba&oldChwm=12040_0006&city=WMXX2971&loginType=0&authToken=4dd0e751f289161adeec2bb997181325&link=&authGuid=6409396086577890289&ua=Xiaomi-MI+5s__sinanews__6.8.9__android__6.0.1&deviceId=7cd27e609fa72795&connectionType=2&resolution=1080x1920&weiboUid=&mac=02%3A00%3A00%3A00%3A00%3A00&osVersion=6.0.1&chwm=12040_0006&weiboSuid=&andId=fcdf1040e0f0ec2a&from=6068995012&sn=322185b8&aId=01AuLIAggwvv6q8bymRfRsl8NQvpxv4XcbyMun5eSkTzeJ0S4.&deviceIdV1=7cd27e609fa72795&osSdk=23&abver=1528118872689&accessToken=&abt=314_302_297_281_275_269_267_255_253_251_249_241_237_231_229_228_226_217_215_207_203_191_189_187_153_149_143_141_135_128_113_111_65_57_45_37_21_18_16_13&seId=f295bff3b2&imei=864454030661742&deviceModel=Xiaomi__Xiaomi__MI+5s&location=39.963886%2C116.358482&authUid=0&urlSign=1bd4875da4&rand=25',
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        data = json.loads(response.body)
        data = data['data']['list']['feed1']
        for i in range(len(data)):
            title = data[i]['title']
            pic = data[i]['image']
            url = data[i]['url']
            author = data[i]['source']
            yield scrapy.Request(url,meta={
                'title':title,
                'pic':pic,
                'author':author
            },callback=self.parse_item, dont_filter=True)

    def parse_item(self,response):
        title = response.meta['title'].replace('&lt;','').replace('em&gt;','').replace('/','')
        pic_url = response.meta['pic']
        author =response.meta['author']
        app_name = '新浪新闻'
        describe = ''
        category = '要闻'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        home_url = 'http://newsapi.sina.cn/'
        content =response.xpath('//article[@class="art_box"]').extract()
        contentt = content[0].replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
        content = re.findall('>(.*?)<', contentt)
        contentdata = ''
        for i in content:
            contentdata += i
        content = contentdata
        try:
            publishedDate = response.xpath('//time[@class="art_time"]/text()').extract()[0].replace('.','-')
        except:
            publishedDate = response.xpath('//time[@class="weibo_time"]').extract()[0]
            publishedDate = publishedDate.replace('\t','').replace('\n','').replace('\r','')
            publishedDate = re.findall('>(.*?)<', publishedDate)
            publishedDated = ''
            for i in publishedDate:
                publishedDated += i
            publishedDate = publishedDated
            publishedDate = '2018-' + publishedDate.replace('月','-').replace('日',' ') + ':00'
        try:
            pic_more_url = response.xpath("//div[@id='wx_pic']/img/@src").extract()[0]
        except:
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

