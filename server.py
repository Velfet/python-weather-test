from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

# makes the app a Flask app
app = Flask(__name__)

# default site to go to
@app.route('/')
@app.route('/index')
def index():
    # return "Hello world 😁"
    # load the index.html site
    return render_template("index.html")

@app.route('/weather')
def get_weather():
    # in Flask, the 'city' in the parameter refers to the input element's name over at the html file, not the id
    city = request.args.get('city')

    
    # check for empty strings or string with only spaces
    if not bool(city.strip()):
        # city name is empty, set default city name
        city = "London"

    weather_data = get_current_weather(city)

    # check if the city name exist in the weather data API
    if(not weather_data["cod"] == 200):
        # find city name failed
        return render_template("city-not-found.html")
    else:
        # load the weather.html site and also set some needed variables
        return render_template(
            "weather.html",
            title = weather_data["name"],
            status = weather_data["weather"][0]["description"].capitalize(),
            temp = f"{weather_data['main']['temp']:.1f}",
            feels_like = f"{weather_data['main']['feels_like']:.1f}"
        )

if(__name__ == "__main__"):
    # app.run(host="0.0.0.0", port=8000)
    serve(app, host="0.0.0.0", port=8000)