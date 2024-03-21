import requests
import pandas as pd
import json
from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta



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


def analyze_data_structure(data,name="", indent =0):
    """
    Analyze the type of input data and recursively analyze nested elements.

    Parameters:
    - data: dict, set, tuple, or list

    Returns:
    - dict: Dictionary containing the type of the input and the types of its elements (if any).
    """
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

# Example usage:



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
    latitude = 39.6444
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


        

        tempForecast = forecast_json.get('properties',{}).get('temperature',{}).get('values')

        for x in tempForecast:
            start_time = x.get('validTime').split('/')
            x['validTime']=parser.parse(start_time[0])

        df = pd.DataFrame(tempForecast)



        dewPointForecast= format_time('dewpoint')

        maxTemperatureForecast = format_time('maxTemperature')

        minTemperatureForecast = format_time('minTemperature')

        relativeHumidityForecast = format_time('relativeHumidity')

        apparentTemperatureForecast = format_time('apparentTemperature')

        wetBulbGlobeTemperatureForecast = format_time('wetBulbGlobeTemperature')

        skyCoverForecast = format_time('skyCover')

        windSpeedForecast = format_time('windSpeed')

        windGustForecast = format_time('windGust')

        probabilityOfPrecipitationForecast = format_time('probabilityOfPrecipitation')

        quantitativePrecipitationForecast = format_time('quantitativePrecipitation')

        ceilingHeightForecast = format_time('ceilingHeight')

        visibilityForecast = format_time('visibility')

        transportWindSpeedForecast = format_time('transportWindSpeed')

        mixingHeightForecast = format_time('mixingHeight')

        hainesIndexForecast = format_time('hainesIndex')



        #print('maxTemperatureForecast; ',maxTemperatureForecast)
















    else:
        print("Failed to retrieve weather information.")
