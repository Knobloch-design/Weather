import requests
import pandas as pd
import json
import datetime
from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta
from LinkedTime import hourWeather, dayWeather



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
def format_time(input):


    temp = forecast_json.get('properties',{}).get(input).get('values')

    for y in temp:
        start_time = y.get('validTime').split('/')
        y['validTime']=parser.parse(start_time[0])
    
    out = forecast_json.get('properties',{}).get(input)
    out['values'] = pd.DataFrame(temp)
    
    return out




if __name__ == "__main__":

    # Display the result
    # Example coordinates (replace with your desired coordinates)
    latitude = 39.6167
    longitude = -105.8486

    # Get weather information for the specified coordinates
    weather_info = get_weather_info(latitude, longitude)
    daylight_info = get_daylight_info( latitude, longitude)
    print(daylight_info)

    # Display the retrieved data
    if weather_info:


        forecast_url = weather_info.get('properties', {}).get('forecastGridData')
        forecast_json = get_forecast_info(forecast_url)
        structure = analyze_data_structure(forecast_json)
        print("Weather Information:")
        print("Location:", weather_info.get('properties', {}).get('relativeLocation', {}).get('properties', {}).get('city'))
        print("Forecast URL:", weather_info.get('properties', {}).get('forecast'))


        
        
        tempForecast = format_time('temperature')


        LinkedList = hourWeather(datetime.now())



        #print("test: ",LinkedList.prev.temp)

            

        #for x in tempForecast:
        #    node = hourWeather

        
        dewPointForecast= format_time('dewpoint')
        weather = {"dewPointForecast": dewPointForecast}
        weather["tempForecast"] = tempForecast
        relativeHumidityForecast = format_time('relativeHumidity')
        weather["relativeHumidityForecast"] = relativeHumidityForecast
        skyCoverForecast = format_time('skyCover')
        weather["skyCoverForecast"] = skyCoverForecast
        windSpeedForecast = format_time('windSpeed')
        weather["windSpeedForecast"] = windSpeedForecast
        visibilityForecast = format_time('visibility')
        weather["visibilityForecast"] = visibilityForecast



        for x in weather.keys():
            print(x)
            data = weather.get(x).get('values')
            #print(data)
            for y in range(len(data)):
                kwargs = {str(x) : data.loc[y].get('value')}
                if data.loc[y].get('validTime') < LinkedList.next.timeStart:
                    LinkedList.insertNext(hourWeather(timeStart=data.loc[y].get('validTime'), **kwargs))

                
                LinkedList = hourWeather(timeStart=data.loc[y].get('validTime'), **kwargs ,prev=LinkedList)



        """
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
