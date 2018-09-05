#coding=utf-8
import time,re,json
import scrapy
from news.items import NewsItem
from lxml.etree import HTML
class guardian(scrapy.Spider):
    name = 'guardian'

    count = 0
    download_delay = 0
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def start_requests(self):
        start_urls = [
            # 大频道Home
            # Headlines:
            'https://mobile.guardianapis.com/us/groups/collections/us-alpha/news/regular-stories',
            # Spotlight:
            'https://mobile.guardianapis.com/us/groups/collections/us-alpha/features/feature-stories',
            # World Cup 2018:
            # 'https://mobile.guardianapis.com/us/groups/collections/189d1918-9c46-4bb4-a695-cc22f44dfe34',
            # Opinions:
            'https://mobile.guardianapis.com/us/groups/collections/98df412d-b0e7-4d9a-98c2-062642823e94',
            # Culture:
            'https://mobile.guardianapis.com/us/groups/collections/fb59c1f8-72a7-41d5-8365-a4d574809bed',
            # Across the country:
            'https://mobile.guardianapis.com/us/groups/collections/5a59a4e5-074e-4a2a-8bbe-2743e07ae30f',
            # Around the world:
            'https://mobile.guardianapis.com/us/groups/collections/adb2876e-946a-49ad-b641-e405d24e5f18',
            # Explore:
            'https://mobile.guardianapis.com/us/groups/collections/5fd45b04-c512-4a8c-a9b5-cc07a6097049',
            # Most viewed:
            'https://mobile.guardianapis.com/us/groups/collections/us/most-viewed/regular-stories',

            # # 大频道US：
            # US Headlines:
            'https://mobile.guardianapis.com/us/groups/collections/ec5e3c77-2684-44a0-bfbd-d337edcb2cba',
            # US Business:
            'https://mobile.guardianapis.com/us/groups/collections/b0e0bc29-41b5-4dd7-8a5e-f5d4129971a7',
            # US Politics:
            'https://mobile.guardianapis.com/us/groups/collections/436ed09d-614f-4418-8500-d1fa9e20404e',
            # Most viewed in US News:
            'https://mobile.guardianapis.com/us/groups/collections/8e2f6e01-1af5-49c1-9cf9-73643365ab82',

            # 大频道Politics:
            # Headlines:
            'https://mobile.guardianapis.com/us/groups/collections/8a12631c-72dd-4f57-baec-24ef7b2abfca',
            # Opinion:
            'https://mobile.guardianapis.com/us/groups/collections/21450e4f-a452-4601-a4b3-03ba00b5da1a',
            # Trump Russia investigation:
            'https://mobile.guardianapis.com/us/groups/collections/357173cc-06e1-4b86-b2f0-74f0b0b05f94',
            # Most viewed in US politics:
            'https://mobile.guardianapis.com/us/groups/collections/04549857-4025-45ec-b7c8-68f4a14a7562',

            # 大频道World:
            # World news:
            'https://mobile.guardianapis.com/us/groups/collections/49ac-e112-5a5c-ff9d',
            # Most viewed in world news:
            'https://mobile.guardianapis.com/us/groups/collections/558b-3b8b-3485-d9ff',
            # Cities:
            'https://mobile.guardianapis.com/us/groups/collections/df6de230-16cf-4c2a-b892-fff893fccec5',
            # Around the world:
            'https://mobile.guardianapis.com/us/groups/collections/951dae3c-6b0d-4cb1-919f-e69f671cc39a',
            # Opinion & analysis:
            'https://mobile.guardianapis.com/us/groups/collections/e92b-7852-9615-d281',
            # Spotlight:
            'https://mobile.guardianapis.com/us/groups/collections/030e17a4-00f1-4aca-8d78-7b152c992111',
            # Global development:
            'https://mobile.guardianapis.com/us/groups/collections/9d2d867a-964c-43cc-a05d-3e517cc89247',

            # World里面还有Asia频道：
            # Asia:
            'https://mobile.guardianapis.com/us/groups/collections/c531-61e2-fb9d-fcc7',
            # Asia Pacific:
            'https://mobile.guardianapis.com/us/groups/collections/4f5e7a27-0e66-47df-b3ff-d49d884399a0',
            # South & central Asia:
            'https://mobile.guardianapis.com/us/groups/collections/5b6dfa32-4782-49d4-88bc-a020b8cc695e',

        ]
        category = [
            # 大频道Home：
            'Home-Headlines',
            'Home-Spotlight',
            # 'Home-World Cup 2018',
            'Home-Opinions',
            'Home-Culture',
            'Home-Across the country',
            'Home-Around the world',
            'Home-Explore',
            'Home-Most viewed',

            # 大频道US：
            'US-Headlines',
            'US-Business',
            'US-Politics',
            'US-Most viewed in US News',

            # 大频道Politics:
            'Politics-Headlines',
            'Politics-Opinion',
            'Politics-Trump Russia investigation',
            'Politics-Most viewed in US politics',

            # 大频道World:
            'World-World news',
            'World-Most viewed in world news',
            'World-Cities',
            'World-Around the world',
            'World-Opinion & analysis',
            'World-Spotlight',
            'World-Global development',

            # World里面还有Asia频道：
            'World-Asia',
            'World-Asia Pacific',
            'World-South & central Asia',

        ]
        # print len(start_urls),len(category)

        for i in range(len(start_urls)):
            yield scrapy.Request(start_urls[i],
                                 meta={
                                     'category':category[i],
                                 },
                                 callback=self.parse_item)

    def parse_item(self, response):
        data_json = json.loads(response.body)
        if 'cards' in data_json.keys():
            for item in data_json['cards']:
                category = response.meta['category']
                title = item['item']['title']
                pic_url = item['item']['displayImages'][0]['urlTemplate'].replace('w=#{width}&h=#{height}&quality=#{quality}','')
                describe = item['item']['trailText']
                app_name = '英国卫报'
                try:
                    selector = HTML(item['item']['body'])
                except:
                    return
                content = selector.xpath('//text()')
                content = ''.join(content)
                content = content.replace('\t', '').replace('\n', '').replace('\r', '')
                publishedDate = item['item']['webPublicationDate'].replace('T',' ').replace('Z','')
                author = item['item']['byline']
                crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                home_url = response.url
                url = 'https://www.theguardian.com/'+item['item']['id']
                pic_more_url = []
                for pic in item['item']['bodyImages']:
                    pic_more_url.append(pic['urlTemplate'].replace('w=#{width}&h=#{height}&quality=#{quality}',''))

                print "app名称", app_name
                print "主图片url", pic_url
                print "子图片url", pic_more_url
                print "作者", author
                print "详情页地址", url
                print "所属类型", category
                print "标题", title
                print "描述", describe
                print "内容", content
                print "主url", home_url
                print "发布时间", publishedDate
                print "爬取时间", crawlTime
                print '\n\n'
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
