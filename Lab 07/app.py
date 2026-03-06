from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            city = city.strip()

            try:
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
                geo_response = requests.get(geo_url, timeout=10)
                geo_response.raise_for_status()
                geo_data = geo_response.json()

                if 'results' not in geo_data or len(geo_data['results']) == 0:
                    error = "City not found. Try another city."
                else:
                    lat = geo_data['results'][0]['latitude']
                    lon = geo_data['results'][0]['longitude']
                    
                    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                    weather_response = requests.get(weather_url, timeout=10)
                    weather_response.raise_for_status()
                    weather_json = weather_response.json()

                    current = weather_json['current_weather']
                    weather_data = {
                        'city': city.title(),
                        'temperature': current['temperature'],
                        'windspeed': current['windspeed'],
                        'weathercode': current['weathercode']
                    }

            except requests.exceptions.Timeout:
                error = "The server took too long to respond. Try again."
            except requests.exceptions.ConnectionError:
                error = "Network error: Could not connect to weather server."
            except requests.exceptions.RequestException as e:
                error = f"Error fetching weather: {e}"
            except KeyError:
                error = "Weather data not available for this city."

    return render_template('index.html', weather=weather_data, error=error)


if __name__ == '__main__':
    app.run(debug=True)