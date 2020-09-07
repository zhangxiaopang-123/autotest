from services import open_api_service
from services import config
import random,time


def order_place():
    """
    执行摆盘操作
    :return:
    """
    last_price = open_api_service.Order().lastprice(config.symbol, 0)
    res = open_api_service.Order().market_depth(config.symbol, config.typ, 0)
    # print(res)
    if res['data']['tick'] == {}:
        for i in range(1, 21):
            params = {
                "side": "SELL", "type": 1, "volume": i, "symbol": config.symbol,
                "price": last_price + round(random.random(), 4)}
            time.sleep(0.1)
            open_api_service.Order().order_place(params, 0)
        for i in range(1, 21):
            params = {
                "side": "BUY", "type": 1, "volume": i, "symbol": config.symbol,
                "price": abs(last_price - round(random.random(), 4))}
            time.sleep(0.1)
            open_api_service.Order().order_place(params, 0)
    else:
        if res['data']['tick']['asks'] is None:
            for i in range(1, 21):
                params = {
                    "side": "SELL", "type": 1, "volume": i, "symbol": config.symbol,
                    "price": last_price + round(random.random(), 4)}
                time.sleep(0.1)
                open_api_service.Order().order_place(params, 0)

        if res['data']['tick']['bids'] is None:
            for i in range(1, 21):
                params = {
                    "side": "BUY", "type": 1, "volume": i, "symbol": config.symbol,
                    "price": abs(last_price - round(random.random(), 4))}
                time.sleep(0.1)
                open_api_service.Order().order_place(params, 0)





if __name__ == '__main__':
    order_place()