#coding=utf-8
import scrapy
import re, json, time
from news.items import NewsItem
class huashengdun(scrapy.Spider):
    name = 'youbao'
    start_urls = [
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/37b6940a-7663-11e8-bda1-18e53a448a14/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/bba910e2-7890-11e8-aeee-4d04c8ac6158/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/d1fee390-78b2-11e8-8df3-007495a78738/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/69a55856-7894-11e8-93cc-6d3beccdd7a3/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/ed3db69c3da74f3539e61a72d087c404/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/36b1c9ac-788a-11e8-93cc-6d3beccdd7a3/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/29ed6c577cebe193576411ca04d8d93d/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/2439c1beafe8a762800e2662c87632da/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/c0e1205e-6a21-11e8-bbc5-dc9f3634fa0a/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/2f82a4ec81e8d0e638ce4e465ed4ce6f/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/bd9e8b662f9182731f40991796b162f4/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/5e891566-78a8-11e8-aeee-4d04c8ac6158/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/d0afd1a0-7567-11e8-b4b7-308400242c2e/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/e25daa5f79c7e4606efb511511b4e6a2/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/2d57bece372faad05b928238719a8e20/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/ea353d2a-70aa-11e8-bd50-b80389a4e569/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/3970a236-765e-11e8-805c-4b67019fcfe4/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/b290155bcb01591d114f141d697037bc/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/ef5c474dc535c6ac6472e745bdfa158f/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/7ca3db317cf8d5fdb431e4c2598f8a57/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/1e479780fef883d72a98f76878fe219e/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/75098d2f9172865f65ef03fe324338ec/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/dd8a7925fdfd772bbfb804df667356fe/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/3048dcfa-7889-11e8-80be-6d32e182a3bc/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/7479ed16582baadec7f0bce15294a3a2/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/99baf91d3feca270fea6b984739fe5fc/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/8cf7fdeb06dfe28b43f3df250049bf94/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/92214dd4-788b-11e8-aeee-4d04c8ac6158/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/fcd2a7ba-7889-11e8-aeee-4d04c8ac6158/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/ca08e804ba9003e0e67bdec5ffe321f0/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/1ca1cfca-78b8-11e8-93cc-6d3beccdd7a3/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/1b5ee510-7653-11e8-b4b7-308400242c2e/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/0be4869aa1abe02674d5d991c3705252/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/725d7c92-78b4-11e8-aeee-4d04c8ac6158/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/4459d618-78b1-11e8-93cc-6d3beccdd7a3/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/9937cdbc-789c-11e8-aeee-4d04c8ac6158/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/9b506c97aca87a4ae824b0579221614c/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/1d1112bbc12d298a5da2f2d6481dd02f/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/a5a57b8e-78a2-11e8-80be-6d32e182a3bc/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/416d7b3c-78b4-11e8-80be-6d32e182a3bc/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/074a7cec1d83ae55124ef399db31cacd/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/116eda879d59d8a437e8304772c33918/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/0b7af337cceb7052a39809d2a450a12d/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/42b5bb3dde994318ceefe0f3bfcf3051/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/478b764f54855f58dff955256f980dc4/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/9e14e254b5189f9131caf2fd8a295ab2/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/ecb3dbad6070164b7a7880741c7190e2/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/0bad0da7e1a8e836caa68b35dd9e6d8e/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/b73b857b6b2dfff41a00be67a2205e4f/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/b18c04e8-78ae-11e8-93cc-6d3beccdd7a3/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/7190174e-78a9-11e8-93cc-6d3beccdd7a3/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/6cb508b71451c54cd0f40764fb0ca02e/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/71db5cba-7893-11e8-aeee-4d04c8ac6158/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/c09c8db9954feed96d5d37eebbf6f3d2/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/fa9218866b8c048b1c9a82f17ada1c18/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/aa0c691f9bc3fac8da940dd7010cd33f/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/1a54efd8-7893-11e8-aeee-4d04c8ac6158/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/98b1c458-789f-11e8-aeee-4d04c8ac6158/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/88b686a5-9dc3-41c3-92db-a8cdb572bc76/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/bf8406191cba9248925b4345cf52f857/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/74e9851e-787d-11e8-ac4e-421ef7165923/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/9781d7c0-7567-11e8-b4b7-308400242c2e/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/e77d5b8db57cbd3ca77529f287c92b95/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/c79983769899daf3ff392c466a2c6081/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/eaa97f888380cbc5db40a112df30d954/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/3fb90a59dcd180d25a6f33ec90a3c761/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/6cfcc000974a57ff928d4db3853f83c3/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/cad47f0c-78e5-11e8-93cc-6d3beccdd7a3/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/b77f02a4-7892-11e8-aeee-4d04c8ac6158/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/6685d693b4b3dbffebd21944c964c0c9/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/6b61b1ce38d5d854aad95ea12d5a31bc/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/6937364565b430af2af1a6d343548418/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/0a3dfac0-78ef-11e8-ac4e-421ef7165923/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/4ae6653c-78cf-11e8-ac4e-421ef7165923/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/15173d2a-7891-11e8-80be-6d32e182a3bc/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/d530a68ec8fa9558909972e019fc5b9a/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/11d168fde52af092c356d0836c04777c/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/2e96fec103c8ab461a467b5c21259a2d/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/f0958e0f200c3d9a1b6e53b938db6930/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/b7107a91e318f499bd1c9375c5113c69/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/e47e331b42335fde6b8097e52c974e6c/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/e4737d7a708b27f8a1d77400e99ee396/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/4dedc2bde956348879a0f25e23647fa8/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/6d547f80-7890-11e8-93cc-6d3beccdd7a3/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/19d55c15650f78e7ae3c9660c2f03e36/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/33372ab5cd5b8b4900e3579007b51f06/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/560a9882-6431-11e8-a69c-b944de66d9e7/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/4d1b513a-765b-11e8-9780-b1dd6a09b549/&platform=phone&followLinks=false",
        "https://rainbowapi-a.wpdigital.net/rainbow-data-service/rainbow/content-by-url.json?url=http://rainbowtool.wpprivate.com/pb/87510908-789f-11e8-80be-6d32e182a3bc/&platform=phone&followLinks=false"
    ]
    count = 0
    number = 1
    download_delay = 2
    time_str = time.strftime("%Y-%m-%d")
    timeArray = time.strptime(time_str, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))

    def parse(self, response):
        data = json.loads(response.body)
        title = data['title']
        pic_url = data['socialImage']
        app_name = '华盛顿邮报'
        author = ''
        describe = ''
        pic_more_url = pic_url
        home_url = 'https://rainbowapi-a.wpdigital.net/'
        crawlTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        category = data['omniture']['channel']
        publishedDate = data['lmt']
        publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(publishedDate)/1000))
        content = data['items']
        contentt = ''
        for i in range(len(content)):
            try:
                contentt += content[i]['content']
            except:
                contentt += ''
        content = contentt
        print "app名称", app_name
        # print "主图片url", pic_url
        # print "子图片url", pic_more_url
        # print "作者", author
        # print "详情页地址", response.url
        # print "所属类型", category
        print "标题", title
        # print "描述", describe
        print "内容", content
        # print "主url", home_url
        print "发布时间", publishedDate
        # print "爬取时间", crawlTime
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
        timeArray = time.strptime(publishedDate, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        if timeStamp >= self.timeStamp:
            publishedDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timeStamp)))
            item['publishedDate'] = publishedDate
        yield item


