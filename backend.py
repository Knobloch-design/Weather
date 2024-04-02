from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_weather_info(latitude, longitude):
    """
    Function to fetch weather information based on latitude and longitude coordinates.
    This function can be replaced with your actual weather API integration.
    """
    # Example API URL (Replace with your actual weather API URL)
    api_url = f'https://api.weather.gov/points/{latitude},{longitude}'
    
    # Make a GET request to the API endpoint
    response = requests.get(api_url)
    
    if response.status_code == 200:
        # Parse the JSON response
        weather_data = response.json()
        return weather_data
    else:
        # Return None if request was unsuccessful
        return None

@app.route('/get_weather_info', methods=['POST'])
def handle_weather_request():
    # Get latitude and longitude from the request
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    
    # Fetch weather information based on the coordinates
    weather_info = get_weather_info(latitude, longitude)
    
    if weather_info:
        # If weather information is retrieved successfully, return it as JSON response
        return jsonify(weather_info)
    else:
        # If unable to fetch weather information, return an error message
        return jsonify({'error': 'Unable to fetch weather information.'}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
