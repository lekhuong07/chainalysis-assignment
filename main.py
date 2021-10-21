import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, render_template, jsonify, json

from forex_python.converter import CurrencyRates

from constants import COIN_LIST, CURRENCIES
from fetch_data import get_data

app = Flask(__name__)


@app.route('/')
def index():
    coin_str = ", ".join(COIN_LIST)
    cr = CurrencyRates()
    rate = cr.get_rates("USD")
    rate_result = {"USD": 1.00}
    for c in CURRENCIES:
        if c != "USD":
            rate_result[c] = round(rate[c], 2)

    # make it easier to return
    result = {
        "rate_result": rate_result,
        "coin_str": coin_str,
        "value": get_data()
    }
    return render_template('index.html', render_value=result)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=get_data,
        trigger=IntervalTrigger(seconds=30),
        id='prices_retrieval_job',
        name='Retrieve prices every 30 seconds',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    app.run(host='127.0.0.1', port=8000, debug=True, use_reloader=False)
