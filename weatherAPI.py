__author__ = 'Travis'

# API ID = this is being kept in a separate file for security reasons
# correct_url = 'http://api.openweathermap.org/data/2.5/weather?q=Austin,tx&APPID=
import requests
import json
from datetime import date, datetime

city = raw_input("Get forecast for which city/state? Use the format: City,st. > ")
target_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' + city + '&cnt=7&units=imperial&mode=json&APPID='
response = requests.get(target_url)
weather = json.loads(response.text)


def high_temp(weather_data):
    """
    gets temps for the day to find the high by comparing
    values to find the highest value in the dict
    :type weather_data: dict
    :return: highest temp for the day
    """

    weekly = []
    x = 0
    # loop iterates through each day and appends highest value to list by sorting by values in the temp dict.
    while x < 7:
        temps = sorted(weather_data[u'list'][x][u'temp'].values())
        weekly.append(temps[-1])
        x += 1
    return weekly


def low_temp(weather_data):
    """
    gets low temp for the day by comparing values in the
    dict through sorting, then returns the lowest.
    :param weather_data:
    :return: lowest temp for the day
    """

    weekly = []
    x = 0
    # loop iterates through each day and appends lowest value to list by sorting by values in the temp dict.
    while x < 7:
        temps = sorted(weather_data[u'list'][x][u'temp'].values())
        weekly.append(temps[0])
        x += 1
    return weekly


def forecast(weather_data):
    """
    main function to create display data in the form of a list, each day is 1 entry in the list.
    First an integer value for the current date is set, then a string is started with that day
    followed by the high and low temps, followed by the conditions. Upon each iteration of the loop
    the high, low, and day is incremented as necessary, the condition is pulled from the
    appropriate part of the JSON response from openweathermap.org's API and
    the string for each day is constructed in its entirety before it is appended to the final list.
    :param weather_data:
    :return: display data for the week
    """

    current_day = date.weekday(datetime.today())  # returns an integer for today's day: Mon == 0 and Sun == 6
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    display = []
    high = high_temp(weather_data)
    low = low_temp(weather_data)
    x = 0
    while x < 7:
        display_string = """{d}'s high is {h} with a low of {l},
 you should expect {c}""".format(d=days[current_day], h=high[x], l=low[x],
                                 c=weather_data[u'list'][x][u'weather'][0][u'description'])
        display.append(display_string)
        x += 1
        current_day += 1
        if current_day > 6:
            current_day = 0
    return display


def forecast_file(weather_data):
    """writes display data to outside text file for easy access"""

    weather_forecast = forecast(weather_data)  # gets list containing each day's forecast
    txt = open('weather_forecast.txt', 'w')
    for item in weather_forecast:
        txt.write(item)
        txt.write('\n')
    txt.close()


def html_forecast(weather_data):
    """writes data in html format for display on web page or in email newsletter"""

    daily_forecast = forecast(weather_data)
    html = """<!DOCTYPE html>
<html>
    <head>
    <style>
        .forecast {{
            margin-left: auto;
            margin-right: auto;
            width: 500px;
            height: 100px;
            font-family:Helvetica;
            background: -webkit-linear-gradient(right, yellow, white);
        }}
    <title>7 Day Forecast</title>
    </head>
    <body>
        <div class="forecast">{a}</div>
        <div class="forecast">{b}</div>
        <div class="forecast">{c}</div>
        <div class="forecast">{d}</div>
        <div class="forecast">{e}</div>
        <div class="forecast">{f}</div>
        <div class="forecast">{g}</div>
    </body>
</html>""".format(a=daily_forecast[0], b=daily_forecast[1], c=daily_forecast[2], d=daily_forecast[3],
                  e=daily_forecast[4], f=daily_forecast[5], g=daily_forecast[6])
    txt = open('html_weather_forecast.txt', 'w')
    txt.write(html)
    txt.close()


forecast_file(weather)
html_forecast(weather)