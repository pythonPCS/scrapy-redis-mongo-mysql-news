import time
import requests
url = 'https://news.baidu.com/sn/api/feed_feedlist?pd=newsplus&os=android&sv=7.1.2.0&from=app&_uid=g8SNu0um2ulx8HuKlu2ci0is2tl5aB8o_iSW8_uNSiiOO2tgga2qi_u62ig8uvihA&_ua=_aBDCgaH-i46ywoUfpw1z4aBsiz5aX8D4a2AiqqHB&_ut=5yG_YtM1vC_bhvhJgODpOYhuA&_from=1019026r&_cfrom=1019026r&_network=1_0&cen=uid_ua_ut'
params = {
     "ln": "20",
    "os": "android",
    "display_time": "1528777824421",
    "from": "app",
    "ver": "6",
    "withtoppic": "0",
    "network": {"wifi_aps":{"ap_mac":"70:05:14:7d:2a:5f","is_connected":True,"ap_name":"","rssi":-33},"ipv4":"172.18.173.37","cellular_id":"-1","operator_type":99,"connection_type":100},
    "pd": "newsplus",
    "user_category": "",
    "cuid": "3ADAC23BAEBDC750FF38B3810FA334A1|918510050145753",
    "action": "0",
    "device": {"screen_size":{"height":1184,"width":768},"model":"Nexus 4","udid":{"android_id":"6140f143b1a4dd1e","mac":"70:05:14:7d:2a:5f","imei":"357541050015819"},"vendor":"LGE","device_type":1,"os_version":{"micro":0,"minor":4,"major":4},"os_type":1},
    "sv": "7.1.2.0",
    "gps": '{"timestamp":1528790165,"longitude":"116.365275","coordinate_type":3,"latitude":"39.969771"}',
    "mid": "357541050015819_70:05:14:7d:2a:5f",
    "loc_ll": "116.365275,39.969771",
    "wf": "1",
}

data = requests.post(url, data=params)
print data.content