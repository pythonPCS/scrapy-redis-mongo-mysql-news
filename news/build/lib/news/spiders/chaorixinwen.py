#coding=utf-8
import scrapy
import json, re, time
from news.items import NewsItem
import urllib2,urllib,sys
class chaorixinwen(scrapy.Spider):
    handle_httpstatus_list = [401]
    name = 'chaorixinwen'

    def start_requests(self):
        num = [
            'national', 'politics', 'eco', 'culture', 'tech_science', 'international', 'business'
        ]
        category = [
            '社会', '政治', '经济', '文化', '科学', '国际', '商业'
        ]
        # headers = {
        #     "Authorization ContentType": "eyJpdiI6Ik05VkVtQng1dEFlQis4bEZcL3ZcDJzUExYUGxJRUdDVnl2andEaWdSaEtOdUh4T3FzUm",
        #     "Accept-Encoding": "gzip"
        # }
        for i in range(len(num)):
            url = 'http://119.23.19.90:5000/news?category=%s/list'%num[i]
            yield scrapy.Request(url, meta={
                'category': category[i]
            }, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        print data