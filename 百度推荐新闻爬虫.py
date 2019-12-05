#                    _ooOoo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                   O\  =  /O
#                ____/`---'\____
#              .'  \\|     |//  `.
#             /  \\|||  :  |||//  \
#            /  _||||| -:- |||||-  \
#            |   | \\\  -  /// |   |
#            | \_|  ''\---/''  |   |
#            \  .-\__  `-`  ___/-. /
#          ___`. .'  /--.--\  `. . __
#       ."" '<  `.___\_<|>_/___.'  >'"".
#      | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#      \  \ `-.   \_ __\ /__ _/   .-` /  /
# ======`-.____`-.___\_____/___.-`____.-'======
#                    `=---='
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#             佛祖保佑       永无BUG

import requests
from lxml import etree
import time
import random
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
    'Cookie': 'BAIDUID=911B377F5CDFF4E6944951033E69A164:FG=1; BIDUPSID=911B377F5CDFF4E6944951033E69A164; PSTM=1548689949; BD_UPN=12314753; MCITY=-268%3A; sugstore=0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=FQOS1mWnFjV1A3SldNdTNjeFREaHNYVHpGRWdRdlMyTmp2d0QxTzR0akpsOTlkRVFBQUFBJCQAAAAAAAAAAAEAAABUN0cMVG9temt5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMkKuF3JCrhdbT; pgv_pvi=3794231296; BD_HOME=1; H_PS_PSSID=1454_21087_29568_29220_26350',
}

url = 'https://www.baidu.com/home/pcweb/data/mancardwater'

for page in range(1,5):
    print('page:',page)
    params = {
        'id': '2',
        'offset': page,
        'sessionId': '15723976647793',
        'crids': '',
        'version': '',
        'pos': '9',
        'newsNum': '9',
        'blacklist_timestamp': '0',
        'indextype': 'manht',
        '_req_seqid': '0xe958577c000872a0',
        'asyn': '1',
        't': int(time.time()*1000),
        'sid': '1454_21087_29568_29220_26350',
    }
    response = requests.get(url,params=params,headers=headers)
    print('status code:',response.status_code)
    data = response.text
    pat_1 = re.compile(r'"html" : "(.*?)","isEnd"')
    data = pat_1.search(data).group(1)
    data = data.replace('&quot;','')
    data = data.replace(r'\x22','"') # 替换成"

    data = data.replace('s-news-list-wrapper','"s-news-list-wrapper"')
    data = data.replace('s-title-yahei','"s-title-yahei"')
    data = data.replace('del','"del"')
    data = data.replace('s-pic-content','"s-pic-content"')
    data = data.replace('item-img-wrap','"item-img-wrap"')
    data = data.replace('s-news-img','"s-news-img"')
    data = data.replace('class=from','class="from"')
    data = data.replace('src-net','"src-net"')
    data = data.replace('src-time','"src-time"')
    data = data.replace('dustbin','"dustbin"')
    data = data.replace('s-pic-content-own','"s-pic-content-own"')
    data = data.replace('s-block-container','"s-block-container"')
    data = data.replace('s-block-container-own','"s-block-container-own"')
    data = data.replace('s-text-content','"s-text-content"')

    data = data.replace(r'\/','/')
    print(data)
    html = etree.HTML(data)
    ls = html.xpath('//div[contains(@class,"s-news-item")]')
    print('len:',len(ls))
    for each in ls:
        title = each.xpath('.//h2/a/@title')[0]
        print('title:',title)
        detail_url = each.xpath('.//h2/a/@href')[0]
        print('detail_url:', detail_url)
        src_net = each.xpath('.//span[@class="src-net"]/a/text()')
        if len(src_net)>0:
            src_net = src_net[0]
        else:
            src_net = '无'
        print('src_net:', src_net)
        src_time = each.xpath('.//span[@class="src-time"]/text()')[0]
        print('src time:',src_time)
        print('='*600)
    time.sleep(random.random()*2)

