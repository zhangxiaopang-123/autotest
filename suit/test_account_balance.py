
from services.wbf_signature import Signature
import time
from services.config import environment
from services import config
import pytest


class TestOpenApi:
    # @pytest.mark.parametrize('api_key,time,sign')
    def test_balance(self):
        api_key = environment(config.env_name,1)[0]
        secret_key = environment(config.env_name,1)[1]
        host = environment(config.env_name,1)[-2]
        # print(host)
        p = {}
        tie = int(time.time())
        request_path = '/open/api/user/account'
        result = Signature(api_key, secret_key, tie).get_sign(request_path, host,p)
        print(result)
        assert result['msg'] == 'suc' and result['code'] == '0'


if __name__ == '__main__':
    pytest.main(['-s', ''])