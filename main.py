from datetime import date, datetime
import math
from nturl2path import url2pathname
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather_now():
  url = "https://restapi.amap.com/v3/weather/weatherInfo?key=fd6beb7eed087534ab7e54872ff47d06&city=640105&extensions=base"
  res = requests.get(url).json()
  weather = res['lives'][0]
  city_n = res['lives'][0]['city']
  return weather['weather'], weather['temperature'],city_n

def get_weather_all():
  url = "https://restapi.amap.com/v3/weather/weatherInfo?key=fd6beb7eed087534ab7e54872ff47d06&city=640105&extensions=all"
  res = requests.get(url).json()
  weather = res['forecasts'][0]['casts'][0]
  return weather['nighttemp'],weather['daytemp']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d %H:%M:%S")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def temp_judge():
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key=fd6beb7eed087534ab7e54872ff47d06&city=640105&extensions=base"
    res = requests.get(url).json()
    str = ""
    temp_now = int(res['lives'][0]['temperature'])
    if temp_now <= 18:
        str = "小笨蛋，现在天气温度有点冷哦，记得多穿点衣服。（づ￣3￣）づ╭❤～"
    else:
        str = "现在天气有点热哦，可是适当减少衣物啦~(*^▽^*)"
    return str

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, city = get_weather_now()
low, high, = get_weather_all()
clothes = temp_judge()
data = {"weather":{"value":wea},"city": {"value": city},"low": {"value": low},"high": {"value": high},"temperature":{"value":temperature},"clothes": {"value": clothes, "color": get_random_color()},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
