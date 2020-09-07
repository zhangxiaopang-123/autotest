
import json
import time
import hashlib


class Sign:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def ign(self, dic):
        tmp = ''
        for key in sorted(dic.keys()):
            tmp += key + str(dic[key])
        tmp += self.secret_key
        digest = hashlib.sha256(tmp.encode(encoding='utf-8')).hexdigest()
        return digest

    def now_time(self):
        now_time = int(time.time())
        return now_time

    def send_data(self):
        p = {"token": self.access_key, "time": str(self.now_time())}
        params = {"action": "req", "ch": "auth", "params": {
            "token": self.access_key, "time": str(self.now_time()), "sign": self.ign(p)}}
        print('验签参数：{}'.format(params))
        return json.dumps(params)






