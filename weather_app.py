import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="🌤️ Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .weather-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }
    .temp-high {
        color: #ff6b6b;
        font-size: 2rem;
    }
    .temp-low {
        color: #4ecdc4;
        font-size: 2rem;
    }
    .weather-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        color: #856404;
        margin: 1rem 0;
        border-left: 4px solid #ffc107;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'saved_locations' not in st.session_state:
    st.session_state.saved_locations = []
if 'current_weather' not in st.session_state:
    st.session_state.current_weather = None
if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = None

# Function to get coordinates from city name
def get_coordinates(city_name):
    try:
        params = {
            "name": city_name,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        response = requests.get(GEOCODING_API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('results'):
            result = data['results'][0]
            return {
                'latitude': result['latitude'],
                'longitude': result['longitude'],
                'name': result['name'],
                'country': result.get('country', ''),
                'admin1': result.get('admin1', '')
            }
        return None
    except Exception as e:
        st.error(f"❌ Error fetching coordinates: {str(e)}")
        return None

# Function to fetch weather data
def fetch_weather_data(latitude, longitude):
    try:
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m',
            'hourly': 'temperature_2m,precipitation_probability,weather_code',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,wind_speed_10m_max',
            'timezone': 'auto',
            'forecast_days': 14
        }
        
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"❌ Error fetching weather data: {str(e)}")
        return None

# Function to get weather description from code
def get_weather_description(code):
    weather_codes = {
        0: "☀️ Clear sky",
        1: "🌤️ Mostly clear",
        2: "⛅ Partly cloudy",
        3: "☁️ Overcast",
        45: "🌫️ Foggy",
        48: "🌫️ Foggy with rime",
        51: "🌧️ Light drizzle",
        53: "🌧️ Moderate drizzle",
        55: "🌧️ Dense drizzle",
        61: "🌧️ Slight rain",
        63: "🌧️ Moderate rain",
        65: "🌧️ Heavy rain",
        71: "❄️ Slight snow",
        73: "❄️ Moderate snow",
        75: "❄️ Heavy snow",
        77: "❄️ Snow grains",
        80: "🌧️ Slight rain showers",
        81: "🌧️ Moderate rain showers",
        82: "🌧️ Violent rain showers",
        85: "❄️ Slight snow showers",
        86: "❄️ Heavy snow showers",
        95: "⛈️ Thunderstorm",
        96: "⛈️ Thunderstorm with slight hail",
        99: "⛈️ Thunderstorm with heavy hail"
    }
    return weather_codes.get(code, "Unknown")

# Function to save search history
def save_search_history(location):
    if location not in st.session_state.search_history:
        st.session_state.search_history.insert(0, location)
        if len(st.session_state.search_history) > 10:
            st.session_state.search_history.pop()

# Function to save location
def save_location(location):
    if location not in st.session_state.saved_locations:
        st.session_state.saved_locations.append(location)

# Function to display current weather
def display_current_weather(weather_data, location_info):
    current = weather_data.get('current', {})
    timezone = weather_data.get('timezone', 'UTC')
    
    st.markdown(f"<h2 class='weather-header'>📍 {location_info['name']}, {location_info['country']}</h2>", unsafe_allow_html=True)
    
    # Main weather display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🌡️ Temperature",
            f"{current.get('temperature_2m', 'N/A')}°C",
            f"Feels like {current.get('apparent_temperature', 'N/A')}°C"
        )
    
    with col2:
        st.metric(
            "💨 Wind Speed",
            f"{current.get('wind_speed_10m', 'N/A')} km/h",
            f"Direction: {current.get('wind_direction_10m', 'N/A')}°"
        )
    
    with col3:
        st.metric(
            "💧 Humidity",
            f"{current.get('relative_humidity_2m', 'N/A')}%"
        )
    
    with col4:
        st.metric(
            "🌧️ Precipitation",
            f"{current.get('precipitation', 0)} mm"
        )
    
    # Weather description
    weather_code = current.get('weather_code', 0)
    weather_desc = get_weather_description(weather_code)
    
    st.markdown(f"""
    <div class='weather-card'>
        <h3>Current Condition: {weather_desc}</h3>
        <p>Time: {current.get('time', 'N/A')} ({timezone})</p>
    </div>
    """, unsafe_allow_html=True)

# Function to display daily forecast
def display_daily_forecast(weather_data):
    st.subheader("📅 14-Day Forecast")
    
    daily = weather_data.get('daily', {})
    times = daily.get('time', [])
    temps_max = daily.get('temperature_2m_max', [])
    temps_min = daily.get('temperature_2m_min', [])
    codes = daily.get('weather_code', [])
    precip = daily.get('precipitation_sum', [])
    wind = daily.get('wind_speed_10m_max', [])
    
    # Create forecast dataframe
    forecast_df = pd.DataFrame({
        'Date': times,
        'Max Temp (°C)': temps_max,
        'Min Temp (°C)': temps_min,
        'Weather': [get_weather_description(code) for code in codes],
        'Precipitation (mm)': precip,
        'Wind (km/h)': wind
    })
    
    # Display as table
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)
    
    # Create temperature chart
    fig_temp = go.Figure()
    
    fig_temp.add_trace(go.Scatter(
        x=times,
        y=temps_max,
        name='Max Temp',
        mode='lines+markers',
        line=dict(color='#ff6b6b', width=3),
        marker=dict(size=8)
    ))
    
    fig_temp.add_trace(go.Scatter(
        x=times,
        y=temps_min,
        name='Min Temp',
        mode='lines+markers',
        line=dict(color='#4ecdc4', width=3),
        marker=dict(size=8),
        fill='tonexty',
        fillcolor='rgba(78, 205, 196, 0.2)'
    ))
    
    fig_temp.update_layout(
        title="Temperature Forecast",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Create precipitation chart
    fig_precip = go.Figure(
        data=go.Bar(
            x=times,
            y=precip,
            name='Precipitation',
            marker=dict(color='#667eea')
        )
    )
    
    fig_precip.update_layout(
        title="Precipitation Forecast",
        xaxis_title="Date",
        yaxis_title="Precipitation (mm)",
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig_precip, use_container_width=True)
    
    # Store for export
    st.session_state.forecast_data = forecast_df

# Function to display hourly forecast
def display_hourly_forecast(weather_data):
    st.subheader("⏰ 24-Hour Forecast")
    
    hourly = weather_data.get('hourly', {})
    times = hourly.get('time', [])
    temps = hourly.get('temperature_2m', [])
    precip_prob = hourly.get('precipitation_probability', [])
    
    # Get first 24 hours
    times_24 = times[:24]
    temps_24 = temps[:24]
    precip_24 = precip_prob[:24]
    
    # Create hourly chart
    fig_hourly = go.Figure()
    
    fig_hourly.add_trace(go.Scatter(
        x=times_24,
        y=temps_24,
        name='Temperature',
        mode='lines+markers',
        line=dict(color='#ff9ff3', width=2),
        marker=dict(size=6)
    ))
    
    fig_hourly.update_layout(
        title="Hourly Temperature",
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Precipitation probability
    fig_prob = go.Figure(
        data=go.Bar(
            x=times_24,
            y=precip_24,
            name='Precipitation Probability',
            marker=dict(color='#54a0ff')
        )
    )
    
    fig_prob.update_layout(
        title="Precipitation Probability (24h)",
        xaxis_title="Time",
        yaxis_title="Probability (%)",
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig_prob, use_container_width=True)

# Function to export data
def export_weather_data(weather_data, location_info):
    st.subheader("📥 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    # CSV Export
    with col1:
        if st.session_state.forecast_data is not None:
            csv = st.session_state.forecast_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"weather_{location_info['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # JSON Export
    with col2:
        json_data = json.dumps(weather_data, indent=2, default=str)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"weather_{location_info['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Report Export
    with col3:
        report_data = f"""
        WEATHER REPORT
        ==============
        Location: {location_info['name']}, {location_info['country']}
        Coordinates: ({location_info['latitude']}, {location_info['longitude']})
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        CURRENT CONDITIONS
        Current Temperature: {weather_data['current']['temperature_2m']}°C
        Feels Like: {weather_data['current']['apparent_temperature']}°C
        Weather: {get_weather_description(weather_data['current']['weather_code'])}
        Humidity: {weather_data['current']['relative_humidity_2m']}%
        Wind Speed: {weather_data['current']['wind_speed_10m']} km/h
        Precipitation: {weather_data['current']['precipitation']} mm
        """
        
        st.download_button(
            label="📥 Download Report",
            data=report_data,
            file_name=f"weather_report_{location_info['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

# ==================== MAIN APP ====================

st.markdown("<h1 class='weather-header'>🌤️ Weather Dashboard</h1>", unsafe_allow_html=True)
st.markdown("Real-time weather data from Open-Meteo API")
st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Search location
    st.subheader("🔍 Search Location")
    
    search_type = st.radio(
        "Choose input method:",
        ["Search by city", "Use saved locations", "Use coordinates"]
    )
    
    location_data = None
    
    if search_type == "Search by city":
        city_name = st.text_input(
            "Enter city name:",
            placeholder="e.g., London, Tokyo, New York"
        )
        
        if st.button("🔎 Search", key="search_btn"):
            if city_name:
                with st.spinner("Searching..."):
                    location_data = get_coordinates(city_name)
                    if location_data:
                        save_search_history(f"{location_data['name']}, {location_data['country']}")
                        st.success(f"✅ Found: {location_data['name']}, {location_data['country']}")
                    else:
                        st.error("❌ Location not found")
        
        # Recent searches
        if st.session_state.search_history:
            st.subheader("📜 Recent Searches")
            for i, location in enumerate(st.session_state.search_history[:5]):
                if st.button(f"📍 {location}", key=f"recent_{i}"):
                    parts = location.rsplit(', ', 1)
                    city = parts[0]
                    location_data = get_coordinates(city)
    
    elif search_type == "Use saved locations":
        if st.session_state.saved_locations:
            selected_location = st.selectbox(
                "Select location:",
                st.session_state.saved_locations
            )
            if st.button("📍 Load Location"):
                location_data = get_coordinates(selected_location)
        else:
            st.info("No saved locations yet. Save one from the current weather display.")
    
    else:  # Use coordinates
        lat = st.number_input("Latitude:", -90.0, 90.0, 51.5074)
        lon = st.number_input("Longitude:", -180.0, 180.0, -0.1278)
        
        if st.button("📍 Load Coordinates"):
            # Get location name from coordinates
            try:
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "format": "json"
                }
                response = requests.get("https://nominatim.openstreetmap.org/reverse", params=params, timeout=5)
                location_data = {
                    'latitude': lat,
                    'longitude': lon,
                    'name': response.json().get('address', {}).get('city', 'Unknown'),
                    'country': response.json().get('address', {}).get('country', 'Unknown')
                }
            except:
                location_data = {
                    'latitude': lat,
                    'longitude': lon,
                    'name': f"Location ({lat}, {lon})",
                    'country': 'Unknown'
                }
    
    # Display settings
    st.divider()
    st.subheader("🎨 Display Options")
    theme = st.selectbox("Theme:", ["Light", "Dark"])
    temp_unit = st.selectbox("Temperature unit:", ["°C (Celsius)", "°F (Fahrenheit)"])

# Main content
if location_data:
    # Fetch weather data
    weather_data = fetch_weather_data(location_data['latitude'], location_data['longitude'])
    
    if weather_data:
        # Store current weather
        st.session_state.current_weather = weather_data
        
        # Display current weather
        display_current_weather(weather_data, location_data)
        
        # Save location option
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("💾 Save Location"):
                save_location(f"{location_data['name']}, {location_data['country']}")
                st.success("✅ Location saved!")
        
        with col2:
            if st.button("🔄 Refresh"):
                st.rerun()
        
        st.divider()
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📅 Daily Forecast", "⏰ Hourly Forecast", "📊 Analytics", "📥 Export"])
        
        with tab1:
            display_daily_forecast(weather_data)
        
        with tab2:
            display_hourly_forecast(weather_data)
        
        with tab3:
            st.subheader("📊 Weather Analytics")
            
            daily = weather_data.get('daily', {})
            times = daily.get('time', [])
            winds = daily.get('wind_speed_10m_max', [])
            
            # Wind speed chart
            fig_wind = go.Figure(
                data=go.Scatter(
                    x=times,
                    y=winds,
                    name='Max Wind Speed',
                    mode='lines+markers',
                    line=dict(color='#a29bfe', width=3),
                    marker=dict(size=8)
                )
            )
            
            fig_wind.update_layout(
                title="Maximum Wind Speed Forecast",
                xaxis_title="Date",
                yaxis_title="Wind Speed (km/h)",
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_wind, use_container_width=True)
            
            # Summary statistics
            temps_max = daily.get('temperature_2m_max', [])
            temps_min = daily.get('temperature_2m_min', [])
            precips = daily.get('precipitation_sum', [])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🔥 Avg High Temp", f"{sum(temps_max)/len(temps_max):.1f}°C")
            
            with col2:
                st.metric("❄️ Avg Low Temp", f"{sum(temps_min)/len(temps_min):.1f}°C")
            
            with col3:
                st.metric("🌧️ Total Precipitation", f"{sum(precips):.1f} mm")
            
            with col4:
                st.metric("📈 Max Wind", f"{max(winds):.1f} km/h")
        
        with tab4:
            export_weather_data(weather_data, location_data)

else:
    st.info("""
    🌍 Welcome to the Weather Dashboard!
    
    **How to use:**
    1. Enter a city name in the sidebar (e.g., London, Paris, Tokyo)
    2. Click the Search button
    3. View current weather and forecasts
    4. Export data as CSV, JSON, or Report
    
    **Features:**
    - 📍 Real-time weather data
    - 📅 14-day forecast
    - ⏰ 24-hour forecast
    - 📊 Analytics and statistics
    - 📥 Export data in multiple formats
    - 💾 Save favorite locations
    """)

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🌐 Data from Open-Meteo API")
with col2:
    st.caption(f"⏰ Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with col3:
    st.caption("🎯 Made with Streamlit")
