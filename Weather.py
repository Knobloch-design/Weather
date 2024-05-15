import requests
import pandas as pd
import json
import datetime
from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta
from LinkedTime import hourWeather, dayWeather
import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import matplotlib as mpl


"""Retrieves weather information for a given latitude and longitude using the National Weather Service API.
    Parameters:
        latitude (float): The latitude coordinate of the location.
        longitude (float): The longitude coordinate of the location.
    Returns:
        dict or None: A dictionary containing weather information if the request is successful. 
                    Returns None if the request fails.
"""







def get_weather_info(latitude, longitude):
    # API endpoint URL
    api_url = f'https://api.weather.gov/points/{latitude},{longitude}'

    # Make a GET request to the API endpoint
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        weather_data = response.json()
        return weather_data
    else:
        # Print an error message if the request was not successful
        print(f"Error: Unable to fetch data. Status Code: {response.status_code}")
        return None
    




""" Retrieves daylight information for a given latitude and longitude using the Sunrise-Sunset API.
    Args:
        latitude (float): The latitude coordinate of the location.
        longitude (float): The longitude coordinate of the location.
    Returns:
        dict or None: A dictionary containing daylight information if the request was successful,
        otherwise None. The dictionary typically includes keys such as 'sunrise', 'sunset', 'solar_noon', etc.,
        providing corresponding time information.
"""
def get_daylight_info(latitude, longitude):
    # API endpoint URL
    api_url = f'https://api.sunrisesunset.io/json?lat={latitude}&lng={longitude}'

    # Make a GET request to the API endpoint
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        daylight_data = response.json()
        return daylight_data
    else:
        # Print an error message if the request was not successful
        print(f"Error: Unable to fetch data. Status Code: {response.status_code}")
        return None




""" Retrieves forecast information from a provided API endpoint URL.
    Args:
        url (str): The URL of the API endpoint providing forecast data.
    Returns:
        dict or None: A dictionary containing forecast information if the request was successful,
        otherwise None. The structure of the dictionary depends on the format of the forecast data provided
        by the API.
"""

def get_forecast_info(url):
    # API endpoint URL
    api_url = url

    # Make a GET request to the API endpoint
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        forecast_data = response.json()
        return forecast_data
    else:
        # Print an error message if the request was not successful
        print(f"Error: Unable to fetch data. Status Code: {response.status_code}")
        return None




""" Analyze the type of input data and recursively analyze nested elements.
    Parameters:
    - data: dict, set, tuple, or list
    Returns:
    - dict: Dictionary containing the type of the input and the types of its elements (if any).
"""
def analyze_data_structure(data, name="", indent =0):

    result = f"{indent * '  '}{type(data).__name__}"

    if name:
        result += f" ({name})"

    if isinstance(data, (list, tuple, set)):
        for i, element in enumerate(data):
            element_name = f"{name}[{i}]" if name else f"[{i}]"
            result += f"\n{analyze_data_structure(element, element_name, indent + 1)}"
    elif isinstance(data, dict):
        for key, value in data.items():
            key_name = f"{name}['{key}']" if name else f"['{key}']"
            value_name = f"{name}['{key}']" if name else f"['{key}']"
            
            result += f"\n{indent * '  '}{analyze_data_structure(key, key_name, indent + 1)}"
            result += f"\n{indent * '  '}{analyze_data_structure(value, value_name, indent + 1)}"

    return result




""" Formats time data retrieved from a forecast JSON object.
    Args:
        input (str): The key to retrieve time data from the forecast JSON object.
        forecast_json (dict): A JSON object containing forecast data.
    Returns:
        dict: A dictionary containing formatted time data. It includes a DataFrame under the 'values' key,
        with each row representing a time interval and its corresponding data.
"""
def format_time(input,timezone):

    temp = forecast_json.get('properties',{}).get(input).get('values')
    
    for y in temp:
        start_time = y.get('validTime').split('/')
        #print(start_time[0])
        #y['validTime']=parser.parse(start_time[0])
        y['validTime']=pd.Timestamp(start_time[0],tz=timezone).tz_localize(None)

    temp = pd.DataFrame(temp)
    temp.rename(columns={'value':input}, inplace=True)



    #print('test line 155 ',out)
    #print("test line 156: ",type(out.get("values").get("validTime").loc[0]))
    return temp




if __name__ == "__main__":

    # Display the result
    # Example coordinates (replace with your desired coordinates)
    latitude = 39.6167
    longitude = -105.8486

    # Get weather information for the specified coordinates
    weather_info = get_weather_info(latitude, longitude)
    daylight_info = get_daylight_info( latitude, longitude)
    timezone = daylight_info.get('results').get('timezone')
    print(daylight_info.get('results').get('timezone'))

    # Display the retrieved data
    if weather_info:


        forecast_url = weather_info.get('properties', {}).get('forecastGridData')
        forecast_json = get_forecast_info(forecast_url)
        structure = analyze_data_structure(forecast_json)
        print("Weather Information:")
        print("Location:", weather_info.get('properties', {}).get('relativeLocation', {}).get('properties', {}).get('city'))
        print("Forecast URL:", weather_info.get('properties', {}).get('forecast'))


        
        
        
        """
        #TODO figure out why now's time is significantly different than the data's time by a couple hours 
        LinkedList = hourWeather(pd.Timestamp.now(tz = timezone).tz_localize(None))
        print("timezone1: ",pd.Timestamp.utcnow()) 
        print("timezone2: ",pd.Timestamp.now(tz = timezone).tz_localize(None))
        """


        dewPointForecast= format_time('dewpoint',timezone)
        tempForecast = format_time('temperature',timezone)
        relativeHumidityForecast = format_time('relativeHumidity',timezone)
        skyCoverForecast = format_time('skyCover',timezone)
        windSpeedForecast = format_time('windSpeed',timezone)

        weather = pd.merge(left = tempForecast,how= 'outer',right = dewPointForecast,on= 'validTime')
        weather = pd.merge(left = weather,how= 'outer',right = relativeHumidityForecast,on= 'validTime')
        weather = pd.merge(left = weather,how= 'outer',right = skyCoverForecast,on= 'validTime')
        weather = pd.merge(left = weather,how= 'outer',right = windSpeedForecast,on= 'validTime')
        
        fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
        
        x = weather['validTime']
        a = weather['temperature']
        b = weather['dewpoint']
        c = weather['skyCover']
        d = weather['relativeHumidity']
        e = weather['windSpeed']
        print(x)
        ax.plot(x, a, label='temperature')  # Plot some data on the axes.
        ax.plot(x, b, label='dewpoint')  # Plot more data on the axes...
        ax.plot(x, c, label='skyCover')  # Plot more data on the axes...
        ax.plot(x, d, label='relativeHumidity')  # Plot more data on the axes...
        ax.plot(x, e, label='windSpeed')  # Plot more data on the axes...
        ax.set_xlabel('Time')  # Add an x-label to the axes.
        ax.set_ylabel('Temperature')  # Add a y-label to the axes.
        ax.set_title("Simple Plot")  # Add a title to the axes.
        ax.legend()  # Add a legend.
        plt.show()



        #print("dewPointForecast: ",dewPointForecast)


        #weather = pd.DataFrame({"dewPointForecast": dewPointForecast})


        #print("weather: ",weather)
        #print(weather.describe())

        

        



   

        #print(weather.describe())
        #visibilityForecast = format_time('visibility',timezone)
        #weather["visibilityForecast"] = visibilityForecast

        """

        for x in weather.keys():
            LinkedList = LinkedList.getHead()

            data = weather.get(x).get('values')
            print(x)
            for y in range(len(data)):
                #print(LinkedList.getInfo())
                kwargs = {x : data.loc[y].get('value')}
                #print("timestart: ",LinkedList.timeStart)
                #print(data.loc[y].get('validTime'))

                #TODO implement function 'find next time' that finds the next equal or 
                while LinkedList.next != None and data.loc[y].get('validTime') <= LinkedList.timeStart:

                    if data.loc[y].get('validTime') == LinkedList.timeStart:
                        #print("got here")
                        LinkedList.addInfo(x,data.loc[y].get('value'))
                    LinkedList = LinkedList.next 
    
                if  LinkedList.next != None and data.loc[y].get('validTime') > LinkedList.timeStart:
                        LinkedList = LinkedList.prev
                        LinkedList.insertNext(hourWeather(timeStart=data.loc[y].get('validTime'), **kwargs))   
                else:
                    LinkedList = hourWeather(timeStart=data.loc[y].get('validTime'), **kwargs ,prev=LinkedList)

                
        
        start = LinkedList.getHead()
        while start.next != None:
            print(start.getInfo())
            start = start.next
        
        windGustForecast = format_time('windGust')
        weather["windGustForecast"] = windGustForecast
        probabilityOfPrecipitationForecast = format_time('probabilityOfPrecipitation')
        weather["probabilityOfPrecipitationForecast"] = probabilityOfPrecipitationForecast
        quantitativePrecipitationForecast = format_time('quantitativePrecipitation')
        weather["quantitativePrecipitationForecast"] = quantitativePrecipitationForecast
        ceilingHeightForecast = format_time('ceilingHeight')
        weather["ceilingHeightForecast"] = ceilingHeightForecast
        apparentTemperatureForecast = format_time('apparentTemperature')
        weather["apparentTemperatureForecast"] = apparentTemperatureForecast
        wetBulbGlobeTemperatureForecast = format_time('wetBulbGlobeTemperature')
        weather["wetBulbGlobeTemperatureForecast"] = wetBulbGlobeTemperatureForecast
        maxTemperatureForecast = format_time('maxTemperature')
        weather["maxTemperatureForecast"] = maxTemperatureForecast
        minTemperatureForecast = format_time('minTemperature')
        weather["minTemperatureForecast"] = minTemperatureForecast 
        transportWindSpeedForecast = format_time('transportWindSpeed')
        weather["transportWindSpeedForecast"] = transportWindSpeedForecast
        mixingHeightForecast = format_time('mixingHeight')
        weather["mixingHeightForecast"] = mixingHeightForecast
        hainesIndexForecast = format_time('hainesIndex')
        weather["hainesIndexForecast"] = hainesIndexForecast
        """

















    else:
        print("Failed to retrieve weather information.")
