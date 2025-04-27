# js8_band_predictor.py

from datetime import datetime
import gpsd
import time
from timezonefinder import TimezoneFinder
import pytz
import requests
import xml.etree.ElementTree as ET
import socket
import json
from typing import Optional, Tuple
import os
from dotenv import load_dotenv
from JS8CallAPI import JS8CallAPI

# Load environment variables
load_dotenv()

# Simplified table of JS8Call standard frequencies by band (in MHz)
JS8_BANDS = {
    "160m": 1.846,
    "80m": 3.578,
    "40m": 7.078,
    "30m": 10.130,
    "20m": 14.078,
    "17m": 18.104,
    "15m": 21.078,
    "12m": 24.922,
    "10m": 28.078,
    "6m": 50.318,
    "2m": 144.178
}

def check_internet_connection() -> bool:
    """Check if there is an active internet connection."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def fetch_weather_data(lat: float, lon: float) -> Optional[Tuple[float, str]]:
    """Fetch weather data from OpenWeatherMap API based on GPS coordinates."""
    try:
        api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        if not api_key:
            return None
            
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        temperature = data['main']['temp']
        weather = data['weather'][0]['main'].lower()
        return temperature, weather
    except Exception:
        return None

def fetch_hamqsl_conditions() -> Optional[Tuple[Optional[float], Optional[int], Optional[float]]]:
    """Fetch solar conditions from HamQSL API."""
    try:
        url = "https://www.hamqsl.com/solarxml.php"
        response = requests.get(url, timeout=5)
        root = ET.fromstring(response.content)
        
        # Get solar flux
        solarflux_elem = root.find('solardata/solarflux')
        solarflux = float(solarflux_elem.text) if solarflux_elem is not None and solarflux_elem.text != 'NoRpt' else None
        
        # Get K-index
        kindex_elem = root.find('solardata/kindex')
        kindex = int(kindex_elem.text) if kindex_elem is not None and kindex_elem.text != 'NoRpt' else None
        
        # Get MUF
        muf_elem = root.find('solardata/muf')
        muf = float(muf_elem.text) if muf_elem is not None and muf_elem.text != 'NoRpt' else None
        
        return solarflux, kindex, muf
    except Exception as e:
        print(f"Error fetching HamQSL data: {e}")
        return None

def predict_band_with_solar_data(muf: Optional[float], utc_hour: int, solarflux: Optional[float], kindex: Optional[int]) -> str:
    """Predict band based on solar conditions."""
    # Convert UTC hour to local hour (assuming EST/EDT for now)
    local_hour = (utc_hour - 5) % 24  # UTC-5 for EST
    
    # If we have MUF, use it
    if muf is not None and kindex is not None:
        adjusted_muf = muf * (1 - (kindex * 0.1))
        
        if adjusted_muf >= 28:
            return "10m"
        elif adjusted_muf >= 21:
            return "15m"
        elif adjusted_muf >= 14:
            return "20m"
        elif adjusted_muf >= 10:
            return "30m"
        elif adjusted_muf >= 7:
            return "40m"
        else:
            return "80m" if local_hour >= 18 or local_hour <= 6 else "40m"
    
    # If we don't have MUF but have solar flux and K-index, use them for prediction
    if solarflux is not None and kindex is not None:
        if solarflux > 150 and kindex <= 2:
            return "15m" if 10 <= local_hour <= 16 else "20m"
        elif solarflux > 100 and kindex <= 3:
            return "20m" if 10 <= local_hour <= 16 else "30m"
        elif solarflux > 80 and kindex <= 4:
            return "30m" if 10 <= local_hour <= 16 else "40m"
        else:
            return "40m" if 10 <= local_hour <= 16 else "80m"
    
    return None

def predict_band(utc_hour: int, latitude: float, temperature: float = None, weather: str = None) -> str:
    """Simple model that uses time of day, latitude, and optional environmental factors."""
    # Convert UTC hour to local hour (assuming EST/EDT for now)
    local_hour = (utc_hour - 5) % 24  # UTC-5 for EST
    day = 7 <= local_hour <= 18
    high_lat = abs(latitude) > 45

    if not day:
        if high_lat:
            return "80m"
        return "40m"
    elif 10 <= local_hour <= 16:
        if temperature and temperature > 85 and weather == "sunny":
            return "10m"
        return "20m"
    elif day:
        return "30m"
    return "40m"

def get_timezone_name(lat: float, lon: float) -> str:
    """Get timezone name based on latitude and longitude."""
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=lat, lng=lon)
    return timezone_str if timezone_str else "UTC"

def get_gps_data() -> tuple[float, float, datetime]:
    """Fetch latitude, longitude, and time from GPSD."""
    try:
        # Try to connect to gpsd with a timeout
        try:
            gpsd.connect(host='127.0.0.1', port=2947, timeout=5)
        except Exception as e:
            print("Warning: Could not connect to gpsd. Please check if:")
            print("1. gpsd service is running (sudo systemctl status gpsd)")
            print("2. GPS device is connected and has proper permissions")
            print("3. GPS device is providing valid data")
            raise RuntimeError(f"GPS Connection Error: {e}")

        try:
            packet = gpsd.get_current()
            if packet.mode < 2:
                print("Warning: No GPS fix available. Please check if:")
                print("1. GPS antenna is properly connected")
                print("2. You have a clear view of the sky")
                print("3. GPS device is properly configured")
                raise RuntimeError("No GPS fix available")
            
            try:
                if isinstance(packet.time, str):
                    # Parse ISO format time string and ensure it's UTC
                    gps_time = datetime.fromisoformat(packet.time.replace('Z', '+00:00'))
                    if gps_time.tzinfo is None:
                        gps_time = gps_time.replace(tzinfo=pytz.UTC)
                else:
                    # Convert timestamp to UTC datetime
                    gps_time = datetime.fromtimestamp(float(packet.time), tz=pytz.UTC)
                
                # Validate GPS time against system time
                system_time = datetime.now(pytz.UTC)
                time_diff = abs((gps_time - system_time).total_seconds())
                
                # If GPS time is more than 5 minutes off, use system time
                if time_diff > 300:  # 5 minutes in seconds
                    print("Warning: GPS time appears incorrect, using system time")
                    gps_time = system_time
                    
            except (ValueError, TypeError) as e:
                print(f"Warning: Error parsing GPS time: {e}")
                print("Using system time instead")
                gps_time = datetime.now(pytz.UTC)
                
            return packet.lat, packet.lon, gps_time
            
        except Exception as e:
            print(f"Warning: Error getting GPS data: {e}")
            print("Using default location and system time")
            return 40.9, -74.3, datetime.now(pytz.UTC)
            
    except Exception as e:
        print(f"Warning: GPS Error: {e}")
        print("Using default location and system time")
        return 40.9, -74.3, datetime.now(pytz.UTC)

def recommend_js8_band(latitude: float, longitude: float, utc_time: datetime) -> tuple[str, float]:
    """Recommend a JS8Call band based on current conditions."""
    utc_hour = utc_time.hour
    temperature = None
    weather = None
    
    if False: #check_internet_connection():
        weather_data = fetch_weather_data(latitude, longitude)
        if weather_data:
            temperature, weather = weather_data
        
        solar_data = fetch_hamqsl_conditions()
        if solar_data:
            solarflux, kindex, muf = solar_data
            band = predict_band_with_solar_data(muf, utc_hour, solarflux, kindex)
            if band:
                return band, JS8_BANDS[band]
    
    band = predict_band(utc_hour, latitude, temperature, weather)
    return band, JS8_BANDS[band]

def switch_js8call_band(band: str, freq: float) -> bool:
    """Switch JS8Call to the specified band and frequency."""
    try:
        api = JS8CallAPI()
        api.connect()
        
        # Convert MHz to Hz
        freq_hz = int(freq * 1000000)
        
        # Set the frequency
        api.set_frequency(dial_freq=freq_hz)
        
        # Get current frequency to confirm
        current_freq = api.get_frequency()
        print(f"JS8Call frequency set to {current_freq['dial']/1000000:.3f} MHz")
        
        api.close()
        return True
    except Exception as e:
        print(f"Error switching JS8Call frequency: {e}")
        return False

def main():
    try:
        lat, lon, gps_time = get_gps_data()
        print(f"GPS Time: {gps_time}")
        tz_name = get_timezone_name(lat, lon)
        local_time = gps_time.astimezone(pytz.timezone(tz_name))
        
        print(f"Location: {lat:.4f}°N, {lon:.4f}°E")
        print(f"Time: {local_time.strftime('%I:%M %p')} {tz_name} (from GPS)")
        
    except RuntimeError as e:
        print("Using default location (NJ)")
        lat = 40.9
        lon = -74.3
        # Use current UTC time for default location
        gps_time = datetime.now(pytz.UTC)
        tz_name = get_timezone_name(lat, lon)
        local_time = gps_time.astimezone(pytz.timezone(tz_name))
        print(f"Location: {lat:.4f}°N, {lon:.4f}°E")
        print(f"Time: {local_time.strftime('%I:%M %p')} {tz_name} (from system time)")

    band, freq = recommend_js8_band(lat, lon, gps_time)
    
    # Fetch and display solar conditions if available
    if check_internet_connection():
        solar_data = fetch_hamqsl_conditions()
        if solar_data:
            solarflux, kindex, muf = solar_data
            print("\nSolar Conditions:")
            if solarflux is not None:
                print(f"Solar Flux: {solarflux}")
            if kindex is not None:
                print(f"K-index: {kindex}")
            if muf is not None:
                print(f"Maximum Usable Frequency: {muf:.1f} MHz")
            
            # Explain conditions
            print("\nWhat this means:")
            if solarflux is not None:
                if solarflux > 150:
                    print("• High solar activity - Good conditions for long-distance communication")
                elif solarflux > 100:
                    print("• Moderate solar activity - Fair conditions for long-distance communication")
                else:
                    print("• Low solar activity - Limited long-distance communication")
                
            if kindex is not None:
                if kindex <= 2:
                    print("• Quiet geomagnetic field - Good conditions for HF propagation")
                elif kindex <= 4:
                    print("• Slightly disturbed conditions - Some HF bands may be affected")
                else:
                    print("• Disturbed conditions - HF propagation may be poor")
            
            if muf is not None:
                print(f"• Maximum usable frequency of {muf:.1f} MHz suggests {'good' if muf > 20 else 'limited'} high-band propagation")
    
    print(f"\nRecommended: {band} ({freq} MHz)")
    
    # Explain recommendation rationale
    print("\nRecommendation rationale:")
    local_hour = local_time.hour
    day = 7 <= local_hour <= 18
    high_lat = abs(lat) > 45
    
    if check_internet_connection():
        weather_data = fetch_weather_data(lat, lon)
        if weather_data:
            temperature, weather = weather_data
            print(f"• Current temperature: {temperature}°F")
            print(f"• Weather conditions: {weather}")
            
            if temperature and temperature > 85 and weather == "sunny":
                print("• High temperature and clear skies suggest enhanced high-band propagation")
    
    if not day:
        print("• Night time conditions favor lower frequency bands")
        if high_lat:
            print("• High latitude location requires lower frequencies for reliable communication")
    elif 10 <= local_hour <= 16:
        print("• Mid-day conditions typically support higher frequency bands")
    else:
        print("• Early morning/late afternoon conditions favor mid-range frequencies")
    
    # Ask if user wants to switch JS8Call to the recommended band
    response = input("\nWould you like to switch JS8Call to this band? (y/n): ").lower().strip()
    if response == 'y':
        if switch_js8call_band(band, freq):
            print("JS8Call frequency updated successfully")
        else:
            print("Failed to update JS8Call frequency")

if __name__ == "__main__":
    main()
