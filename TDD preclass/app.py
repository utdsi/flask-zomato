from flask import Flask, jsonify,request

app = Flask(__name__)

weather_data = {
    'San Francisco': {'temperature': 14, 'weather': 'Cloudy'},
    'New York': {'temperature': 20, 'weather': 'Sunny'},
    'Los Angeles': {'temperature': 24, 'weather': 'Sunny'},
    'Seattle': {'temperature': 10, 'weather': 'Rainy'},
    'Austin': {'temperature': 32, 'weather': 'Hot'},
}

@app.route("/weather/<string:city>")
def get_weather(city):
    if city in weather_data:
        return jsonify(weather_data[city])
    else:
        return f"Sorry, no weather information available for {city}.", 404

@app.route("/weather", methods=["POST"])
def add_weather():
    data = request.get_json()
    if not data:
        return "Invalid request data.", 400

    city = data.get("city")
    temperature = data.get("temperature")
    weather = data.get("weather")

    if not city or not temperature or not weather:
        return "Missing required fields in the request data.", 400

    weather_data[city] = {
        "temperature": temperature,
        "weather": weather
    }
    
    return f"Weather data for {city} added successfully."  

@app.route("/weather/<string:city>", methods=["PUT"])
def update_weather(city):
    if city in weather_data:
        data = request.get_json()
        if not data:
            return "Invalid request data.", 400

        temperature = data.get("temperature")
        weather = data.get("weather")

        if temperature:
            weather_data[city]["temperature"] = temperature

        if weather:
            weather_data[city]["weather"] = weather

        return f"Weather data for {city} updated successfully."
    else:
        return f"Sorry, no weather information available for {city}.", 404  
    
    
@app.route("/weather/<string:city>", methods=["DELETE"])
def delete_weather(city):
    if city in weather_data:
        del weather_data[city]
        return f"Weather data for {city} deleted successfully."
    else:
        return f"Sorry, no weather information available for {city}.", 404
    
    
        

if __name__ == "__main__":
    app.run()

