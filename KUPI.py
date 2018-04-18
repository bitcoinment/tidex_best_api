# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import time
import requests
import json
import os

# GLOBAL_DOMAIN = 'http://127.0.0.1:8000'
GLOBAL_DOMAIN = 'http://kupi.net'
GLOBAL_API_KEY = False

def jprint(arr):
    print(json.dumps(arr, indent=4, sort_keys=False))


def apiRoute(arr):

    if not GLOBAL_API_KEY:
        return {
            'error': True,
            'message': 'Api key not specified!'
        }


    conf_site = os.path.join(GLOBAL_DOMAIN,'api', 'v1', GLOBAL_API_KEY)
    postfix = '/'.join(arr)
    url = os.path.join(conf_site, postfix.lower())

    try:
        print(url)
        r = requests.get(url)
        response = r.content.decode('utf8')
        if len(response) > 0:
            data = json.loads(response)
            return data
        else:
            print('Server error')
            return False


    except Exception as e:
        print('Error >> '+str(e))
        return False



class KUPINET:

    def __init__(self, apikey):
        global GLOBAL_API_KEY
        GLOBAL_API_KEY = apikey


    class Stocks:

        def __init__(self, stock_name=False):
            self.stock_name = stock_name.strip() if stock_name else False

        def getOrders(self, coin_from, coin_to):
            coin_from_ = coin_from.strip().lower()
            coin_to_   = coin_to.strip().lower()


            return apiRoute(['stocks',self.stock_name,'orders',coin_from_,coin_to_])

        def getList(self):
            return apiRoute(['stocks-list'])

        def getAllPairs(self):
            return apiRoute(['stocks', self.stock_name, 'all-pairs'])


    class Pair:
        def __init__(self, coin_from=False, coin_to=False):
            self.coin_from_ = coin_from.strip().lower()
            self.coin_to_ = coin_to.strip().lower()

        def getBestPrices(self):

            return apiRoute(['pairs', 'best-prices', self.coin_from_, self.coin_to_])


    class BestPrices:
        def __init__(self, coin):
            self.coin_ = coin.strip().lower()

        def Ask(self):
            return apiRoute(['best-prices', 'ask', self.coin_])

        def Bid(self):
            return apiRoute(['best-prices', 'bid', self.coin_])



    class Calc:
        def __init__(self, coin_from=False, coin_to=False):
            self.coin_from = False
            self.coin_to = False

            if coin_from and coin_to:
                self.coin_from = coin_from.strip().lower()
                self.coin_to = coin_to.strip().lower()

        def Amount(self, amount):
            self.amount = str(float(amount))

            if not self.coin_from or not self.coin_to:
                return {
                    'error': True,
                    'message': 'Coins not defined',
                }

            return apiRoute(['calc', 'math', self.coin_from, self.coin_to, self.amount])


        def Data(self):
            return apiRoute(['calc', 'data'])



if __name__ == "__main__":
    pass


    # orders = KUPINET('freeApi').Stocks('Binance').getOrders('ETH','BTC')
    # jprint(orders)

    # allStocks = KUPINET('freeApi').Stocks().getList()
    # jprint(allStocks)

    #
    # pairs = KUPINET.Stocks('Binance').getAllPairs()
    # jprint(pairs)

    # prices = KUPINET.Pair('LTC','ETH').getBestPrices()
    # jprint(prices)


    # bestAsk = KUPINET.BestPrices('LTC').Ask()
    # bestBid = KUPINET.BestPrices('LTC').Bid()
    # jprint(bestAsk)
    # jprint(bestBid)


    # calcMath = KUPINET.Calc('LTC','ETH').Amount(10)
    # jprint(calcMath)

    # calcData = KUPINET.Calc().Data()
    # jprint(calcData)

