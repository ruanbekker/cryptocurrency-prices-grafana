from flask import Flask
from redis import Redis
import os

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

app = Flask(__name__)
redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=1)

@app.route("/coins/<acr>")
def retrieve_coin_price(acr):
    value = redis.get('{coin}_TO_USD'.format(coin=acr.upper()))
    return {"acronymm": acr.upper(), "current_price_in_usd": value.decode("utf-8")}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
