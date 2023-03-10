import requests
import datetime
import math
from twilio.rest import Client
import html
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
URL_STOCK = "https://www.alphavantage.co/query?"
KEY = "B67N7JDLVUMA9A6R"
NEWS_KEY = "4211967b8023437e8d89cc9d4a0ea432"
URL_NEWS = "https://newsapi.org/v2/everything?"

account_sid = "AC02eb8d729f051151ab2930022a99f435"
auth_token = "d4f68edc716c8b20c5bd73ff9925d80c"


PARAMETERS = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": KEY
}

PARAMETERS2 = {
    "qinTitle": COMPANY_NAME,
    "apiKey": NEWS_KEY,
}
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
current_date = datetime.datetime.now().date()
yesterday_date = str(current_date - datetime.timedelta(days=1))
day_before_yesterday_date = str(current_date - datetime.timedelta(days=2))
response = requests.get(url=URL_STOCK, params=PARAMETERS)
response.raise_for_status()
data = response.json()

yesterday_stock = float(data['Time Series (Daily)'][yesterday_date]["4. close"])
day_before_yesterday_stock = float(data['Time Series (Daily)'][day_before_yesterday_date]["4. close"])
x = "🔻" if (day_before_yesterday_stock-yesterday_stock) < 0 else "🔺"
change_percentage = math.fabs((day_before_yesterday_stock-yesterday_stock)/yesterday_stock*100)



## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if change_percentage >= 1:
    response = requests.get(url="https://newsapi.org/v2/everything", params=PARAMETERS2)
    response.raise_for_status()
    news = response.json()
    titles = []
    descriptions = []
    for i in range(3):
        titles.append(news["articles"][i]["title"])
        descriptions.append(news["articles"][i]["description"])
    news_formatted = [f"{COMPANY_NAME}: {x}{change_percentage}% \n Headline: {a} \n Brief: {b}"
                      for (a, b) in zip(titles, descriptions)]

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

client = Client(account_sid, auth_token)

for i in news_formatted:
    message = client.messages.create(
                         body=i,
                         from_='+15095120878',
                         to='+573022496216'
                     )

#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

