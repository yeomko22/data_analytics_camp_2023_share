from typing import TypedDict


class WeatherItem(TypedDict):
    baseDate: str
    baseTime: str
    category: str
    fcstDate: str
    fcstTime: str
    fcstValue: str
    nx: str
    ny: str
