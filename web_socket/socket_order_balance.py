
import zlib
import json
import websocket
from services import config
import time
from web_socket import socket_methods

try:
    import thread
except ImportError:
    import _thread as thread
data = [json.dumps({"action": "sub", "ch": "orders#zhfusdt"})]
# data = [json.dumps({"action": "sub", "ch": "accounts.update#usdt"})]

access_key = config.environment(config.env_name)[0]
secret_key = config.environment(config.env_name)[1]
_host = config.environment(config.env_name)[-1]
url = _host + '/ws'
# print(access_key, secret_key)


def on_message(ws, message):
    ws_result = str(zlib.decompressobj(31).decompress(message), encoding="utf-8")
    print(ws_result)
    if ws_result.find('ping') > 0 and ws_result.find('heartbeat') <= 0:
        pong_data = {"pong": json.loads(ws_result)['ping']}
        ws.send(json.dumps(pong_data))
        print('向服务器发pong:{}'.format(pong_data))


def on_error(ws, error):
    err_result = error
    print(err_result)


def on_close(ws):
    ws.close()
    print("### closed ###")


def on_open(ws):
    ws.send(socket_methods.Sign(access_key, secret_key).send_data())
    def run(*args):
        for sub in data:
            ws.send(sub)
            time.sleep(1)
    thread.start_new_thread(run, ())



def _socket():
    # prd_pro_ws = 'ws://wsnx.v3.wbfexchina.top/kline-api/ws'
    # prd_pro_ws = 'wss://beta-ws.wbfex.info:32004/kline-api/ws'
    # url_ws = prd_pro_ws
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url=url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                )
    ws.on_open = on_open
    ws.run_forever(ping_timeout=3)


if __name__ == "__main__":
    _socket()
