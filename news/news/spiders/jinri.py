#coding=utf-8
import scrapy
import time
import json
import re
from news.items import NewsItem

class jinri(scrapy.Spider):
    name = 'jinri'
    start_urls = [
        'http://lf.snssdk.com/api/2/wap/search_content/?from=search_tab&keyword=%E4%B9%A0%E8%BF%91%E5%B9%B3&keyword_type=&cur_tab_title=search_tab&action_type=&plugin_enable=3&followbtn_template=%257B%2522color_style%2522%253A%2522red%2522%257D&iid=34576817871&device_id=46711983535&ac=wifi&channel=store_yingyonghui_cpd&aid=13&app_name=news_article&version_code=675&version_name=6.7.5&device_platform=android&ab_version=261581%252C197604%252C360501%252C368749%252C293033%252C367159%252C271178%252C357703%252C326524%252C326532%252C358832%252C295827%252C353305%252C366051%252C239097%252C360540%252C344351%252C170988%252C368832%252C366643%252C364965%252C365857%252C365054%252C363578%252C368303%252C368342%252C330632%252C297058%252C366609%252C276205%252C286212%252C350193%252C365026%252C366024%252C367077%252C277718%252C368359%252C364452%252C364280%252C369501%252C369166%252C368839%252C368937%252C369666%252C366034%252C323233%252C358512%252C363824%252C346556%252C361338%252C357124%252C319960%252C345191%252C362183%252C362908%252C171965%252C214069%252C31210%252C338062%252C366869%252C360991%252C358490%252C356267%252C280447%252C281291%252C347050%252C364988%252C325612%252C357403%252C361073%252C288416%252C362405%252C290188%252C366030%252C370015%252C353483%252C367984%252C358170&ab_client=a1%252Cc4%252Ce1%252Cf1%252Cg2%252Cf7&ab_group=100170&ab_feature=102749%252C94563&abflag=3&device_type=Nexus%2B5&device_brand=google&language=zh&os_api=19&os_version=4.4.4&uuid=352584064289389&openudid=def5d0d299d3042d&manifest_version_code=675&resolution=1080*1776&dpi=480&update_version_code=67505&_rticket=1528180449799&rom_version=19&plugin=10539&pos=5r_88Pzt0fzp9Ono-fi_p66ks6SrrqWqpLG__PD87d706eS_p794EQp5JzF4JR-_sb_88Pzt0fLz-vTp6Pn4v6esrKuzrqilqavg&fp=2rT_F2T5Pl5qFlGWPlU1FYGeFzKI&search_sug=1&forum=1&as=A1355BF156F2EE3&cp=5B16D2DECE535E1&count=10&cur_tab=1&format=json&offset=10&pd=synthesis&search_id=20180605143411172018007166664520',
        'http://lf.snssdk.com/api/2/wap/search_content/?from=search_tab&keyword=%E4%B9%A0%E8%BF%91%E5%B9%B3&keyword_type=&cur_tab_title=search_tab&action_type=&plugin_enable=3&followbtn_template=%257B%2522color_style%2522%253A%2522red%2522%257D&iid=34576817871&device_id=46711983535&ac=wifi&channel=store_yingyonghui_cpd&aid=13&app_name=news_article&version_code=675&version_name=6.7.5&device_platform=android&ab_version=261581%252C197604%252C360501%252C368749%252C293033%252C367159%252C271178%252C357703%252C326524%252C326532%252C358832%252C295827%252C353305%252C366051%252C239097%252C360540%252C344351%252C170988%252C368832%252C366643%252C364965%252C365857%252C365054%252C363578%252C368303%252C368342%252C330632%252C297058%252C366609%252C276205%252C286212%252C350193%252C365026%252C366024%252C367077%252C277718%252C368359%252C364452%252C364280%252C369501%252C369166%252C368839%252C368937%252C369666%252C366034%252C323233%252C358512%252C363824%252C346556%252C361338%252C357124%252C319960%252C345191%252C362183%252C362908%252C171965%252C214069%252C31210%252C338062%252C366869%252C360991%252C358490%252C356267%252C280447%252C281291%252C347050%252C364988%252C325612%252C357403%252C361073%252C288416%252C362405%252C290188%252C366030%252C370015%252C353483%252C367984%252C358170&ab_client=a1%252Cc4%252Ce1%252Cf1%252Cg2%252Cf7&ab_group=100170&ab_feature=102749%252C94563&abflag=3&device_type=Nexus%2B5&device_brand=google&language=zh&os_api=19&os_version=4.4.4&uuid=352584064289389&openudid=def5d0d299d3042d&manifest_version_code=675&resolution=1080*1776&dpi=480&update_version_code=67505&_rticket=1528180449799&rom_version=19&plugin=10539&pos=5r_88Pzt0fzp9Ono-fi_p66ks6SrrqWqpLG__PD87d706eS_p794EQp5JzF4JR-_sb_88Pzt0fLz-vTp6Pn4v6esrKuzrqilqavg&fp=2rT_F2T5Pl5qFlGWPlU1FYGeFzKI&search_sug=1&forum=1&as=A1355BF156F2EE3&cp=5B16D2DECE535E1&count=10&cur_tab=1&format=json&offset=20&pd=synthesis&search_id=20180605143411172018007166664520',
        'http://lf.snssdk.com/api/2/wap/search_content/?from=search_tab&keyword=%E4%B9%A0%E8%BF%91%E5%B9%B3&keyword_type=&cur_tab_title=search_tab&action_type=&plugin_enable=3&followbtn_template=%257B%2522color_style%2522%253A%2522red%2522%257D&iid=34576817871&device_id=46711983535&ac=wifi&channel=store_yingyonghui_cpd&aid=13&app_name=news_article&version_code=675&version_name=6.7.5&device_platform=android&ab_version=261581%252C197604%252C360501%252C368749%252C293033%252C367159%252C271178%252C357703%252C326524%252C326532%252C358832%252C295827%252C353305%252C366051%252C239097%252C360540%252C344351%252C170988%252C368832%252C366643%252C364965%252C365857%252C365054%252C363578%252C368303%252C368342%252C330632%252C297058%252C366609%252C276205%252C286212%252C350193%252C365026%252C366024%252C367077%252C277718%252C368359%252C364452%252C364280%252C369501%252C369166%252C368839%252C368937%252C369666%252C366034%252C323233%252C358512%252C363824%252C346556%252C361338%252C357124%252C319960%252C345191%252C362183%252C362908%252C171965%252C214069%252C31210%252C338062%252C366869%252C360991%252C358490%252C356267%252C280447%252C281291%252C347050%252C364988%252C325612%252C357403%252C361073%252C288416%252C362405%252C290188%252C366030%252C370015%252C353483%252C367984%252C358170&ab_client=a1%252Cc4%252Ce1%252Cf1%252Cg2%252Cf7&ab_group=100170&ab_feature=102749%252C94563&abflag=3&device_type=Nexus%2B5&device_brand=google&language=zh&os_api=19&os_version=4.4.4&uuid=352584064289389&openudid=def5d0d299d3042d&manifest_version_code=675&resolution=1080*1776&dpi=480&update_version_code=67505&_rticket=1528180449799&rom_version=19&plugin=10539&pos=5r_88Pzt0fzp9Ono-fi_p66ks6SrrqWqpLG__PD87d706eS_p794EQp5JzF4JR-_sb_88Pzt0fLz-vTp6Pn4v6esrKuzrqilqavg&fp=2rT_F2T5Pl5qFlGWPlU1FYGeFzKI&search_sug=1&forum=1&as=A1355BF156F2EE3&cp=5B16D2DECE535E1&count=10&cur_tab=1&format=json&offset=30&pd=synthesis&search_id=20180605143411172018007166664520',
        'http://lf.snssdk.com/api/2/wap/search_content/?from=search_tab&keyword=%E4%B9%A0%E8%BF%91%E5%B9%B3&keyword_type=&cur_tab_title=search_tab&action_type=&plugin_enable=3&followbtn_template=%257B%2522color_style%2522%253A%2522red%2522%257D&iid=34576817871&device_id=46711983535&ac=wifi&channel=store_yingyonghui_cpd&aid=13&app_name=news_article&version_code=675&version_name=6.7.5&device_platform=android&ab_version=261581%252C197604%252C360501%252C368749%252C293033%252C367159%252C271178%252C357703%252C326524%252C326532%252C358832%252C295827%252C353305%252C366051%252C239097%252C360540%252C344351%252C170988%252C368832%252C366643%252C364965%252C365857%252C365054%252C363578%252C368303%252C368342%252C330632%252C297058%252C366609%252C276205%252C286212%252C350193%252C365026%252C366024%252C367077%252C277718%252C368359%252C364452%252C364280%252C369501%252C369166%252C368839%252C368937%252C369666%252C366034%252C323233%252C358512%252C363824%252C346556%252C361338%252C357124%252C319960%252C345191%252C362183%252C362908%252C171965%252C214069%252C31210%252C338062%252C366869%252C360991%252C358490%252C356267%252C280447%252C281291%252C347050%252C364988%252C325612%252C357403%252C361073%252C288416%252C362405%252C290188%252C366030%252C370015%252C353483%252C367984%252C358170&ab_client=a1%252Cc4%252Ce1%252Cf1%252Cg2%252Cf7&ab_group=100170&ab_feature=102749%252C94563&abflag=3&device_type=Nexus%2B5&device_brand=google&language=zh&os_api=19&os_version=4.4.4&uuid=352584064289389&openudid=def5d0d299d3042d&manifest_version_code=675&resolution=1080*1776&dpi=480&update_version_code=67505&_rticket=1528180449799&rom_version=19&plugin=10539&pos=5r_88Pzt0fzp9Ono-fi_p66ks6SrrqWqpLG__PD87d706eS_p794EQp5JzF4JR-_sb_88Pzt0fLz-vTp6Pn4v6esrKuzrqilqavg&fp=2rT_F2T5Pl5qFlGWPlU1FYGeFzKI&search_sug=1&forum=1&as=A1355BF156F2EE3&cp=5B16D2DECE535E1&count=10&cur_tab=1&format=json&offset=40&pd=synthesis&search_id=20180605143411172018007166664520',
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime('2018-06-01', "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))


    def parse(self, response):
        data = json.loads(response.body)
        data = data['data']
        for i in range(len(data)):
            title = data[i]['title']
            pubt = data[i]['datetime']
            try:
                desc = data[i]['abstract']
            except:
                desc = ''
            url = data[i]['article_url']
            try:
                pic = data[i]['image_list']
            except:
                pic = ''
            timeArray = time.strptime(pubt, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            if timeStamp >= self.timeStamp:
                yield scrapy.Request(url, meta={
                    'title':title,
                    'pubt':pubt,
                    'desc':desc,
                    'pic':pic
                }, callback=self.parse_item,dont_filter=True)

    def parse_item(self,response):
        title = response.meta['title']
        publishedDate = response.meta['pubt']
        describe = response.meta['desc']
        app_name = '今日头条'
        category = '推荐'
        pic_url = response.meta['pic']
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        author = ''
        home_url = 'http://lf.snssdk.com/'
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
                    content = content.replace('a', '').replace('b', '').replace('c', '').replace('d', '').replace('e',
                                                                                                                  '').replace(
                        'f', '').replace('g', '').replace('h', '').replace('i', '').replace('j', '').replace('k', '').replace(
                        'l', '').replace('m', '').replace('n', '').replace('o', '').replace('p', '').replace('q', '').replace(
                        'r', '').replace('s', '').replace('t', '').replace('u', '').replace('v', '').replace('w', '').replace(
                        'x', '').replace('y', '').replace('z', '').replace('&', '').replace('/', '').replace(';', '')
            except:
                content = response.xpath('//p').extract()
                contentt = ''
                for i in range(0,len(content)):
                    contentt += contentt
                content = contentt
        except:
            html = str(response.body).replace('\t', '').replace('\n', '').replace('\r', '')
            content = html.replace('a', '').replace('b', '').replace('c', '').replace('d', '').replace('e','').replace(
                'f', '').replace('g', '').replace('h', '').replace('i', '').replace('j', '').replace('k', '').replace(
                'l', '').replace('m', '').replace('n', '').replace('o', '').replace('p', '').replace('q', '').replace(
                'r', '').replace('s', '').replace('t', '').replace('u', '').replace('v', '').replace('w', '').replace(
                'x', '').replace('y', '').replace('z', '').replace('&', '').replace('/', '').replace(';', '').replace('<','').replace('>','')

        html = str(response.body).replace('\t', '').replace('\n', '').replace('\r', '')
        pic_more_url = re.findall('&quot;http://(.*?)&quot', html)
        pic_more_url1 = []
        for i in range(0, len(pic_more_url)):
            pic_more_urlt = 'http://' + pic_more_url[i]
            pic_more_url1.append(pic_more_urlt)
        pic_more_url = str(set(pic_more_url1))
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





