import requests
from services import config
import os
import json

url = 'https://api.sxfaawu.cn/api/futureQuot/queryCandlestick?symbol=100000&range=2419200000'
res = requests.get(url).json()['data']['lines']
print(res)
print(len(res))
# print('http-res:{}'.format(res))
path = os.path.join(config.basedir, 'json_directory/kline.json')
with open(path, 'r', encoding='utf-8') as f:
    mine = eval(json.loads(f.read()))
    # print(type(mine))
    # print(mine['data'])
    p = mine['data']
    d = []
    for key in range(0, len(p)):
        data = p[key]['id'] * 1000
        # print(data)
        p[key]['id'] = data
        l = [
            p[key].get('id'), p[key].get('amount'), p[key].get('open'),
            p[key].get('close'), p[key].get('high'), p[key].get('low')
        ]
        d.append(l)
    # print(d)
    for s in range(0, len(d)):
        # print(d[s][0])
        for t in range(0, len(res)):
            # pass
            # print(res[t][0])
            # if int(d[s][0]) == int(res[t][0]):
            if int(d[s][0]) == int(res[t][0]) and float(d[s][1]) == float(res[t][-1]) \
                    and float(d[s][2]) == float(res[t][1]) and float(d[s][3]) == float(res[t][-2])\
                    and float(d[s][4]) == float(res[t][2]) and float(d[s][5]) == float(res[t][-3]):
                print(s)
                print('ws-数据', d[s])
                print('http-数据', res[t])
            else:
                pass
                # print('ws-数据', d[s])
                # print('http-数据', res[t])









