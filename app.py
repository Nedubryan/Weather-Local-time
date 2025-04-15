import streamlit as st
import requests

# API keys (replace with yours)
OPENWEATHER_API_KEY = "94a0c14826e793cf805cd168ad54e0f1"
TIMEZONEDB_API_KEY = "MFHTKFQMPFLW"

st.set_page_config(page_title="Global Weather & Time Agent 🌍", page_icon="⏰")
st.title("🤖 AI Agent: Weather & Local Time by City")
st.write("Type in any city in the world to get the current weather and time zone.")

city = st.text_input("Enter city name", placeholder="e.g. Tokyo, London, Lagos")

# --- Get Weather Data ---
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        return {
            "weather": f"{weather}, {temp}°C, Humidity: {humidity}%",
            "lat": lat,
            "lon": lon
        }
    else:
        return None

# --- Get Time from Coordinates using TimeZoneDB ---
def get_time(lat, lon):
    url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={TIMEZONEDB_API_KEY}&format=json&by=position&lat={lat}&lng={lon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("formatted", "Time unavailable")
    return "Time unavailable"

# --- Main App Logic ---
if city:
    st.info(f"🔍 Fetching data for {city.title()}...")

    weather_data = get_weather(city)
    if weather_data:
        st.success(f"🌤️ Weather in {city.title()}: {weather_data['weather']}")
        time_string = get_time(weather_data["lat"], weather_data["lon"])
        st.success(f"⏰ Local Time in {city.title()}: {time_string}")
    else:
        st.error("❌ Could not find data for that city. Please check the spelling and try again.")