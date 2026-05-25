# Example functions for using Open-Meteo API
# Use these in your own projects

import requests
import json
from datetime import datetime

# ====================
# BASIC API CALLS
# ====================

def get_current_weather(latitude, longitude):
    """
    Get current weather for coordinates
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    
    Returns:
        dict: Current weather data
    
    Example:
        weather = get_current_weather(51.5074, -0.1278)
        print(weather['current']['temperature_2m'])
    """
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m',
        'timezone': 'auto'
    }
    response = requests.get('https://api.open-meteo.com/v1/forecast', params=params)
    return response.json()

def get_forecast(latitude, longitude, days=7):
    """
    Get weather forecast
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        days (int): Number of days (1-16)
    
    Returns:
        dict: Forecast data
    """
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code',
        'timezone': 'auto',
        'forecast_days': min(days, 16)
    }
    response = requests.get('https://api.open-meteo.com/v1/forecast', params=params)
    return response.json()

def search_city(city_name):
    """
    Search for a city's coordinates
    
    Args:
        city_name (str): Name of the city
    
    Returns:
        dict: City information with coordinates
    
    Example:
        city = search_city('London')
        print(city['latitude'], city['longitude'])
    """
    params = {
        'name': city_name,
        'count': 1,
        'language': 'en',
        'format': 'json'
    }
    response = requests.get('https://geocoding-api.open-meteo.com/v1/search', params=params)
    data = response.json()
    if data.get('results'):
        return data['results'][0]
    return None

# ====================
# ADVANCED EXAMPLES
# ====================

def get_detailed_weather(city_name):
    """
    Get comprehensive weather data for a city
    
    Returns current + forecast + hourly data
    """
    # Search for city
    city = search_city(city_name)
    if not city:
        return None
    
    # Get comprehensive data
    params = {
        'latitude': city['latitude'],
        'longitude': city['longitude'],
        'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m',
        'hourly': 'temperature_2m,precipitation_probability,weather_code',
        'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,wind_speed_10m_max',
        'timezone': 'auto',
        'forecast_days': 14
    }
    
    response = requests.get('https://api.open-meteo.com/v1/forecast', params=params)
    data = response.json()
    
    # Add city info
    data['city'] = city
    
    return data

def compare_cities_temperature(cities, days=7):
    """
    Compare temperatures across multiple cities
    
    Args:
        cities (list): List of city names
        days (int): Number of days to forecast
    
    Returns:
        dict: Comparison data
    """
    comparison = {}
    
    for city in cities:
        city_data = search_city(city)
        if city_data:
            weather = get_forecast(
                city_data['latitude'],
                city_data['longitude'],
                days
            )
            comparison[city] = {
                'current_temp': None,  # Would need current endpoint
                'forecast': weather['daily']
            }
    
    return comparison

def get_weather_alerts(city_name):
    """
    Check for severe weather conditions
    
    Returns alerts if:
    - Temperature extremely high/low
    - Heavy precipitation
    - Strong winds
    """
    weather = get_detailed_weather(city_name)
    if not weather:
        return None
    
    alerts = []
    current = weather['current']
    
    # Temperature alerts
    if current['temperature_2m'] > 35:
        alerts.append("🔥 Heat warning: High temperature")
    elif current['temperature_2m'] < -20:
        alerts.append("❄️ Cold warning: Very low temperature")
    
    # Wind alerts
    if current['wind_speed_10m'] > 50:
        alerts.append("💨 Strong wind warning")
    
    # Precipitation alerts
    if current['precipitation'] > 10:
        alerts.append("🌧️ Heavy rain warning")
    
    return alerts if alerts else None

# ====================
# UTILITY FUNCTIONS
# ====================

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def kmh_to_mph(kmh):
    """Convert km/h to mph"""
    return kmh * 0.621371

def get_weather_description(code):
    """
    Get human-readable weather description
    
    Args:
        code (int): WMO weather code
    
    Returns:
        str: Weather description
    """
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy with rime",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail"
    }
    return codes.get(code, "Unknown")

def format_weather_report(weather_data):
    """
    Format weather data as readable report
    """
    city = weather_data['city']
    current = weather_data['current']
    
    report = f"""
    WEATHER REPORT
    ==============
    Location: {city['name']}, {city['country']}
    Time: {current['time']}
    
    Current Conditions:
    - Temperature: {current['temperature_2m']}°C
    - Feels Like: {current['apparent_temperature']}°C
    - Condition: {get_weather_description(current['weather_code'])}
    - Humidity: {current['relative_humidity_2m']}%
    - Wind: {current['wind_speed_10m']} km/h from {current['wind_direction_10m']}°
    - Precipitation: {current['precipitation']} mm
    """
    
    return report

# ====================
# USAGE EXAMPLES
# ====================

if __name__ == "__main__":
    # Example 1: Get current weather
    print("Example 1: Current Weather")
    weather = get_current_weather(51.5074, -0.1278)
    print(json.dumps(weather, indent=2))
    
    # Example 2: Search city
    print("\nExample 2: Search City")
    city = search_city("Paris")
    print(f"Paris: {city['latitude']}, {city['longitude']}")
    
    # Example 3: Get detailed weather
    print("\nExample 3: Detailed Weather")
    weather = get_detailed_weather("Tokyo")
    print(format_weather_report(weather))
    
    # Example 4: Get alerts
    print("\nExample 4: Weather Alerts")
    alerts = get_weather_alerts("Dubai")
    if alerts:
        for alert in alerts:
            print(alert)
    
    # Example 5: Compare cities
    print("\nExample 5: Compare Cities")
    comparison = compare_cities_temperature(["London", "Paris", "Berlin"])
    for city, data in comparison.items():
        print(f"{city}: Max {max(data['forecast']['temperature_2m_max'])}°C")
