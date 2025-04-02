#!/usr/bin/env python3
"""
Example 3: Station Monitor
Demonstrates how to monitor station activity
"""
from JS8CallAPI import JS8CallAPI
import time
from datetime import datetime

def monitor_stations():
    api = JS8CallAPI()
    
    try:
        print("Connecting to JS8Call...")
        api.connect()
        
        # Monitor for 60 seconds
        end_time = time.time() + 60
        seen_stations = set()
        
        while time.time() < end_time:
            print(f"\n--- Station Activity at {datetime.now().strftime('%H:%M:%S')} ---")
            
            # Get call activity
            stations = api.get_call_activity()
            for call, info in stations.items():
                if call not in seen_stations:
                    print(f"\nNew station: {call}")
                    print(f"  SNR: {info.get('SNR')} dB")
                    print(f"  Grid: {info.get('GRID')}")
                    print(f"  Time: {datetime.fromtimestamp(info.get('UTC', 0)/1000).strftime('%Y-%m-%d %H:%M:%S')}")
                    seen_stations.add(call)
            
            # Get band activity
            band = api.get_band_activity()
            print(f"\nBand Activity: {len(band)} frequencies active")
            
            time.sleep(10)  # Check every 10 seconds
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.close()

if __name__ == "__main__":
    monitor_stations() 