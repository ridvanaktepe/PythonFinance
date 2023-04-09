import datetime
from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import OrderBook
from .tasks import save_order_book
from rest_framework.decorators import api_view
import psycopg2


def get_statistics_from_db(rawSqlQuery):
    conn = psycopg2.connect(
        database="financedb", user='postgres',
        password='4535', host='localhost', port='5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(rawSqlQuery)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def get_order_book():
    save_order_book.delay()
    return JsonResponse({"message": "Order book data saved to database"})


@api_view(['GET'])
def get_statics(request):
    dailyDict = []
    weeklyDict = []
    mountlyDict = []

    daily = get_statistics_from_db(
        'SELECT avg(low_24h), avg(high_24h), avg(avg_24h), avg(volume_24h), day FROM public."FinanceApi_orderbook" GROUP BY day')
    weekly = get_statistics_from_db(
        'SELECT avg(low_24h), avg(high_24h), avg(avg_24h), avg(volume_24h), week FROM public."FinanceApi_orderbook" GROUP BY week')
    mountly = get_statistics_from_db(
        'SELECT avg(low_24h), avg(high_24h), avg(avg_24h), avg(volume_24h), mount FROM public."FinanceApi_orderbook" GROUP BY mount')

    for d in daily:
        dailyDict.append({"daily_low":d[0], "daily_high":d[1], "daily_avg":d[2], "daily_volume":d[3], "day":d[4]})
    for w in weekly:
        weeklyDict.append({"weekly_low":w[0], "weekly_high":w[1], "weekly_avg":w[2], "weekly_volume":w[3], "week": w[4]})
    for m in mountly:
        mountlyDict.append({"mountly_low":m[0], "mountly_high":m[1], "mountly_avg":m[2], "mountly_volume":m[3], "mount": m[4]})

    return JsonResponse({"daily": dailyDict, "weekly": weeklyDict, "mountly": mountlyDict})
