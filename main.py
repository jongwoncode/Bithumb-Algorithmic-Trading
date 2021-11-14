# 변동성 돌파 전략 코드 
import time
import pybithumb
import datetime


# 목표가 구하는 함수
def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]            

    today_open = yesterday['close']      
    yesterday_high = yesterday['high']   
    yesterday_low = yesterday['low']     
    target = today_open + (yesterday_high - yesterday_low) * 0.5   
    return target


# 매수 함수 구현
def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]-bithumb.get_balance(ticker)[3]    
    order_krw = krw*0.80                # 안잡히는 경우가 있어서 주문 가능한 가격에 * 0.8 을 해준다.
    orderbook = pybithumb.get_orderbook(ticker)

    sell_price = orderbook['asks'][0]['price']
    unit = order_krw/float(sell_price)
    bithumb.buy_market_order(ticker, unit)


## 매도 함수 구현
def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)


if __name__ ==  "__main__()" :
    
    ## api.txt 파일 열어서 접속
    with open('api.txt') as f :
        lines = f.readlines()
        key = lines[0].strip()
        secret = lines[1].strip()
        bithumb = pybithumb.Bithumb(key, secret)    

    # 5일 이평선 구하기
    def get_yesterday_ma5(ticker):
        df = pybithumb.get_ohlcv(ticker)
        close = df['close']
        ma = close.rolling(window =5).mean()
        return ma[-2]

    # 프로그램이 시작될 때 전일 `5일이평선` 구한다. 
    now = datetime.datetime.now()
    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
    ma5 = get_yesterday_ma5('BTC')
    target_price = get_target_price('BTC')


    # 목표가 설정 및 매수/ 자정 전량 매도
    while True:
        try :
            now = datetime.datetime.now()
            if mid < now < mid + datetime.delta(seconds = 10):
                target_price = get_target_price('BTC')
                mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                ma5 = get_yesterday_ma5('BTC')
                sell_crypto_currency('BTC')

            ## (목표가 도달 & 5일 이평선 위에 있을 때) 매수 
            current_price = pybithumb.get_current_price('BTC')
            if (current_price > target_price) and (current_price > ma5):
                buy_crypto_currency('BTC')
        
        except Exception as e:
            print('Error', e)
        time.sleep(1)