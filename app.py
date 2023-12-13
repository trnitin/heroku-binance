# import sys
# import ctypes
from binance.enums import *
from binance.client import Client
import json
import config
# import win32api
# import time
# import math
from flask import Flask, request, jsonify
app = Flask(__name__)


# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False


# client = Client(config.API_KEY, config.API_SECRET)
# gt = client.get_server_time()
# aa = str(gt)
# bb = aa.replace("{'serverTime': ", "")
# aa = bb.replace("}", "")
# gg = int(aa)
# ff = gg-19798879
# uu = ff/1000
# yy = int(uu)
# tt = time.localtime(yy)
# if is_admin():
#     win32api.SetSystemTime(tt[0], tt[1], 0, tt[2], tt[3], tt[4], tt[5], 0)
# else:
#     # Re-run the program with admin rights
#     ctypes.windll.shell32.ShellExecuteW(
#         None, "runas", sys.executable, __file__, None, 1)


print(config.API_KEY)


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order",side,quantity,symbol)
        order = client.futures_create_order(
            symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order


# for i in range(1, 10):
#     local_time1 = int(time.time() * 1000)
#     server_time = client.get_server_time()
#     diff1 = server_time['serverTime'] - local_time1
#     local_time2 = int(time.time() * 1000)
#     diff2 = local_time2 - server_time['serverTime']
#     print("local1: %s server:%s local2: %s diff1:%s diff2:%s" %
#           (local_time1, server_time['serverTime'], local_time2, diff1, diff2))
#     time.sleep(2)


@app.route('/')
def hello_world():
    return 'Hello, World'


@app.route('/test')
def whatever():
    return 'Hello, Worlssfad'


@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return{
            "code": "error",
            "message": "Invalid passphrase"
        }
    print(data['ticker'])
    # print(data['bar'])

    # info = client.get_symbol_info('BTCUSDT_210924PERP')
    # print(info)
    side = data['strategy']['order_action'].upper()
    tick = data['ticker']
    quantity = data['strategy']['order_contracts']
    formatQuantity = format(quantity, '.5')
    print(formatQuantity)
    # print(formatQuantity)
    # if(data['strategy']['order_id'] == "short" or data['strategy']['order_id'] == "exit short" ):
    # formatQuantity = '0.002'

    order_response = order(side, formatQuantity, 'BTCUSDT')
    # order_response = order(
    #     symbol=tick,
    #     type='MARKET',
    #     timeInForce='GTC',
    #     side=side,
    #     quantity=quantity
    # )
    print(side)
    print(order_response)
    # btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
    # # print full output (dictionary)
    # print(btc_price)
    if order_response:
        return {
            "code": "success",
        }
    else:
        print("order failed")
        return {
        "code": "error",
        "message": "order"
       }   
