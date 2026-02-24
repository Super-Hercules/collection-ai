import openmeteo_requests
import pandas
import requests_cache
import csv
import os

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 26.05942,
    "longitude": 119.198,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "daily": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "sunshine_duration"],
    "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "weather_code", "cloud_cover", "wind_speed_10m", "wind_direction_10m", "shortwave_radiation", "is_day"],
    "timezone": "Asia/Singapore",
}

script_directory = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_directory, "data")
os.makedirs(data_path, exist_ok = True)
geo_file_path = os.path.join(data_path, "geographic_data.csv")
hourly_file_path = os.path.join(data_path, "hourly_data.csv")

def main():
    cache_session = requests_cache.CachedSession(".cache", expire_after = -1)
    #创建一个持久化缓存的会话，将请求结果缓存在本地.cache文件夹，且永不过期（expire_after=-1），避免重复请求相同数据。
    openmeteo = openmeteo_requests.Client(session = cache_session)
    response = openmeteo.weather_api(url, params = params)[0]
    geographic_data = [
        [
            "latitude",
            "longitude",
            "elevation",
            "utc_offset_seconds",
            "timezone",
            "timezone_abbreviation"
        ],
        [
            response.Latitude(),
            response.Longitude(),
            response.Elevation(),
            response.UtcOffsetSeconds(),
            response.Timezone().decode("utf-8"),
            response.TimezoneAbbreviation().decode("utf-8")
        ]
    ]

    with open(geo_file_path, "w", encoding = "utf-8", newline = "") as file:
        writer = csv.writer(file)
        writer.writerows(geographic_data) 

    hourly = response.Hourly()
    print(hourly)
    hourly_data_head = [
        "time",
        "temperature_2m (°C)",
        "relative_humidity_2m (%)",
        "apparent_temperature (°C)",
        "precipitation (mm)",
        "weather_code (wmo code)",
        "cloud_cover (%)", 
        "wind_speed_10m (km/h)",
        "wind_direction_10m (°)",
        "shortwave_radiation (W/m²)",
        "is_day ()"
    ]

    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(4).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(5).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(6).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(7).ValuesAsNumpy()
    hourly_shortwave_radiation = hourly.Variables(8).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(9).ValuesAsNumpy()

    hourly_data = {"date": pandas.date_range(
	start = pandas.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
	end =  pandas.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
	freq = pandas.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
    hourly_data["is_day"] = hourly_is_day

    hourly_dataframe = pandas.DataFrame(hourly_data)
    hourly_dataframe.to_csv(hourly_file_path, index = False, encoding = "utf-8-sig")#UTF-8 with BOM

if __name__ == "__main__":
    main()