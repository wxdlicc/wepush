from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from zhdate import ZhDate

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
wea_id = os.environ["WEA_ID"]
wea_secret = os.environ["WEA_SECRET"]
my_id = os.environ["MY_ID"]
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://www.yiketianqi.com/free/day?appid=" + wea_id + "&appsecret=" + wea_secret + "&unescape=1&city=" + city
  res = requests.get(url).json()
  print(res)
  weather = " " + res['wea'] + ", " + res['tem_night'] + "℃~" + res['tem_day'] + "℃"
  tem = " " + res['tem']
  dateweek = res['date'] + " " + res['week']
  return weather, tem, dateweek

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days + 1

def get_birthday():
    month = int(birthday[:2])
    day = int(birthday[2:])
    next = ZhDate(today.year, month, day).to_datetime()
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days + 1

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, date_week = get_weather()
data = {"dateweek": {"value": date_week},
        "city": {"value": city},
        "weather": {"value": wea},
        "temperature": {"value": temperature},
        "love_days": {"value": get_count()},
        "birthday_left": {"value": get_birthday()},
        "words": {"value": get_words(), "color": get_random_color()}}
print(data)
res = wm.send_template(user_id, template_id, data)
print(res)
res_my = wm.send_template(my_id, template_id, data)
print(res_my)
