import requests
import pandas as pd
import json
from datetime import date




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



if __name__ == "__main__":


    # Display the result
    # Example coordinates (replace with your desired coordinates)
    latitude = 39.6444
    longitude = -105.8486

    # Get weather information for the specified coordinates
    weather_info = get_weather_info(latitude, longitude)
    #structure = analyze_data_structure(weather_info)
    #print(structure,'weather data')
    #print("test", weather_info)
    # Display the retrieved data
    if weather_info:
        forecast_url = weather_info.get('properties', {}).get('forecastGridData')
        forecast_json = get_forecast_info(forecast_url)
        structure = analyze_data_structure(forecast_json)
        print("Weather Information:")
        print("Location:", weather_info.get('properties', {}).get('relativeLocation', {}).get('properties', {}).get('city'))
        print("Forecast URL:", weather_info.get('properties', {}).get('forecast'))
        #print("Forecast:", structure)

        

        tempForecast = forecast_json.get('properties',{}).get('temperature',{}).get('values')
        df = pd.DataFrame(tempForecast)
        print(df)


        print(type(df.loc[1].get('validTime')))
        dewPointForecast = forecast_json.get('properties',{}).get('dewpoint')
        maxTemperatureForecast = forecast_json.get('properties',{}).get('maxTemperature')
        minTemperatureForecast = forecast_json.get('properties',{}).get('minTemperature')
        relativeHumidityForecast = forecast_json.get('properties',{}).get('relativeHumidity')
        apparentTemperatureForecast = forecast_json.get('properties',{}).get('apparentTemperature')
        wetBulbGlobeTemperatureForecast = forecast_json.get('properties',{}).get('wetBulbGlobeTemperature')
        skyCoverForecast = forecast_json.get('properties',{}).get('skyCover')
        windSpeedForecast = forecast_json.get('properties',{}).get('windSpeed')
        windGustForecast = forecast_json.get('properties',{}).get('windGust')
        probabilityOfPrecipitationForecast = forecast_json.get('properties',{}).get('probabilityOfPrecipitation')
        quantitativePrecipitationForecast = forecast_json.get('properties',{}).get('quantitativePrecipitation')
        ceilingHeightForecast = forecast_json.get('properties',{}).get('ceilingHeight')
        visibilityForecast = forecast_json.get('properties',{}).get('visibility')
        transportWindSpeedForecast = forecast_json.get('properties',{}).get('transportWindSpeed')
        mixingHeightForecast = forecast_json.get('properties',{}).get('mixingHeight')
        hainesIndexForecast = forecast_json.get('properties',{}).get('hainesIndex')

















    else:
        print("Failed to retrieve weather information.")
