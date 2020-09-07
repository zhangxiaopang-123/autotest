
import json
import zlib
import websocket
from services import config
import os
try:
    import thread
except ImportError:
    import _thread as thread
import time
# 24小时k线数据
# data = [json.dumps({"event": "sub", "params": {"channel": "review.future"}})]
# 实时成交数据
# data = [json.dumps({"event": "sub", "params": {"channel": "market_btcusdt100000.swap_trade_ticker"}})]
# 请求历史成交
# data = [json.dumps({"event":"req","params":{"channel":"market_eosusdt100002.swap_trade_ticker"}})]
# 订阅盘口
# data = [json.dumps({"event":"sub","params":{"channel":"market_eosusdt100002.swap_depth_step0"}})]
# 订阅1mink线
# data = [json.dumps({"event": "sub", "params": {"channel": "market_btcusdt100000.swap_kline_15min"}})]
# 订阅1min历史k线
data = [json.dumps({"event": "req", "params": {"channel": "market_btcusdt100000.swap_kline_60min"}})]


def on_message(ws, message):
    ws_result = str(zlib.decompressobj(31).decompress(message), encoding="utf-8")
    print(ws_result)
    # print(type(ws_result))
    if json.loads(ws_result)['status'] == 'ok':
        path = os.path.join(config.basedir, 'json_directory/kline.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(ws_result, f)
    if ws_result.find('ping') > 0 and ws_result.find('heartbeat') <= 0:
        pong_data = {"pong": json.loads(ws_result)['ping']}
        ws.send(json.dumps(pong_data))
        print('向服务器发pong')


def on_error(ws, error):
    err_result = error
    print(err_result)


def on_close(ws):
    ws.close()
    print("### closed ###")


def on_open(ws):
    def run(*args):
        for sub in data:
            ws.send(sub)
            # time.sleep(1)
    thread.start_new_thread(run, ())


def _socket():
    prd_pro_ws = 'ws://wsnx.v3.wbfexchina.top/kline-api/ws'
    # prd_pro_ws = 'wss://beta-ws.wbfex.info:32004/kline-api/ws'
    # prd_pro_ws = 'wss://ws.wbf.live/kline-api/ws'
    url_ws = prd_pro_ws
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url=url_ws,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                )
    ws.on_open = on_open
    ws.run_forever(ping_timeout=3)


if __name__ == "__main__":
    _socket()
