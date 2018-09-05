# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
class NewsPipeline(object):
    def process_item(self, item, spider):
        time_str = time.strftime("%Y-%m-%d")
        fileName =  str(time_str) + '.json'
        items_title = item['title']
        items_time = item['publishedDate']
        items_cate = item['category']
        items_appname = item['app_name']
        items_content = item['content']
        itemss = {
            "appname":items_appname,
            # "appurl":item['url'],
            "apptitle":items_title,
            'apptimes':items_time,
            # 'appcategory':items_cate,
            # 'apptontent':items_content
        }
        # ttt = 'https://114.255.183.210:2181/pro0912/insertDataToFuckEs.htm?app_name=人民日报&content_url=' +  item['url']+ '&content_type=首页新闻&title=' + item['title'] + '&content=' + item['content'] + '&pubTime=' + items_time
        with open(fileName, 'a+') as fp:
            line = json.dumps(dict(itemss), ensure_ascii=False) + '\n'
            fp.write(line)
        return item
