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
krw_buy = get_balance("KRW")
BTC_i = 0
AXS_i = 0
SAND_i = 0
MANA_i =0
XTZ_i =0
XRP_i =0
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)


        if start_time < now < end_time - datetime.timedelta(seconds=1800):
            target_price_BTC = get_target_price("KRW-BTC", 0.7)
            current_price_BTC = get_current_price("KRW-BTC")


            target_price_AXS = get_target_price("KRW-XEC", 0.7)
            current_price_AXS  = get_current_price("KRW-XEC")


            target_price_SAND = get_target_price("KRW-KNC", 0.5)
            current_price_SAND = get_current_price("KRW-KNC")


            target_price_MANA = get_target_price("KRW-AERGO", 0.6)
            current_price_MANA = get_current_price("KRW-AERGO")


            target_price_XTZ = get_target_price("KRW-GLM", 0.8)
            current_price_XTZ = get_current_price("KRW-GLM")

            target_price_XRP = get_target_price("KRW-XRP", 0.5)
            current_price_XRP = get_current_price("KRW-XRP")

            if target_price_BTC < current_price_BTC and BTC_i ==0:
                if krw_buy > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.5995)
                    print("BTC 매수합니다")
                    time.sleep(10)
                    krw_buy = get_balance("KRW")
                    BTC_i =1
            if target_price_AXS < current_price_AXS and AXS_i ==0:
                if krw_buy > 5000:
                    upbit.buy_market_order("KRW-XEC", krw*0.3995)
                    print("XEC 매수합니다")
                    time.sleep(10)
                    krw_buy = get_balance("KRW")
                    AXS_i = 1
            if target_price_SAND < current_price_SAND and SAND_i == 0:
                if krw_buy > 5000:
                    upbit.buy_market_order("KRW-KNC", krw*0.3995)
                    print("KNC 매수합니다")
                    time.sleep(10)
                    krw_buy = get_balance("KRW")
                    SAND_i = 1
            if target_price_MANA < current_price_MANA and MANA_i == 0:
                if krw_buy > 5000:
                    upbit.buy_market_order("KRW-AERGO", krw*0.1995)
                    print("MANA 매수합니다")
                    time.sleep(10)
                    krw_buy = get_balance("KRW")
                    MANA_i = 1
            if target_price_XTZ < current_price_XTZ and XTZ_i == 0:
                if krw_buy > 5000:
                    upbit.buy_market_order("KRW-GLM", krw*0.1995)
                    print("XTZ 매수합니다")
                    time.sleep(10)
                    krw_buy = get_balance("KRW")
                    XTZ_i = 1
            if target_price_XRP < current_price_XRP and XRP_i == 0:
                if krw_buy > 5000:
                    upbit.buy_market_order("KRW-XRP", krw*0.3995)
                    print("XRP 매수합니다")
                    time.sleep(10)
                    krw_buy = get_balance("KRW")
                    XRP_i = 1

        else:
            btc = get_balance("BTC")
            if btc > 0.00009 and BTC_i ==1:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                print("BTC 매도합니다")
                BTC_i = 0
            AXS = get_balance("XEC")
            if AXS > 0.00008 and AXS_i ==1:
                upbit.sell_market_order("KRW-XEC", AXS*0.9995)
                print("POLY 매도합니다")
                AXS_i = 0
            SAND = get_balance("KNC")
            if SAND > 0.00008 and SAND_i ==1:
                upbit.sell_market_order("KRW-KNC", SAND*0.9995)
                print("KNC 매도합니다")
                SAND_i = 0
            MANA = get_balance("AERGO")
            if MANA > 0.00008 and MANA_i ==1:
                upbit.sell_market_order("KRW-AERGO", MANA*0.9995)
                print("AERGO 매도합니다")
                MANA_i = 0
            XTZ = get_balance("GLM")
            if XTZ > 0.00008 and XTZ_i ==1:
                upbit.sell_market_order("KRW-GLM", XTZ*0.9995)
                print("GLM 매도합니다")
                XTZ_i = 0
            XRP = get_balance("XRP")
            if XRP > 0.00008 and XRP_i ==1:
                upbit.sell_market_order("KRW-XRP", XRP*0.9995)
                print("XRP 매도합니다")
                XRP_i = 0
            BTC_i = 0
            AXS_i = 0
            SAND_i = 0
            MANA_i = 0
            XTZ_i = 0
            XRP_i = 0
            krw = get_balance("KRW")

        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
