#coding=utf-8
import scrapy
import json,re,time
from news.items import NewsItem
from lxml.etree import HTML

class voayingwen(scrapy.Spider):
    name = 'voayingwenwang'
    start_urls = [
        'https://www.voanews.com/z/599',#US News
        'https://www.voanews.com/z/4720',#US Politics
        'https://www.voanews.com/z/4720?p=1',
        ''
    ]