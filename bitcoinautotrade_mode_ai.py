
import time
import numpy as np
import pyupbit
import datetime
import schedule
from fbprophet import Prophet

access = "S7EQC8OdSCSqDeQz8xFozCOHw2DW7qPPKu1qp1vx"
secret = "ozCbzFCxakxVCx8htKqgWI6FxLdnGsjKSIfluGmE"




def get_target_price(ticker):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    target_price = (df.iloc[-2]['high'] - df.iloc[-2]['low'])
    last_price = df.iloc[-2]['close']
    open_price = df.iloc[-2]['open']
    close_5 = df.iloc[-5:, 3]
    close_5_list = close_5.to_list()
    ma5 = np.average(close_5_list)
    close_10 = df.iloc[-10:, 3]
    close_10_list = close_10.to_list()
    ma10 = np.average(close_10_list)

    return target_price, last_price, open_price, ma5, ma10


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



predicted_close_price = []
def predict_price(ticker):
    """Prophet으로 당일 종가 가격 예측"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60")
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    curr_p = df.iloc[-1]['close']
    data = df[['ds','y']]
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
    closeValue = closeDf['yhat'].values[0]
    print(ticker, "closeValue", closeValue, curr_p, round(closeValue/curr_p,2))
    return closeValue

def predict_price_all(coin_list):
    global predicted_close_price
    predicted_close_price = []
    for p in range(0, len(coin_list)):
        try:
            predicted_close_price.append(predict_price(coin_list[p]))
        except:
            predicted_close_price.append(0)






# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

coin_list = pyupbit.get_tickers(fiat="KRW")
i_list_short = []
ik_list_short = []
bbk = []
time_short = []
falling_transition_list = []
rising_transition_list = []
start = []

krw = get_balance("KRW")
krw_buy = get_balance("KRW")


predict_price_all(coin_list)

schedule.every().hour.do(lambda: predict_price_all(coin_list))

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        krw_buy = get_balance("KRW")
        schedule.run_pending()

        if start_time + datetime.timedelta(seconds=3000) < now < end_time - datetime.timedelta(seconds=1800):
            # 대형주

            for c in range(0, len(coin_list)):
                target_price_orgin, last_price, open_price, ma5, ma10  = get_target_price(coin_list[c])
                time.sleep(0.01)
                current_price = get_current_price(coin_list[c])

                if current_price > ma5 : #상승 Transition
                    if rising_transition_list.count(coin_list[c]) < 500 and coin_list[c] not in start:
                        rising_transition_list.append(coin_list[c])
                        max_price = target_price_orgin * 0.8 + last_price
                        target_price_short = target_price_orgin * 0.7 + last_price
                        limit = 1.10
                        if rising_transition_list.count(coin_list[c]) >= 499:
                            start.append(coin_list[c])

                    elif rising_transition_list.count(coin_list[c]) < 500 and coin_list[c] in start:
                        if rising_transition_list.count(coin_list[c]) > 200:
                            rising_transition_list.append(coin_list[c])
                            max_price = target_price_orgin * 0.8 + last_price
                            target_price_short = ma5 + ma5 * 0.03
                            limit = 1.10
                        else:
                            rising_transition_list.append(coin_list[c])
                            max_price = target_price_orgin * 0.8 + last_price
                            target_price_short = ma5 + ma5 * 0.05
                            limit = 1.10
                            # print("상승 Transition")

                    else:  #상승 모드
                        max_price = target_price_orgin * 0.8 + last_price
                        target_price_short = target_price_orgin * 0.5 + last_price
                        limit = 1.10
                        falling_transition_list = []
                        start.append(coin_list[c])
                        # print("상승")

                else:
                    if falling_transition_list.count(coin_list[c]) < 300: # 하강 Transition
                        falling_transition_list.append(coin_list[c])
                        max_price = target_price_orgin * 0.5 + last_price
                        target_price_short = target_price_orgin * 3.5 + last_price
                        limit = last_price / open_price

                        limit = 1.10
                        if falling_transition_list.count(coin_list[c]) >= 299:
                            start.append(coin_list[c])
                        # print("하강 Transition")

                    else: # 하강모드
                        max_price = target_price_orgin * 0.5 + last_price
                        target_price_short = target_price_orgin * 3.5 + last_price
                        limit = 1.10
                        rising_transition_list = []
                        start.append(coin_list[c])
                        # print("하강")

                if target_price_short < current_price and coin_list[c] not in i_list_short and krw_buy > 5000 \
                        and last_price / open_price < limit and current_price < max_price and target_price_orgin /open_price < 0.1\
                        and current_price * 1.02 < predicted_close_price[c] :

                    bbk.append(coin_list[c])

                # print(coin_list[c], target_price_short - current_price, current_price * 1.02 - predicted_close_price[c] )

                if target_price_short < current_price and coin_list[c] not in i_list_short and krw_buy > 5000 \
                        and last_price / open_price < limit and current_price < max_price and bbk.count(coin_list[c]) > 5\
                        and target_price_orgin /open_price < 0.1 and current_price * 1.02 < predicted_close_price[c] :
                    if krw_buy < krw * 0.2:
                        oder_krw = krw_buy * 0.9995
                    else:
                        oder_krw = krw * 0.1995
                    upbit.buy_market_order(coin_list[c], oder_krw)
                    print(f"{coin_list[c]} 매수합니다")
                    time.sleep(10)
                    krw_buy = get_balance("KRW")
                    i_list_short.append(coin_list[c])
                    ik_list_short.append(current_price)
                    now_short = datetime.datetime.now()
                    time_short.append(now_short)

            # 조기 매도
            if falling_transition_list.count(coin_list[c]) > 300:
                for o in range(0, len(i_list_short)):
                    target_price_sell_short = ik_list_short[o]
                    current_price_sell_short = get_current_price(i_list_short[o])
                    coin = get_balance(i_list_short[o][4:])
                    now_cell = datetime.datetime.now()
                    if target_price_sell_short * 1.0050 < current_price_sell_short:
                        upbit.sell_market_order(i_list_short[o], coin)
                        print(f"{i_list_short[o]}  falling transition 매도합니다")
                        krw_buy = get_balance("KRW")


            else:

                for o in range(0, len(i_list_short)):
                    target_price_sell_short = ik_list_short[o]
                    current_price_sell_short = get_current_price(i_list_short[o])
                    coin = get_balance(i_list_short[o][4:])
                    now_cell = datetime.datetime.now()
                    if i_list_short[o] == "KRW-BTC":
                        profit = 1.05
                    else:
                        profit = 1.22

                    if target_price_sell_short * profit < current_price_sell_short and coin > 0:
                        upbit.sell_market_order(i_list_short[o], coin)
                        print(f"{i_list_short[o]} 이익 실현 매도합니다")
                        krw_buy = get_balance("KRW")

                    if now_cell - time_short[o] > datetime.timedelta(
                            seconds=7200) and coin > 0 and target_price_sell_short * 1.03 < current_price_sell_short < target_price_sell_short * 1.03:
                        upbit.sell_market_order(i_list_short[o], coin)
                        print(f"{i_list_short[o]} 2시간 매도합니다")
                        krw_buy = get_balance("KRW")
                    if now_cell - time_short[o] > datetime.timedelta(
                            seconds=14400) and coin > 0 and target_price_sell_short * 1.01 < current_price_sell_short < target_price_sell_short * 1.05:
                        upbit.sell_market_order(i_list_short[o], coin)
                        print(f"{i_list_short[o]} 4시간 매도합니다")
                        krw_buy = get_balance("KRW")
                    if now_cell - time_short[o] > datetime.timedelta(
                            seconds=28800) and coin > 0 and target_price_sell_short * 1.0050 < current_price_sell_short < target_price_sell_short * 1.12:
                        upbit.sell_market_order(i_list_short[o], coin)
                        print(f"{i_list_short[o]} 8시간 매도합니다")
                        krw_buy = get_balance("KRW")




        else:
            for oo in range(0, len(i_list_short)):
                coin = get_balance(i_list_short[oo][4:])
                if coin > 0:
                    upbit.sell_market_order(i_list_short[oo], coin)
                    print(f"{i_list_short[oo]} 최종 매도합니다")

            krw = get_balance("KRW")
            krw_buy = get_balance("KRW")
            i_list_short = []
            ik_list_short = []
            time_short = []
            bbk = []
            falling_transition_list = []
            rising_transition_list = []
            start = []



        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
