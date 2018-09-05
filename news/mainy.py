# #coding=utf-8
import requests
import json

url = 'http://www.toutiao.com/api/pc/focus/'
wbdata = requests.get(url).text

data = json.loads(wbdata.decode('utf-8'))
news = data['data']['pc_feed_focus']

for n in news:
  title = n['title']
  img_url = n['image_url']
  url = n['media_url']
  print url,title,img_url

