from redis import Redis
import os
import time
import requests

REDIS_HOST     = os.environ['REDIS_HOST']
REDIS_PORT     = os.environ['REDIS_PORT']
REDIS_TTL      = os.environ['REDIS_TTL']
PG_ENDPOINT    = os.environ['PG_ENDPOINT']
DELAY_INTERVAL = os.environ['DELAY_INTERVAL']

r = Redis(host=REDIS_HOST, port=REDIS_PORT, db=1)

coins = {
    "bitcoin": "BTC", 
    "ethereum": "ETH", 
    "cardano": "ADA", 
    "ripple": "XRP", 
    "dogecoin": "DOGE", 
    "matic-network": "MATIC", 
    "tron": "TRX", 
    "chainlink": "LINK", 
    "vechain": "VET"
}

def get_price_in_usd(coin, currency):
    coingecko_api_url = "https://api.coingecko.com/api/v3/coins/markets"
    headers = {"content-type": "application/json", "accept": "application/json"}
    parameters = {"vs_currency": currency, "ids": coin, "order": "market_cap_desc", "per_page": "100", "sparkline": "false"}
    response = requests.get(coingecko_api_url, headers=headers, params=parameters).json()
    return response

def post_metric_to_pushgateway(coin, metric_value):
    request_url = '{endpoint}/metrics/job/crypto-to-usd/provider/coingecko/coin/{coin}'.format(coin=coin, endpoint=PG_ENDPOINT)
    response = requests.post(request_url, data='{_n} {_v}\n'.format(_n='cryptocurrency_price'.format(coin=coin), _v=metric_value))
    return response.status_code

while True:
    for coin in coins.keys():
        value = r.get('{acr}_TO_USD'.format(acr=coins[coin]))
        if value == None:
            print("MISS: retrieving from db and adding to redis")
            response = get_price_in_usd(coin, "usd")
            r.set('{coin}_TO_USD'.format(coin=coins[coin]), response[0]['current_price'], ex=int(REDIS_TTL))
            pg_response = post_metric_to_pushgateway(response[0]['symbol'], response[0]['current_price'])
        else:
            print("HIT: retrieved from redis {}".format(value))
            pg_response = post_metric_to_pushgateway(coin, value)

    time.sleep(int(DELAY_INTERVAL))
