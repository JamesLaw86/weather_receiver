# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 12:32:17 2018

@author: James Law
"""

import requests
import datetime

class weather_point(object):
    """
    Represents a weather data point
    """
    def __init__(self, location = None,
                 date_time = None,
                 mainT = None,
                 maxT = None,
                 minT = None,
                 humidity = None,
                 cloud_cover_per = None,
                 rain_mm = None,
                 snow_mm = None,
                 wind_speed_mps = None,
                 wind_dir = None,
                 main_weather = None,
                 description = None,
                 icon = None,
                 pressure = None):
        """
        This is only a subset of what is available from the data request
        """
        self.location = str(location)
        self.date_time = date_time
        self.mainT = str(mainT)
        self.minT = str(minT)
        self.maxT = str(maxT)
        self.humidity = str(humidity)
        self.cloud_cover_per = str(cloud_cover_per)
        self.rain_mm = str(rain_mm)
        self.snow_mm = str(snow_mm)
        self.wind_speed_mps = str(wind_speed_mps)
        self.wind_dir_deg = str(wind_dir)
        self.main_weather = str(main_weather)
        self.description = str(description)
        self.icon = str(icon)
        self.pressure = str(pressure)
        #convert Kelvin to degrees celcius
        try:
            f_mainT = float(self.mainT)
            f_mainT = f_mainT - 273.15
            self.mainT = f"{f_mainT:.{2}f}"
            f_minT = float(self.minT)
            f_minT = f_minT - 273.15
            self.minT = f"{f_minT:.{2}f}"
            f_maxT = float(self.maxT)
            f_maxT = f_maxT - 273.15
            self.maxT = f"{f_maxT:.{2}f}"
        except:
            pass
            
    
    def __repr__(self):
        rep = '<location: ' + self.location + ', weather_point: time: '\
        + str(self.date_time) + ', temperature: ' + self.mainT + ', max Temp: '\
        + self.maxT + ', min Temp: ' + self.minT + ', humidity: ' + \
        self.humidity + ', % cloud cover: ' + self.cloud_cover_per + \
        ', rain mm: ' + self.rain_mm + ', snow mm: ' + self.snow_mm + \
        ', wind speed mps: ' + self.wind_speed_mps + ', main weather: ' + \
        self.main_weather + ', description: ' + self.description + ', icon: ' \
        + self.icon + ' >'
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
    
    def cur_weather_by_ID_json(self, city_ID):
        """
        makes the request for current  weather using city ID, this needs to be 
        looked up in the city.list.json file
        """
        parameters = {'APPID' : self.key,
                      'id' : city_ID}
        results = requests.get(cweather_receiver.url + 'weather', parameters)
        return results.json()
    
    def forecast_byID(self, city_ID, key = None):
        """
        makes the request for forecast weather using city ID, this needs to be 
        looked up in the city.list.json file
        """
        parameters = {'APPID' : self.key,
                      'id' : city_ID}
        results = requests.get(cweather_receiver.url + 'forecast', parameters)
        if not results.ok:
            print('error retrieving forecast')
            return None
        
        res_json = results.json()
        weathers = res_json['list']
        weather_points = []
        for weather in weathers:
            point = self._read_weather_point(weather)
            weather_points.append(point)
            
        return weather_points
    
    def forecast_byID_json(self, city_ID, key = None):
        """
        makes the request for forecast weather using city ID, this needs to be 
        looked up in the city.list.json file
        """
        parameters = {'APPID' : self.key,
                      'id' : city_ID}
        results = requests.get(cweather_receiver.url + 'forecast', parameters)
        if not results.ok:
            print('error retrieving forecast')
            return None
            
        return results.json()
    
    def _read_weather_point(self, weather):
        """
        Read single request point
        """
        location = self._get_val_check_error(weather, 'name')
        unix_time = int(self._get_val_check_error(weather, 'dt'))
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
        wind_dir = self._get_val_check_error(weather, 'wind', 'deg')
        snow_mm = self._get_val_check_error(weather, 'snow', '3h')
        pressure = self._get_val_check_error(weather, 'main', 'pressure')
        
        return weather_point(location = location, date_time = date_time,
                              mainT = mainT, minT = minT,
                              maxT = maxT, humidity = humidity,
                              cloud_cover_per = cloud_cover_per,
                              description = description, icon = icon,
                              main_weather = main_weather,
                              rain_mm = rain_mm, snow_mm = snow_mm,
                              wind_speed_mps = wind_speed_mps,
                              wind_dir = wind_dir,
                              pressure = pressure)
        
    
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
        lines = txt_file.readlines()
        key = lines[0]
        ID = '7290651'
        wr = cweather_receiver(key)
        current_weather = wr.cur_weather_by_ID(ID)
        forecast = wr.forecast_byID(ID)
        
