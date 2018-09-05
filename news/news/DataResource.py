#-*- coding: utf-8 -*-
from news.Configuration import Configuration
# import pymysql

class TransportData():
    pass
    # @staticmethod
    # def transport_data(app_name,pic_url,pic_more_url,writer,content_url,content_type,title,summary,content,home_url,pubTime,crawlTime):
    #     try:
    #         conn = pymysql.connect(host=Configuration.host, user=Configuration.user, passwd=Configuration.passwd,
    #                                db=Configuration.db, charset="utf8")
    #         cursor = conn.cursor()
    #         sql_content = "insert into news_info(app_name,pic_url,pic_more_url,writer,content_url,content_type,title,summary,content,home_url,pubTime,crawlTime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #         cursor.execute(sql_content,(app_name,pic_url,pic_more_url,writer,content_url,content_type,title,summary,content,home_url,pubTime,crawlTime))
    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #         print "success!!!!!!!!!!!!!!!!!!!!!"
    #     except pymysql.Error, e:
    #         print "Mysql Error"
    #
    # @staticmethod
    # def getData(app_name):
    #     existing_title = []
    #     try:
    #         conn =pymysql.connect(host=Configuration.host, user=Configuration.user, passwd=Configuration.passwd,
    #                               db=Configuration.db, charset="utf8")
    #         cursor = conn.cursor()
    #         sql_content = "select title from news_info where app_name='%s'"%app_name
    #         cursor.execute(sql_content)
    #         data = cursor.fetchall()
    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #         for name in data:
    #             existing_title.append(name[0].encode("utf-8"))
    #         del data
    #         return existing_title
    #     except pymysql.Error, e:
    #         print "Mysql Error"
    #
    # @staticmethod
    # def getMaxPubtime(app_name):
    #     try:
    #         conn = pymysql.connect(host=Configuration.host, user=Configuration.user, passwd=Configuration.passwd,
    #                                db=Configuration.db, charset="utf8")
    #         cursor = conn.cursor()
    #         sql_content = "select MAX(pubTime) from news_info WHERE app_name = %s"
    #         cursor.execute(sql_content, app_name)
    #         data = cursor.fetchall()
    #         print data
    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #         for name in data:
    #            max_pubTime = name[0]
    #         del data
    #         return max_pubTime
    #     except pymysql.Error, e:
    #         print "Mysql Error"
