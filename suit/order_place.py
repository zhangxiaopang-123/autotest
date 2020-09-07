
from services.wbf_signature import Signature
import time
from services.config import environment
from services import config
import pytest


class TestPlaceApi:
    # @pytest.mark.parametrize('api_key,time,sign')
    def test_order(self, p):
        api_key = environment(config.env_name)[0]
        secret_key = environment(config.env_name)[1]
        host = environment(config.env_name)[-2]
        # print(host)
        tie = time.time()
        request_path = '/open/api/create_order'
        result = Signature(api_key, secret_key, tie).post_sign(p, request_path, host)
        print(result)
        assert result['msg'] == 'suc' and result['code'] == '0'


if __name__ == '__main__':
    pytest.main(['-s', ''])