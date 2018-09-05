#-*- coding: utf-8 -*-
from scrapy.spider import Spider
import scrapy
import sys
import json,time,re
from news.items import NewsItem
import random

reload(sys)
sys.setdefaultencoding('utf8')

class tengxun(Spider):
    name = 'tengxun'
    start_urls = [
        'https://www.baidu.com'
    ]

    def parse(self, response):
        a = self.suiji1()
        b = self.suiji2()
        c = self.suiji3()
        d = self.suiji4()
        e = self.suiji5()
        # STR = [chr(i) for i in range(65, 91)]  # 65-91对应字符A-Z
        # str = [chr(i) for i in range(97, 123)]  # a-z
        # number = [chr(i) for i in range(48, 58)]  # 0-9
        # a = random.shuffle(str)
        # b = random.shuffle(STR)
        # c = random.shuffle(number)
        # print a
        # print b
        # print c
        num = str(a) + '-' + str(b) +'-' + c +'-' + d +'-' + e
        print num
        canshu = 'appver=19_android_5.6.02&cgi=searchMore&devid=352584064289389&qn-rid=%s&secret=qn123456'%num
        print canshu
        key = self.md5(canshu)
        url = 'https://r.inews.qq.com/search?query=习近平&is_special_device=0&omgbizid=e32dc9fbfa5d254c5f3b7adeebc4c57157c40050213506&network_type=wifi&store=153&extinfo=&hw=LGE_Nexus5&orig_store=153&global_session_id=1528252581892&activefrom=icon&mac=64:89:9a:4e:e8:08&origin_imei=352584064289389&qqnetwork=wifi&islite=0&rom_type=&lite_version=&real_device_width=2.44&imsi_history=460078106345962&pagestartfrom=icon&sceneid=&dpi=480.0&apptype=android&screen_width=1080&real_device_height=4.33&is_chinamobile_oem=0&patchver=5602&global_info=0|1|1|1|1|8|4|1|2|6|1|2|1|2|0|0|2|&adcode=110108&imsi=460078106345962&mid=08caf3a626732fca43979e630a77e2e5855b9474&isoem=0&screen_height=1776&Cookie=lskey%3D;skey%3D;uin%3D;%20luin%3D;logintype%3D0;%20main_login%3D;%20&omgid=91c0f3a78f61b1429c0acea8f8480f3b8182001021301f&uid=def5d0d299d3042d&devid=352584064289389&appver=19_android_5.6.02&qn-rid=' + num + '&qn-sig=' + key
        print url
        params = {
            "Cookie":"lskey=;skey=;uin=; luin=;logintype=0; main_login=;",
            "appver":"19_android_5.6.02",
            "Referer":"http://inews.qq.com/inews/android/",
            "User-Agent":"%E8%85%BE%E8%AE%AF%E6%96%B0%E9%97%BB5602(android)",
            "Host":"r.inews.qq.com",
            "Connection":"Keep-Alive",
            "Accept-Encoding":"gzip"
        }
        import requests
        data =requests.get(url, params=json.dumps(params))
        print data.content

    def md5(self,page):
        import hashlib
        m = hashlib.md5()
        m.update(page)
        return m.hexdigest()

    def suiji1(self):
        import random
        auth = ""  # 定义全局验证码变量
        for i in range(0, 8):  # 定义循环4次，形成4位验证码。
            current = random.randint(0, 9)  # 定义一个随机0-4的一个范围，去猜i 的值。
            if current == i:  # 如果current 和i 的值一样
                current_code = random.randint(0, 9)  # 生成一个随机的数字
            else:  # 如果current和i 的值不一样
                current_code = chr(random.randint(97, 120))  # 生成一个随机的字母，这里一定要主义chr（）转换一下。
            auth += str(current_code)  # 将每次随机生成的值赋值给auth
        return auth

    def suiji2(self):
        import random
        auth = ""  # 定义全局验证码变量
        for i in range(0, 4):  # 定义循环4次，形成4位验证码。
            # current = random.randint(0, 4)  # 定义一个随机0-4的一个范围，去猜i 的值。
            # if current == i:  # 如果current 和i 的值一样
            current_code = random.randint(0, 9)  # 生成一个随机的数字
            # else:  # 如果current和i 的值不一样
            # current_code = chr(random.randint(97, 120))  # 生成一个随机的字母，这里一定要主义chr（）转换一下。
            # auth += str(current_code)  # 将每次随机生成的值赋值给auth
            auth += str(current_code)
        return auth

    def suiji3(self):
        import random
        auth = ""  # 定义全局验证码变量
        for i in range(0, 4):  # 定义循环4次，形成4位验证码。
            # current = random.randint(0, 4)  # 定义一个随机0-4的一个范围，去猜i 的值。
            # if current == i:  # 如果current 和i 的值一样
            #     current_code = random.randint(0, 9)  # 生成一个随机的数字
            # else:  # 如果current和i 的值不一样
            current_code = chr(random.randint(97, 120))  # 生成一个随机的字母，这里一定要主义chr（）转换一下。
            # auth += str(current_code)  # 将每次随机生成的值赋值给auth
            auth += current_code
        return auth

    def suiji4(self):
        import random
        auth = ""  # 定义全局验证码变量
        for i in range(0, 4):  # 定义循环4次，形成4位验证码。
            # current = random.randint(0, 4)  # 定义一个随机0-4的一个范围，去猜i 的值。
            # if current == i:  # 如果current 和i 的值一样
            #     current_code = random.randint(0, 9)  # 生成一个随机的数字
            # else:  # 如果current和i 的值不一样
            current_code = chr(random.randint(97, 120))  # 生成一个随机的字母，这里一定要主义chr（）转换一下。
            # auth += str(current_code)  # 将每次随机生成的值赋值给auth
            auth += current_code
        return auth

    def suiji5(self):
        import random
        auth = ""  # 定义全局验证码变量
        for i in range(0, 12):  # 定义循环4次，形成4位验证码。
            # current = random.randint(0, 4)  # 定义一个随机0-4的一个范围，去猜i 的值。
            # if current == i:  # 如果current 和i 的值一样
            #     current_code = random.randint(0, 9)  # 生成一个随机的数字
            # else:  # 如果current和i 的值不一样
            current_code = chr(random.randint(97, 120))  # 生成一个随机的字母，这里一定要主义chr（）转换一下。
            # auth += str(current_code)  # 将每次随机生成的值赋值给auth
            auth += current_code
        return auth
