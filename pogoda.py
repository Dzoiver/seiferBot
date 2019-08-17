import weather
import requests, json

api_key = '4b4f27869ff5dd5617a6c5fd9f3b9870'
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city = 'ulyanovsk'
url = base_url + "appid=" + api_key + "&q=" + city
json_data = requests.get(url).json()
info = json_data['main']
current_temp = info['temp']
print(info)
print(int(current_temp) -273)
for e in json_data:
    print(e)

# pogoda = weather.Weather(unit=weather.Unit.CELSIUS)
# try:
#     lookup = pogoda.lookup(560743)
# except requests.exceptions.ConnectionError:
#     print('nu sorry')
# condition = lookup.condition
#
# print(condition.text)