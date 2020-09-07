import base64
import hashlib
import hmac
import datetime
import urllib
import urllib.parse
import urllib.request
import json



def create_sign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')

    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature


class Signature:
    def __init__(self, request_path, host, access_key, secret_key):
        self.request_path = request_path
        self.host = host
        self.access_key = access_key
        self.secret_key = secret_key

    def get_methods(self, parameter):
        method = 'GET'
        parameter = parameter
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        parameter.update({'AccessKeyId': self.access_key,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp})
        host_name = urllib.parse.urlparse(self.host).hostname
        host_name = host_name.lower()
        parameter['Signature'] = create_sign(
            parameter, method, host_name, self.request_path, self.secret_key
        )
        return parameter

    def post_methods(self):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': self.access_key,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}
        host_name = urllib.parse.urlparse(self.host).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = create_sign(
            params_to_sign, method, host_name, self.request_path, self.secret_key)
        # print(json.dumps(params_to_sign))
        url = self.host + self.request_path + '?' + urllib.parse.urlencode(params_to_sign)
        return url


