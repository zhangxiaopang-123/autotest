from services import read_yaml
import os

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_name = 'test'
symbol = 'trxusdt'
typ = 'step0'
eos = 'zhf'
usd = 'btc'


def environment(env, sex):
    if env == env_name:
        key = read_yaml.read_()[env_name]['access-key'].split(',')[0]
        secret = read_yaml.read_()[env_name]['secret-key'].split(',')[0]
        api_key = read_yaml.read_()[env_name]['access-key'].split(',')[1]
        secret_key = read_yaml.read_()[env_name]['secret-key'].split(',')[1]
        host = read_yaml.read_()[env_name]['host']
        _host = read_yaml.read_()[env_name]['_host']
        # print(api_key)
        if sex == 0:
            return key, secret, host, _host
        else:
            return api_key, secret_key, host, _host


if __name__ == '__main__':
    environment('test')

