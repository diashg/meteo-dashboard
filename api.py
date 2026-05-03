import requests


def get_city_info(city_name: str) -> dict:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,         #Premier résultat
        "language": "fr",
        "format": "json"
        }
    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        raise ValueError(f"City '{city_name}' not found")
    
    city = data["results"][0]
    
    return {
        "name": city["name"],
        "country": city["country"],
        "latitude": city["latitude"],
        "longitude": city["longitude"]
    }

def get_forecast(latitude: float, longitude: float) -> list[dict]:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode,windspeed_10m_max,relative_humidity_2m_max,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 14
    }
    response = requests.get(url, params=params)
    data = response.json()

    daily = data["daily"]
    forecast = []
    for i in range(len(daily["time"])):
        forecast.append({
            "date": daily["time"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "temp_max": daily["temperature_2m_max"][i],
            "humidity": daily["relative_humidity_2m_max"][i],
            "wind": daily["windspeed_10m_max"][i],
            "description": get_description(daily["weathercode"][i]),
            "icon": get_icon(daily["weathercode"][i])
        })
    return forecast

def get_description(code: int) -> str:
    descriptions = {
        0: "Ciel dégagé",
        1: "Principalement dégagé",
        2: "Partiellement nuageux",
        3: "Couvert",
        45: "Brouillard",
        48: "Brouillard givrant",
        51: "Bruine légère",
        53: "Bruine modérée",
        55: "Bruine dense",
        56: "Bruine légère givrant",
        57: "Bruine dense givrant",
        61: "Pluie légère",
        63: "Pluie modérée",
        65: "Pluie forte",
        66: "Pluie légère givrant",
        67: "Pluie forte givrant",
        71: "Neige légère",
        73: "Neige modérée",
        75: "Neige forte",
        77: "Grains de neige épars",
        80: "Averses de pluie légères",
        81: "Averses de pluie modérées",
        82: "Averses de pluie violentes",
        85: "Averses de neige légères",
        86: "Averses de neige fortes",
        95: "Orage",
        99: "Orage violent"
    }
    return descriptions.get(code, "Inconnu")

def get_icon(code: int) -> str: 
    if code == 0:
        return "☀️"
    if code in [1, 2]:
        return "🌤️"
    if code == 3:
        return "☁️"
    if code in [45, 48]:
        return "🌫️"
    if code in [51, 53, 55, 56, 57]:
        return "🌦️"
    if code in [61, 63, 65, 66, 67]:
        return "🌧️"
    if code in [71, 73, 75, 77]:
        return "❄️"
    if code in [80, 81, 82]:
        return "🌧️"
    if code in [85, 86]:
        return "🌧️"
    if code in [95, 99]:
        return "⛈️"
    return "Inconnu"

if __name__ == "__main__":
    city_info = get_city_info("Paris")
    print(city_info)
    forecast = get_forecast(city_info["latitude"], city_info["longitude"])
    print(forecast)