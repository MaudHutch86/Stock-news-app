import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
# api_key = os.environ.get('api_key')change with you personal account details
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
#news_api_key = os.environ.get("news_api_key")change with you personal account details
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
#twilio_sid = os.environ.get("twilio_sid") change with you personal account details
#twilio_token = os.environ.get("twilio_token") change with you personal account details

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key

}

stock_api = requests.get(STOCK_ENDPOINT, params=parameters)
data = stock_api.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

price_difference = round(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))

up_down = None
if price_difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

result = round(100 * (float(yesterday_closing_price) - float(day_before_yesterday_closing_price)) / float(
    day_before_yesterday_closing_price))

if abs(result) > 3:

    news_api_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": news_api_key
    }

    news_api = requests.get(NEWS_ENDPOINT, params=news_api_parameters)
    news_data = news_api.json()["articles"]
    three_articles = news_data[:3]
    print(three_articles)

    formatted_article_list = [f"{STOCK}:{up_down}{price_difference}%\nHeadlines:{article['title']}.\n Brief:"
                              f"{article['description']}" for article in
                              three_articles]
    client = Client(twilio_sid, twilio_token)

    """"Make use to change you twilio account details"""
    for article in formatted_article_list:
        message = client.messages.create(
            body=article,
            # from_="000000000" use your personal twilio number
            # to="0000000000" put the number you want to send msg to into the string
        )
