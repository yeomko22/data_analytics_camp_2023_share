from typing import List


class WeatherData:
    def __init__(self, forecast_date):
        self.forecast_date = forecast_date
        self.forecast_times: List[str] = []
        self.temperatures: List[int] = []
        self.sky_status: List[str] = []
        self.rain_percentages: List[int] = []
        self.rain_amount: List[str] = []
        self.rain_type: List[str] = []
        self.weather_per_hour: List[str] = []

    def get_info(self):
        weather_per_hour_str = '\n'.join(self.weather_per_hour)
        return f"""날짜: {self.forecast_date} 
최고 기온: {max(self.temperatures)}°C
최저 기온: {min(self.temperatures)}°C

시간대 별 날씨
{weather_per_hour_str}
"""
