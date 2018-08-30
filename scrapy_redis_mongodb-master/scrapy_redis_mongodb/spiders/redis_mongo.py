#encoding:utf-8
from scrapy_redis.spiders import RedisSpider
from ..items import data_redis_mongodb
class MySpider(RedisSpider):
    name = 'redis'
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_redis_mongodb.pipelines.Mysqlpipine': 300
        }}
    redis_key = 'myspider:start_urls'
    '''
        从redis里面读url,如果redis中存在表【hongniangSpider:start_urls】，
        则可以直接读取，如果没有表【hongniangSpider:start_urls】则需要lpush传
    '''

    def parse(self, response):
        print response.url
        item = data_redis_mongodb()
        item['url'] = response.url
        item['title'] = response.xpath("//td[@id='sharetitle']/text()").extract_first()
        item['place'] = response.xpath("//tr[@class='c bottomline']/td[1]/text()").extract_first()
        item['types'] = response.xpath("//tr[@class='c bottomline']/td[2]/text()").extract_first()
        item['num'] = response.xpath("//tr[@class='c bottomline']/td[3]/text()").extract_first()
        yield item