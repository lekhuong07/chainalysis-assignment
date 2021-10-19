import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, render_template

from forex_python.converter import CurrencyRates

from constants import COIN_LIST
from fetch_data import get_data

app = Flask(__name__)


@app.route('/')
def index():
    coin_str = ", ".join(COIN_LIST)
    return render_template('index.html', coin=coin_str, value=get_data())


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=get_data,
        trigger=IntervalTrigger(seconds=5),
        id='prices_retrieval_job',
        name='Retrieve prices every 5 seconds',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    app.run(debug=True, host='0.0.0.0', use_reloader=True)
