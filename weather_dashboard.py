# Alternative weather dashboard with advanced features
import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from pytz import timezone as tz
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Advanced Weather Dashboard",
    page_icon="🌡️",
    layout="wide"
)

# Caching functions for performance
@st.cache_data(ttl=3600)
def get_weather_data(lat, lon):
    """Cache weather data for 1 hour"""
    try:
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m',
            'hourly': 'temperature_2m,precipitation_probability,weather_code',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,wind_speed_10m_max',
            'timezone': 'auto',
            'forecast_days': 14
        }
        response = requests.get('https://api.open-meteo.com/v1/forecast', params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching weather: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_city_coordinates(city):
    """Cache city coordinates for 1 hour"""
    try:
        params = {
            'name': city,
            'count': 1,
            'language': 'en',
            'format': 'json'
        }
        response = requests.get('https://geocoding-api.open-meteo.com/v1/search', params=params, timeout=5)
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
        st.error(f"Error finding city: {str(e)}")
        return None

# UI Configuration
st.markdown("""
<style>
    .main { max-width: 1400px; }
    .metric { text-align: center; padding: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("🌡️ Advanced Weather Dashboard")

# Sidebar
with st.sidebar:
    st.header("Search Settings")
    search_method = st.radio("Search by:", ["City Name", "Coordinates"])
    
    location_info = None
    
    if search_method == "City Name":
        city = st.text_input("Enter city name:", "London")
        if st.button("Search", use_container_width=True):
            location_info = get_city_coordinates(city)
            if not location_info:
                st.error("City not found")
    else:
        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input("Latitude:", -90.0, 90.0, 51.5074)
        with col2:
            lon = st.number_input("Longitude:", -180.0, 180.0, -0.1278)
        
        if st.button("Load", use_container_width=True):
            location_info = {
                'latitude': lat,
                'longitude': lon,
                'name': f"Location ({lat}, {lon})",
                'country': 'Coordinates',
                'admin1': ''
            }
    
    # Display options
    st.divider()
    st.subheader("Display Options")
    temp_unit = st.selectbox("Temperature:", ["Celsius", "Fahrenheit"])
    speed_unit = st.selectbox("Speed:", ["km/h", "mph", "m/s"])

if location_info:
    weather = get_weather_data(location_info['latitude'], location_info['longitude'])
    
    if weather:
        current = weather['current']
        
        # Header
        st.markdown(f"### 📍 {location_info['name']}, {location_info['country']}")
        
        # Main metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("🌡️ Temperature", f"{current['temperature_2m']}°C")
        with col2:
            st.metric("🤔 Feels Like", f"{current['apparent_temperature']}°C")
        with col3:
            st.metric("💨 Wind", f"{current['wind_speed_10m']} km/h")
        with col4:
            st.metric("💧 Humidity", f"{current['relative_humidity_2m']}%")
        with col5:
            st.metric("🌧️ Rain", f"{current['precipitation']} mm")
        
        st.divider()
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Charts", "📅 Forecast", "📈 Stats", "💾 Export"])
        
        with tab1:
            st.subheader("Weather Charts")
            
            daily = weather['daily']
            
            # Temperature chart
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(x=daily['time'], y=daily['temperature_2m_max'], name='Max Temp', line=dict(color='red')))
            fig_temp.add_trace(go.Scatter(x=daily['time'], y=daily['temperature_2m_min'], name='Min Temp', line=dict(color='blue'), fill='tonexty'))
            fig_temp.update_layout(title="Temperature Forecast", xaxis_title="Date", yaxis_title="°C", height=400)
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Precipitation chart
            fig_precip = go.Figure(data=go.Bar(x=daily['time'], y=daily['precipitation_sum'], name='Precipitation'))
            fig_precip.update_layout(title="Precipitation Forecast", xaxis_title="Date", yaxis_title="mm", height=400)
            st.plotly_chart(fig_precip, use_container_width=True)
            
            # Wind speed chart
            fig_wind = go.Figure(data=go.Scatter(x=daily['time'], y=daily['wind_speed_10m_max'], mode='lines+markers', name='Wind Speed'))
            fig_wind.update_layout(title="Wind Speed Forecast", xaxis_title="Date", yaxis_title="km/h", height=400)
            st.plotly_chart(fig_wind, use_container_width=True)
        
        with tab2:
            st.subheader("14-Day Forecast")
            
            forecast_df = pd.DataFrame({
                'Date': daily['time'],
                'Max (°C)': daily['temperature_2m_max'],
                'Min (°C)': daily['temperature_2m_min'],
                'Precip (mm)': daily['precipitation_sum'],
                'Wind (km/h)': daily['wind_speed_10m_max']
            })
            
            st.dataframe(forecast_df, use_container_width=True, hide_index=True)
        
        with tab3:
            st.subheader("Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            temps_max = daily['temperature_2m_max']
            temps_min = daily['temperature_2m_min']
            precips = daily['precipitation_sum']
            winds = daily['wind_speed_10m_max']
            
            with col1:
                st.metric("Avg High", f"{sum(temps_max)/len(temps_max):.1f}°C")
            with col2:
                st.metric("Avg Low", f"{sum(temps_min)/len(temps_min):.1f}°C")
            with col3:
                st.metric("Total Rain", f"{sum(precips):.1f} mm")
            with col4:
                st.metric("Max Wind", f"{max(winds):.1f} km/h")
        
        with tab4:
            st.subheader("Export Data")
            
            # CSV export
            csv_data = forecast_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"weather_{location_info['name']}.csv",
                mime="text/csv"
            )
            
            # JSON export
            json_data = json.dumps(weather, indent=2, default=str)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"weather_{location_info['name']}.json",
                mime="application/json"
            )
else:
    st.info("👈 Enter a location in the sidebar to get started!")
