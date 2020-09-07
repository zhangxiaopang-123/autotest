from services import open_api_service
from services import config
import random,time


def order_place():
    """
    执行摆盘操作
    :return:
    """
    side = ['SELL', 'BUY']
    typ = [1, 2, 3]
    for s in range(0, len(side)):
        for t in range(0, len(typ)):
            for i in range(1, 100):
                if typ[t] == 2:
                    params = {
                        "side": side[s], "type": typ[t], "volume": 1, "symbol": config.symbol}
                else:
                    params = {
                        "side": side[s], "type": typ[t], "volume": 1, "symbol": config.symbol,
                        "price": i}
                time.sleep(0.1)
                open_api_service.Order().order_place(params, 0)


if __name__ == '__main__':
    order_place()