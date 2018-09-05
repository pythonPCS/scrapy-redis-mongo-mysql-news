#coding=utf-8
import scrapy,re,time,json
from news.items import NewsItem

class huaerjie(scrapy.Spider):
    name = 'huaerjieyingwenwang'
    start_urls = [
        'https://www.wsj.com/search/term.html?KEYWORDS=Xi%20Jinping',
        'https://www.wsj.com/search/term.html?KEYWORDS=Xi%20Jinping&page=2'
    ]

    def parse(self, response):
        links = response.xpath('//ul[@class="items hedSumm"]/li/div/div[1]/h3/a/@href').extract()
        title = response.xpath('//ul[@class="items hedSumm"]/li/div/div[1]/h3/a/text()').extract()
        for i in range(len(links)):
            if 'http' not in links[i]:
                url = 'https://www.wsj.com' + links[i]
            else:
                url = links[i]
            tit = title[i]
            yield scrapy.Request(url, meta={
                'title': tit,
                'home_url': response.url
            }, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        title = response.meta['title']
        home_url = response.meta['home_url']
        app_name = '华尔街日报英文网'
        describe = ''
        pic_url = ''
        author = ''
        publishedDate = response.xpath('//time/text()').extract()[0].replace(' ','')
        publishedDate = publishedDate.replace('\t', '').replace('\n', '').replace('\r', '')
        pic_more_url = ''
        try:
            content = response.xpath('//div[@class="wsj-snippet-body"]').extract()[0]
            content = content.replace('\t', '').replace('\n', '').replace('\r', '')
        except:
            content = response.xpath('//p').extract()
            contentt = ''
            for i in range(len(content)):
                contentt += content[i]
            content = contentt.replace('\t', '').replace('\n', '').replace('\r', '')
            content = re.findall('>(.*?)<', content)
            contentdata = ''
            for i in content:
                contentdata += i
            content = contentdata
        print publishedDate
        print content