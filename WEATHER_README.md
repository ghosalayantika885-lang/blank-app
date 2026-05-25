# 🌤️ Weather Dashboard

A comprehensive, real-time weather dashboard built with Streamlit that fetches data from the Open-Meteo API.

![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

---

## ✨ Features

### 🌍 Real-time Weather Data
- Current temperature, humidity, wind speed
- Apparent temperature (feels like)
- Precipitation data
- Weather conditions with emoji indicators

### 📅 14-Day Forecast
- Daily high and low temperatures
- Precipitation predictions
- Weather conditions
- Wind speed forecasts
- Interactive temperature charts

### ⏰ 24-Hour Hourly Forecast
- Hourly temperature changes
- Precipitation probability
- Real-time trends

### 📊 Weather Analytics
- Average temperature analysis
- Wind speed statistics
- Precipitation totals
- Weather trend visualization

### 💾 Location Management
- Save favorite locations
- Search history (last 10 searches)
- Search by coordinates
- Quick location switching

### 📥 Data Export
- Export as CSV
- Export as JSON
- Generate weather report (TXT)
- Multiple download formats

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

### Installation

#### Windows
```bash
# Clone or download the repository
cd weather-dashboard

# Create virtual environment
python -m venv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r weather_requirements.txt

# Run the app
streamlit run weather_app.py
```

#### Mac/Linux
```bash
# Clone or download the repository
cd weather-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r weather_requirements.txt

# Run the app
streamlit run weather_app.py
```

### Access the App
The app will automatically open in your browser at:
```
http://localhost:8501
```

---

## 📚 How to Use

### 1. Search for a Location

**Method 1: Search by City Name**
- Enter city name in the sidebar (e.g., "London", "Tokyo", "New York")
- Click the "🔎 Search" button
- View the weather for that location

**Method 2: Use Saved Locations**
- First search a location and save it
- Select from saved locations in the sidebar
- Click "📍 Load Location"

**Method 3: Use Coordinates**
- Enter latitude and longitude
- Click "📍 Load Coordinates"
- View weather for that location

### 2. View Current Weather
The dashboard displays:
- Current temperature and feels-like temperature
- Wind speed and direction
- Humidity percentage
- Precipitation level
- Weather conditions with icons

### 3. Check Forecasts

**Daily Forecast Tab:**
- 14-day outlook
- High and low temperatures
- Precipitation predictions
- Wind speed forecasts
- Temperature trend chart
- Precipitation bar chart

**Hourly Forecast Tab:**
- Next 24 hours temperature
- Precipitation probability
- Hourly trends

### 4. View Analytics
- Average high and low temperatures
- Total precipitation forecast
- Maximum wind speed
- Weather statistics and trends

### 5. Export Data
- **CSV Format**: Open in Excel or Google Sheets
- **JSON Format**: For developers or data processing
- **Text Report**: Human-readable weather report

---

## 🎨 Features Explanation

### Temperature Display
- **Red color**: High temperatures
- **Blue color**: Low temperatures
- **Charts**: Visual trends over time

### Weather Indicators
- ☀️ Clear sky
- 🌤️ Mostly clear
- ⛅ Partly cloudy
- ☁️ Overcast
- 🌧️ Rain conditions
- ❄️ Snow conditions
- ⛈️ Thunderstorms
- 🌫️ Fog conditions

### Wind Direction
- 0°: North
- 90°: East
- 180°: South
- 270°: West

---

## 📊 Data Visualization

### Interactive Charts
- **Temperature Chart**: Line chart with min/max range
- **Precipitation Chart**: Bar chart for rainfall/snowfall
- **Wind Speed Chart**: Line chart for wind trends
- **Hourly Charts**: Detailed 24-hour trends

### Hover Information
Hover over charts to see:
- Exact values
- Date and time
- Multiple data points simultaneously

---

## 🔌 API Information

### Open-Meteo API
- **Base URL**: https://api.open-meteo.com/v1/forecast
- **Geocoding URL**: https://geocoding-api.open-meteo.com/v1/search
- **Benefits**:
  - No API key required
  - Free to use
  - Accurate weather data
  - Global coverage
  - Open-source

### Data Parameters
- Current weather (14 parameters)
- Hourly forecast (72+ hours)
- Daily forecast (16 days)
- 400+ locations

---

## 💾 File Structure

```
weather-dashboard/
├── weather_app.py              # Main application
├── weather_requirements.txt    # Python dependencies
├── WEATHER_README.md           # This documentation
├── .env.example                # Environment variables template
├── .env                        # Your API keys (create this)
└── weather_dashboard.py        # Alternative app version
```

---

## ⚙️ Configuration

### Environment Variables

1. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

2. Add your API keys (optional):
```
WEATHER_API_KEY=your_api_key_here
```

### Settings in Sidebar
- **Theme**: Light/Dark mode
- **Temperature Unit**: Celsius or Fahrenheit
- **Location Management**: Save/view locations

---

## 🎯 Use Cases

### 1. Weather Monitoring
- Track weather patterns
- Plan outdoor activities
- Monitor extreme weather

### 2. Travel Planning
- Check destination weather
- Plan for different climates
- Pack appropriate clothing

### 3. Business Intelligence
- Weather-dependent planning
- Agricultural forecasting
- Event planning

### 4. Educational
- Learn weather patterns
- Study climate data
- Data visualization practice

### 5. Research
- Historical weather analysis
- Climate trends
- Data export for analysis

---

## 🐛 Troubleshooting

### Issue: "Connection Error"
**Solution**: 
- Check internet connection
- Verify Open-Meteo API is online
- Try a different location

### Issue: "Location Not Found"
**Solution**:
- Use exact city name
- Try country name
- Use coordinates instead
- Check spelling

### Issue: "Module Not Found"
**Solution**:
```bash
pip install -r weather_requirements.txt --force-reinstall
```

### Issue: "Port Already in Use"
**Solution**:
```bash
streamlit run weather_app.py --server.port 8502
```

### Issue: "Slow Loading"
**Solution**:
- Check internet connection
- API might be busy
- Try different location
- Refresh the page

---

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (FREE)
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Deploy with one click
4. Get public URL

### Option 2: Docker
```bash
docker build -t weather-dashboard .
docker run -p 8501:8501 weather-dashboard
```

### Option 3: Heroku
```bash
heroku create
git push heroku main
```

---

## 📱 Responsive Design
- ✅ Works on desktop
- ✅ Works on tablet
- ✅ Works on mobile
- ✅ Touch-friendly buttons
- ✅ Responsive charts

---

## 🔒 Privacy & Security

- ✅ No personal data collected
- ✅ API calls only for weather data
- ✅ Local data processing
- ✅ No third-party tracking
- ✅ HTTPS encrypted connections

---

## 📈 Performance

- **Initial Load**: ~2-3 seconds
- **Location Search**: ~1-2 seconds
- **Data Refresh**: ~2-3 seconds
- **Charts Rendering**: ~1 second
- **Export**: Instant

---

## 🎓 Learning Resources

### For Developers
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python)
- [Open-Meteo API Docs](https://open-meteo.com/en/docs)
- [Python Requests Library](https://requests.readthedocs.io)

---

## 🤝 Contributing

Want to improve the dashboard?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🎉 Version History

### v1.0.0 (Current)
- ✅ Real-time weather display
- ✅ 14-day forecast
- ✅ Hourly forecast
- ✅ Weather analytics
- ✅ Data export
- ✅ Location management
- ✅ Interactive charts

---

## 📞 Support

Need help?
1. Check this README
2. Review troubleshooting section
3. Check Streamlit documentation
4. Visit Open-Meteo API docs

---

## 🌟 Credits

- **Weather Data**: [Open-Meteo](https://open-meteo.com)
- **Geocoding**: [Open-Meteo Geocoding](https://open-meteo.com/en/docs/geocoding-api)
- **Maps**: [Nominatim/OpenStreetMap](https://nominatim.org)
- **Charts**: [Plotly](https://plotly.com)
- **Web Framework**: [Streamlit](https://streamlit.io)

---

**Enjoy exploring the weather! 🌍🌤️**
