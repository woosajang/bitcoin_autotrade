import time
import pyupbit
import datetime

access = "S7EQC8OdSCSqDeQz8xFozCOHw2DW7qPPKu1qp1vx"
secret = "ozCbzFCxakxVCx8htKqgWI6FxLdnGsjKSIfluGmE"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

coin_list = ["KRW-BTC", "KRW-XEC", "KRW-KNC", "KRW-AERGO", "KRW-GLM", "KRW-XRP","KRW-WAVES","KRW-SAND","KRW-MBL"] #8
coin_list_others = ["KRW-CHZ",  "KRW-JST", "KRW-ATOM", "KRW-ICX", "KRW-OMG", "KRW-SBD"] #5
k_list = [0.7, 0.7, 0.5, 0.5, 0.5,0.5, 0.5,0.6,0.5 ]
k_list_others = [0.9, 0.8, 0.8, 0.5,0.7, 0.7, 0.5]
rate_list = [0.6995, 0.2995, 0.2995, 0.2995, 0.2995, 0.2995, 0.2995, 0.2995, 0.2995]
rate_list_others = [0.1995,0.1995,0.1995,0.1995,0.1995,0.1995]
i_list =[]
ik_list = []
i_list_others =[]
bbk = []

krw = get_balance("KRW")
krw_buy = get_balance("KRW")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)


        if start_time < now < end_time - datetime.timedelta(seconds=1800):
            #대형주

            for c in range(0,len(coin_list)):
                target_price = get_target_price(coin_list[c],k_list[c])
                current_price = get_current_price(coin_list[c])
                if target_price < current_price and coin_list[c] not in i_list :
                    bbk.append(coin_list[c])

                # print(coin_list[c], target_price, current_price)
                if target_price < current_price and coin_list[c] not in i_list and krw_buy > 5000 and bbk.count(coin_list[c]) > 100:
                    if krw_buy < krw *0.21:
                        oder_krw = krw_buy
                    else:
                        oder_krw = krw * rate_list[c]
                    upbit.buy_market_order(coin_list[c], oder_krw)
                    print(f"{coin_list[c]} 매수합니다")
                    time.sleep(10)
                    krw_buy = get_balance("KRW")
                    i_list.append(coin_list[c])
                    ik_list.append(k_list[c])

            #개잡주

            for o in range(0,len(coin_list_others)):
                target_price_others = get_target_price(coin_list_others[o],k_list_others[o])
                current_price_others = get_current_price(coin_list_others[o])
                if target_price_others < current_price_others and coin_list_others[o] not in i_list :
                    bbk.append(coin_list_others[o])

                # print(coin_list_others[o], target_price_others, current_price_others)
                if target_price_others < current_price_others and coin_list_others[o] not in i_list_others and krw_buy  > 5000 and bbk.count(coin_list_others[o]) > 100:
                    if krw_buy < krw *0.11:
                        oder_krw = krw_buy
                    else:
                        oder_krw = krw * rate_list_others[o]
                    upbit.buy_market_order(coin_list_others[o], oder_krw)
                    print(f"{coin_list_others[o]} 매수합니다")
                    time.sleep(10)
                    krw_buy = get_balance("KRW")
                    i_list_others.append(coin_list_others[o])


            # 조기 매도

            for s in range(0,len(i_list)):
                target_price_sell = get_target_price(i_list[s],ik_list[s])
                current_price_sell = get_current_price(i_list[s])
                coin = get_balance(i_list[s][4:])
                if i_list[s] == "KRW-BTC":
                    profit = 1.03
                else:
                    profit = 1.05
                if target_price_sell*profit < current_price_sell and coin > 0:
                    upbit.sell_market_order(i_list[s], coin)
                    print(f"{i_list[s]} 조기 매도합니다")
                    krw_buy = get_balance("KRW")


        else:
            for ss in range(0, len(i_list)):
                coin = get_balance(i_list[ss][4:])
                if coin > 0:
                    upbit.sell_market_order(i_list[ss], coin)
                    print(f"{i_list[ss]} 매도합니다")
                    i_list.remove(i_list[ss])
            for oo in range(0, len(i_list_others)):
                coin = get_balance(i_list_others[oo][4:])
                if coin > 0:
                    upbit.sell_market_order(i_list_others[oo], coin)
                    print(f"{i_list_others[oo]} 매도합니다")
                    i_list.remove(i_list_others[oo])

            krw = get_balance("KRW")
            krw_buy = get_balance("KRW")
            i_list = []
            ik_list = []
            i_list_others = []
            bbk = []

        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
