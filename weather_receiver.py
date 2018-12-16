# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 12:32:17 2018

@author: James
"""

import requests
import datetime

class weather_point(object):
    """
    Represents a weather data point
    """
    def __init__(self, date_time = None,
                 mainT = None,
                 maxT = None,
                 minT = None,
                 humidity = None,
                 cloud_cover_per = None,
                 rain_mm = None,
                 snow_mm = None,
                 wind_speed_mps = None,
                 main_weather = None,
                 description = None,
                 icon = None):
        """
        This is only a subset of what is available from the data request
        more info is available, particularly pressure info if we want that..
        """
        self.date_time = date_time
        self.mainT = str(mainT)
        self.minT = str(minT)
        self.maxT = str(maxT)
        self.humidity = str(humidity)
        self.cloud_cover_per = str(cloud_cover_per)
        self.rain_mm = str(rain_mm)
        self.snow_mm = str(snow_mm)
        self.wind_speed_mps = str(wind_speed_mps)
        self.main_weather = str(main_weather)
        self.description = str(description)
        self.icon = str(icon)
    
    def __repr__(self):
        rep = '<weather_point: time: ' + str(self.date_time) + ' temperature: ' + \
        self.mainT + ' max Temp: ' + self.maxT + ' min Temp: ' + self.minT + \
        ' humidity: ' + self.humidity + ' % cloud cover: ' + self.cloud_cover_per + \
        ' rain mm: ' + self.rain_mm + ' snow mm: ' + self.snow_mm + \
        ' wind speed mps: ' + self.wind_speed_mps + ' main weather: ' + self.main_weather + \
        ' description: ' + self.description + ' icon: ' + self.icon + ' >'
        return rep
                 
                           
        

class cweather_receiver(object):
    """
    Wraps up some requests to OpenWeatherMap
    """
    url = 'http://api.openweathermap.org/data/2.5/'
    def __init__(self, key):
        self.key = key
    
    def cur_weather_by_ID(self, city_ID):
        """
        makes the request for current  weather using city ID, this needs to be 
        looked up in the city.list.json file
        """
        parameters = {'APPID' : self.key,
                      'id' : city_ID}
        results = requests.get(cweather_receiver.url + 'weather', parameters)
        if not results.ok:
            return None
        res_json = results.json()
        return self._read_weather_point(res_json)
    
    def forecast_byID(self, city_ID, key = None):
        """
        makes the request for forecast weather using city ID, this needs to be 
        looked up in the city.list.json file
        """
        parameters = {'APPID' : self.key,
                      'id' : city_ID}
        results = requests.get(cweather_receiver.url + 'forecast', parameters)
        if not results.ok:
            return None
        
        res_json = results.json()
        weathers = res_json['list']
        weather_points = []
        for weather in weathers:
            point = self._read_weather_point(weather)
            weather_points.append(point)
            
        return weather_points
    
    def _read_weather_point(self, weather):
        """
        Read single request point
        """
        unix_time = int(weather['dt'])
        date_time = datetime.datetime.fromtimestamp(unix_time)
        minT = self._get_val_check_error(weather, 'main', 'temp_min')
        maxT = self._get_val_check_error(weather, 'main', 'temp_max')
        mainT = self._get_val_check_error(weather, 'main', 'temp')
        humidity = self._get_val_check_error(weather, 'main', 'humidity')
        cloud_cover_per = self._get_val_check_error(weather, 'clouds', 'all')
        description = self._get_val_check_error(weather, 'weather', 0, 'description')
        main_weather = self._get_val_check_error(weather, 'weather', 0, 'main')
        icon = self._get_val_check_error(weather, 'weather', 0, 'icon')
        rain_mm = self._get_val_check_error(weather, 'rain', '3h')
        wind_speed_mps = self._get_val_check_error(weather, 'wind', 'speed')
        snow_mm = self._get_val_check_error(weather, 'snow', '3h')
        
        return weather_point(date_time = date_time,
                              mainT = mainT, minT = minT,
                              maxT = maxT, humidity = humidity,
                              cloud_cover_per = cloud_cover_per,
                              description = description, icon = icon,
                              main_weather = main_weather,
                              rain_mm = rain_mm, snow_mm = snow_mm,
                              wind_speed_mps = wind_speed_mps)
        
    
    def _get_val_check_error(self, dictionary, *args):
        """
        returns value from dict, returns 'None' if not present
        Probably not the most efficient way of doing this....
        """

        try:
            ret_val = dictionary
            for arg in args:
                ret_val = ret_val[arg] 
            return ret_val
        except KeyError:
            return None
        

if __name__ == '__main__':
    with open('key.txt', 'r') as txt_file:
        key = txt_file.read()
        ID = '2646557' #Horsham
        wr = cweather_receiver(key)
        #res = wr.forecast_byID(ID)
        res = wr.cur_weather_by_ID(ID)
        


