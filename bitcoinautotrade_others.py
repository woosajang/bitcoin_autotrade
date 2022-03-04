import time
import pyupbit
import datetime

access = ""
secret = ""

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
krw = get_balance("KRW")
BTC_i = 0
AXS_i = 0
SAND_i = 0
MANA_i =0
XTZ_i =0
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)


        if start_time < now < end_time - datetime.timedelta(seconds=1800):
            target_price_BTC = get_target_price("KRW-BTC", 0.9)
            current_price_BTC = get_current_price("KRW-BTC")


            target_price_AXS = get_target_price("KRW-AXS", 0.9)
            current_price_AXS  = get_current_price("KRW-AXS")


            target_price_SAND = get_target_price("KRW-SAND", 0.6)
            current_price_SAND = get_current_price("KRW-SAND")


            target_price_MANA = get_target_price("KRW-MANA", 0.6)
            current_price_MANA = get_current_price("KRW-MANA")


            target_price_XTZ = get_target_price("KRW-XTZ", 0.8)
            current_price_XTZ = get_current_price("KRW-XTZ")

            if target_price_BTC < current_price_BTC and BTC_i ==0:
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.3995)
                    print("BTC 매수합니다")
                    time.sleep(10)
                    krw = get_balance("KRW")
                    BTC_i =1
            if target_price_AXS < current_price_AXS and AXS_i ==0:
                if krw > 5000:
                    upbit.buy_market_order("KRW-AXS", krw*0.0995)
                    print("AXS 매수합니다")
                    time.sleep(10)
                    krw = get_balance("KRW")
                    AXS_i = 1
            if target_price_SAND < current_price_SAND and SAND_i == 0:
                if krw > 5000:
                    upbit.buy_market_order("KRW-SAND", krw*0.2995)
                    print("SAND 매수합니다")
                    time.sleep(10)
                    krw = get_balance("KRW")
                    SAND_i = 1
            if target_price_MANA < current_price_MANA and MANA_i == 0:
                if krw > 5000:
                    upbit.buy_market_order("KRW-MANA", krw*0.0995)
                    print("MANA 매수합니다")
                    time.sleep(10)
                    krw = get_balance("KRW")
                    MANA_i = 1
            if target_price_XTZ < current_price_XTZ and XTZ_i == 0:
                if krw > 5000:
                    upbit.buy_market_order("KRW-XTZ", krw*0.0995)
                    print("XTZ 매수합니다")
                    time.sleep(10)
                    krw = get_balance("KRW")
                    XTZ_i = 1

        else:
            btc = get_balance("BTC")
            if btc > 0.00009 and BTC_i ==1:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                print("BTC 매도합니다")
                BTC_i = 0
            AXS = get_balance("AXS")
            if AXS > 0.00008 and AXS_i ==1:
                upbit.sell_market_order("KRW-AXS", AXS*0.9995)
                print("AXS 매도합니다")
                AXS_i = 0
            SAND = get_balance("SAND")
            if SAND > 0.00008 and SAND_i ==1:
                upbit.sell_market_order("KRW-SAND", SAND*0.9995)
                print("SAND 매도합니다")
                SAND_i = 0
            MANA = get_balance("MANA")
            if MANA > 0.00008 and MANA_i ==1:
                upbit.sell_market_order("KRW-MANA", MANA*0.9995)
                print("MANA 매도합니다")
                MANA_i = 0
            XTZ = get_balance("XTZ")
            if XTZ > 0.00008 and XTZ_i ==1:
                upbit.sell_market_order("KRW-XTZ", XTZ*0.9995)
                print("XTZ 매도합니다")
                XTZ_i = 0
            BTC_i = 0
            AXS_i = 0
            SAND_i = 0
            MANA_i = 0
            XTZ_i = 0
            krw = get_balance("KRW")

        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
