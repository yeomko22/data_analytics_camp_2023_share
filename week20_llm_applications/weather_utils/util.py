import os
from datetime import datetime, timedelta
from typing import List

import requests

from .weather_data import WeatherData
from .weather_item import WeatherItem


SKY_TYPE_DICT = {
    "1": "맑음",
    "3": "구름많음",
    "4": "흐림"
}

RAIN_TYPE_DICT = {
    "0": "강수없음",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "4": "소나기",
}


def get_target_date_str(target_date: str) -> str:
    cur_date = datetime.now()
    if target_date == "내일":
        target_date = cur_date + timedelta(days=1)
    elif target_date == "모레":
        target_date = cur_date + timedelta(days=2)
    target_date_str = target_date.strftime("%Y%m%d")
    return target_date_str


def get_weather_data(api_key: str) -> List[WeatherItem]:
    url_template = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={service_key}&numOfRows=1000&pageNo=1&base_date={base_date}&base_time=0500&nx=55&ny=127&dataType=JSON"
    base_date = datetime.now().strftime("%Y%m%d")
    url = url_template.format(service_key=api_key, base_date=base_date)
    response = requests.get(url).json()
    weather_items: List[WeatherItem] = response["response"]["body"]["items"]["item"]
    return weather_items


def postprocess_weather_items(weather_items: List[WeatherItem]):
    weather_dict = {}
    for item in weather_items:
        forecast_date = item["fcstDate"]
        forecast_time = item["fcstTime"]
        value = item["fcstValue"]
        category = item["category"]
        if forecast_date not in weather_dict:
            weather_dict[forecast_date] = WeatherData(forecast_date)

        # 각 카테고리별 데이터 입력
        if category == "TMP":
            weather_dict[forecast_date].temperatures.append(value)
            weather_dict[forecast_date].forecast_times.append(forecast_time)
        elif category == "SKY":
            weather_dict[forecast_date].sky_status.append(SKY_TYPE_DICT[value])
        elif category == "POP":
            weather_dict[forecast_date].rain_percentages.append(value)
        elif category == "PCP":
            weather_dict[forecast_date].rain_amount.append(value)
        elif category == "PTY":
            weather_dict[forecast_date].rain_type.append(RAIN_TYPE_DICT[value])

    for k, v in weather_dict.items():
        for sky, f_time, r_type, r_percentage, r_amount, temperature in \
                zip(v.sky_status, v.forecast_times, v.rain_type, v.rain_percentages, v.rain_amount, v.temperatures):
            if r_type == "강수없음":
                v.weather_per_hour.append(f"{f_time[:2]}:00 {temperature}°C {sky}")
            else:
                v.weather_per_hour.append(f"{f_time[:2]}:00 {temperature}°C {r_type} {r_percentage}% {r_amount}")
    return weather_dict


def get_weather_forecast(target_date: str) -> str:
    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("no weather api key!")
    target_date_str = get_target_date_str(target_date)
    weather_items = get_weather_data(api_key)
    weather_dict = postprocess_weather_items(weather_items)
    target_weather_data = weather_dict[target_date_str]
    weather_info = target_weather_data.get_info()
    return weather_info
