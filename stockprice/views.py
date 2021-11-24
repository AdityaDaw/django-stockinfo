from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import yfinance
import pandas as pd
import os
from django.conf import settings
import json
# Create your views here.

def getquote(request):
    symbol=request.GET.get("symbol")
    stock=yfinance.Ticker(symbol)
    earnings=stock.earnings
    dv=stock.dividends
    summary=(stock.info)['longBusinessSummary']
    longName=(stock.info)['longName']
    marketCap=(stock.info)['marketCap']
    trailingAnnualDividendYield=(stock.info)['trailingAnnualDividendYield']
    try:
        date=list(dv.index.to_list())[-10:-1]
        dividend=list(dv.to_list())[-10:-1]
        dvd=zip(date,dividend)
    except:
        dvd=None
    try:
        yaer=list(earnings.index.to_list())[-10:-1]
        rev=list(earnings['Revenue'].to_list())[-10:-1]
        ear=list(earnings['Earnings'].to_list())[-10:-1]
        ear_rev=zip(yaer,rev,ear)
    except:
        ear_rev=None
    
    rc=stock.recommendations
    try:
        yaer=list(rc.index.to_list())[-5:-1]
        Firm=list(rc['Firm'].to_list())[-5:-1]
        To_grade=list(rc['To Grade'].to_list())[-5:-1]
        recc=zip(yaer,Firm,To_grade)
    except:
        recc=None
    
    data={
        'Devd':dvd,
        'Earnings':ear_rev,
        'Recc':recc,
        'Summary':summary,
        'LongName':longName,
        'MarketCap':marketCap,
        'TrailingAnnualDividendYield':trailingAnnualDividendYield,
    }
    return render(request, os.path.join('stockprice','price_show.html'),data)

def home(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'stockprice','st.csv')
    ticker=pd.read_csv(file_path)
    content = list(ticker['SYMBOL'].to_list())
    quotes=json.dumps(content)
    
    return render(request,os.path.join('stockprice','home.html'),{'quotes':quotes})