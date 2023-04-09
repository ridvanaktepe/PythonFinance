import datetime
import json
from celery import shared_task
import requests

from .models import OrderBook


@shared_task
def save_order_book(self):

        
    url = "https://www.bitexen.com/api/v1/order_book/BTCTRY/"

    response = requests.get(url)
    data = json.loads(response.content)

    low_24h = json.dumps(float(data["data"]["ticker"]["low_24h"]))
    high_24h = json.dumps(float(data["data"]["ticker"]["high_24h"]))
    avg_24h = json.dumps(float(data["data"]["ticker"]["avg_24h"]))
    volume_24h = json.dumps(float(data["data"]["ticker"]["volume_24h"]))
    day=datetime.datetime.fromtimestamp((float(data["data"]["ticker"]["timestamp"]))).strftime('%d')
    week=datetime.datetime.fromtimestamp((float(data["data"]["ticker"]["timestamp"]))).strftime('%V')
    mount=datetime.datetime.fromtimestamp((float(data["data"]["ticker"]["timestamp"]))).strftime('%m')

    order_book = OrderBook(low_24h=low_24h, high_24h=high_24h, avg_24h=avg_24h, volume_24h=volume_24h, day=day, week=week, mount=mount)
    order_book.save()

    return "Db save operation successful"
