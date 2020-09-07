from services import open_api_service
from services import config
from sampal import order_place
import time
from services import wirte_log


order_place.order_place()
time.sleep(2)
res = open_api_service.Order().market_depth(config.symbol, config.typ, 0)


class OrderTest:

    def limit(self, side, data):
        """
        if side = buy or sell
        if data = 0 时限价挂单
        if data = 1 时限价全部成交
        if data = 2 时限价部分成交
        if data = 3 时限价全部撤单
        if data = 4 时限价部分成交撤单
        :param side:
        :param data:
        :return:
        """
        if side == 'SELL':
            if data == 0:
                """
                限价卖单挂单
                """
                params = {
                    "side": side, "type": 1, "volume": 1, "symbol": config.symbol,
                    "price": round(res['data']['tick']['bids'][0][0] + 0.0001, 4)}
                before_eos = open_api_service.Order().account_balance(1, config.eos)
                before_usd = open_api_service.Order().account_balance(1, config.usd)
                wirte_log.return_log(u'期初资产eos-usdt', before_eos, before_usd)
                order_id = open_api_service.Order().order_place(params, 1)
                time.sleep(1)
                end_eos = open_api_service.Order().account_balance(1, config.eos)
                end_usd = open_api_service.Order().account_balance(1, config.usd)
                wirte_log.return_log(u'期末资产eos-usdt', before_eos, before_usd)
                assert float(before_eos[0])-float(end_eos[0]) == float(end_eos[1]) - float(before_eos[1])
                assert float(before_usd[0]) - float(end_usd[0]) == float(end_usd[1]) - float(before_usd[1])
                detail = {"order_id": order_id['data']['order_id'], "symbol": config.symbol}
                res_detail = open_api_service.Order().order_detail(detail, 1)
                assert res_detail['data']['order_info']['status'] == 0
                # print(res_detail)
            elif data == 1:
                """
                限价卖单全部成交
                """
                params = {
                    "side": side, "type": 1, "volume": res['data']['tick']['bids'][0][1], "symbol": config.symbol,
                    "price": res['data']['tick']['bids'][0][0]}
                # print(params)
                before_eos = open_api_service.Order().account_balance(1, config.eos)
                before_usd = open_api_service.Order().account_balance(1, config.usd)
                print("before_usd:{}".format(before_usd))
                wirte_log.return_log(u'期初资产eos-usdt', before_eos, before_usd)
                order_id = open_api_service.Order().order_place(params, 1)
                time.sleep(6)
                end_eos = open_api_service.Order().account_balance(1, config.eos)
                end_usd = open_api_service.Order().account_balance(1, config.usd)
                print("end_usd:{}".format(end_usd))
                wirte_log.return_log(u'期末资产eos-usdt', before_eos, before_usd)
                # 期初eos - 期末eos = 卖出量
                assert float(before_eos[0]) - float(end_eos[0]) == res['data']['tick']['bids'][0][1]
                # 期末冻结eos -期初冻结eos = 0
                assert float(end_eos[1]) - float(before_eos[1]) == float(0)
                # 期末usdt = 期初usdt + 卖出量*卖出价格 - 卖出量*卖出价格*手续费率
                assert float(end_usd[0]) == round(float(before_usd[0]) + float(res['data']['tick']['bids'][0][1]* res['data']['tick']['bids'][0][0]) -float(res['data']['tick']['bids'][0][1]* res['data']['tick']['bids'][0][0] *0.1),2)
                # 期末冻结usdt - 期末冻结usdt = 0
                assert float(end_usd[1]) - float(before_usd[1]) == float(0)
                detail = {"order_id": order_id['data']['order_id'], "symbol": config.symbol}
                res_detail = open_api_service.Order().order_detail(detail, 1)
                assert res_detail['data']['order_info']['status'] == 2
            elif data == 2:
                """
                限价卖单部分成交
                """
                params = {
                    "side": side, "type": 1, "volume": res['data']['tick']['bids'][0][1], "symbol": config.symbol,
                    "price": res['data']['tick']['bids'][0][0]}
                # print(params)
                before_eos = open_api_service.Order().account_balance(1, config.eos)
                before_usd = open_api_service.Order().account_balance(1, config.usd)
                print("before_usd:{}".format(before_usd))
                wirte_log.return_log(u'期初资产eos-usdt', before_eos, before_usd)
                order_id = open_api_service.Order().order_place(params, 1)
                time.sleep(6)
                end_eos = open_api_service.Order().account_balance(1, config.eos)
                end_usd = open_api_service.Order().account_balance(1, config.usd)
                print("end_usd:{}".format(end_usd))
                wirte_log.return_log(u'期末资产eos-usdt', before_eos, before_usd)
                # 期初eos - 期末eos = 卖出量
                assert float(before_eos[0]) - float(end_eos[0]) == res['data']['tick']['bids'][0][1]
                # 期末冻结eos -期初冻结eos = 0
                assert float(end_eos[1]) - float(before_eos[1]) == float(0)
                # 期末usdt = 期初usdt + 卖出量*卖出价格 - 卖出量*卖出价格*手续费率
                assert float(end_usd[0]) == round(float(before_usd[0]) + float(
                    res['data']['tick']['bids'][0][1] * res['data']['tick']['bids'][0][0]) - float(
                    res['data']['tick']['bids'][0][1] * res['data']['tick']['bids'][0][0] * 0.1), 2)
                # 期末冻结usdt - 期末冻结usdt = 0
                assert float(end_usd[1]) - float(before_usd[1]) == float(0)
                detail = {"order_id": order_id['data']['order_id'], "symbol": config.symbol}
                res_detail = open_api_service.Order().order_detail(detail, 1)
                assert res_detail['data']['order_info']['status'] == 2
            elif data == 3:
                """
                限价卖单完全撤单
                """
                params = {
                    "side": side, "type": 1, "volume": 1, "symbol": config.symbol,
                    "price": round(res['data']['tick']['bids'][0][0] + 0.0001, 4)}
                # print(params)
                response = open_api_service.Order().order_place(params, 1)
                p = {"order_id": response['data']['order_id'], "symbol": config.symbol}
                open_api_service.Order().order_cancel(p, 1)
            elif data == 4:
                """
                限价卖单部分成交撤单
                """
                params = {
                    "side": side, "type": 1, "volume": 1, "symbol": config.symbol,
                    "price": round(res['data']['tick']['bids'][0][0] + 0.0001, 4)}
                # print(params)
                response = open_api_service.Order().order_place(params, 1)
                p = {"order_id": response['data']['order_id'], "symbol": config.symbol}
                open_api_service.Order().order_cancel(p, 1)



        # if side == 'BUY':
        #     pass



    # def post_only(self):
    #     pass
    # def market(self):
    #     pass
if __name__ == '__main__':
    OrderTest().limit('SELL',0)