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
    response = requests.get(api_url).json()
    print(response)
    #TODO need to include catch and test case if api returns request but data is available for requested point
    forecast_url = response.get('properties', {}).get('forecastGridData')
    forecast_json = get_forecast_info(forecast_url)

    return forecast_json




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
    

if __name__ == '__main__':
    app.run(debug=True)