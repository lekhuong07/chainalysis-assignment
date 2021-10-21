import requests
from constants import KEY, COIN_LIST, CURRENCIES
from forex_python.converter import CurrencyRates


# get data from lunacrush
# parameters:
# ticker - the crypto / stock that we are going to look at.
# return: the price for that ticker or stock
def get_price_from_lunacrush(ticker):
    ticker = ticker.upper()
    base = f'https://api.lunarcrush.com/v2?data=assets&key={KEY}&symbol={ticker}'
    r = requests.get(base)
    return r.json()['data'][0]['price']  # the price are in 2 decimal


# get data from coinbase
# parameters:
# ticker - the crypto / stock that we are going to look at.
# order_type is going to be: "buy", "sell", "spot"
# return: the price for that ticker or stock
def get_price_from_coinbase(ticker, order_type):
    ticker = ticker.upper()
    base = f'https://api.coinbase.com/v2/prices/{ticker}-usd/{order_type}'
    r = requests.get(base)
    return r.json()['data']['amount']


# combine data together and return as a dictionary.
def get_data():
    # https://help.coinbase.com/en/pro/trading-and-funding/trading-rules-and-fees/fees
    data = {
        "coinbase": [],
        "lunacrush": []
    }

    for coin in COIN_LIST:
        # make API call so don't call it again in initialize value
        cb_buy = round(float(get_price_from_coinbase(coin, "buy")), 2)  # coinbase return a string
        cb_sell = round(float(get_price_from_coinbase(coin, "sell")), 2)
        # let's say lunacrush charges 0.5% to buy and 0.3% to sell (coinbase max is 0.5% for both)
        # if it's an exchange
        lc_buy = round(get_price_from_lunacrush(coin) * 1.005, 2)
        lc_sell = round(get_price_from_lunacrush(coin) * 0.997, 2)
        data["coinbase"].append({
            "ticker": coin.upper(),
            "buy": cb_buy,  # 0.50% if < 10K
            "sell": cb_sell,  # 0.50% if < 10K
            "diff": round(cb_sell - cb_buy, 2)  # if you buy then sell instantly
        })
        data["lunacrush"].append({
            "ticker": coin.upper(),
            "buy": lc_buy,
            "sell": lc_sell,
            "diff": round(lc_sell - lc_buy, 2)
        })
    return data


if __name__ == '__main__':
    # Testing API calls
    cr = CurrencyRates()
    rate = cr.get_rates("USD")
    rate_result = {"USD": 1.00}
    for c in CURRENCIES:
        if c != "USD":
            rate_result[c] = round(rate[c], 2)
    print(rate_result)
    #print(get_data())
