from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/weather', methods=['GET'])
def get_weather():

    variable_value = request.args.get('position')

    longitude,latitude = variable_value.split(",")
    longitude,latitude = float(longitude),float(latitude)

    api_url = f'https://api.weather.gov/points/{latitude},{longitude}'
    response = requests.get(api_url)

    print(response)
    
    if response.status_code == 200:
        # Parse the JSON response
        weather_data = response.json()
        return weather_data
    else:
        # Print an error message if the request was not successful
        print(f"Error: Unable to fetch data. Status Code: {response.status_code}")
        return None





@app.route('/backend', methods=['GET'])
def get_weather_info():
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
