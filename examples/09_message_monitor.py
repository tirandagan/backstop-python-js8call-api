#!/usr/bin/env python3
"""
Example 9: Message Monitor
Demonstrates how to monitor received messages and spots
"""
from JS8CallAPI import JS8CallAPI
import time
from datetime import datetime

def monitor_messages():
    api = JS8CallAPI()
    
    try:
        print("Connecting to JS8Call...")
        api.connect()
        
        # Monitor for 60 seconds
        end_time = time.time() + 60
        print("\nMonitoring messages for 60 seconds...")
        
        while time.time() < end_time:
            print(f"\n--- Message Activity at {datetime.now().strftime('%H:%M:%S')} ---")
            
            # Check for directed messages
            directed = api.get_directed_message()
            if directed:
                print("\nDirected Message:")
                print(f"From: {directed.get('FROM')}")
                print(f"To: {directed.get('TO')}")
                print(f"Text: {directed.get('TEXT')}")
            
            # Check for spots
            spot = api.get_spot()
            if spot:
                print("\nSpot:")
                print(f"Station: {spot.get('STATION')}")
                print(f"Frequency: {spot.get('FREQ')/1000:.1f} kHz")
                print(f"SNR: {spot.get('SNR')} dB")
            
            # Check for TX frames
            tx_frame = api.get_tx_frame()
            if tx_frame:
                print("\nTX Frame:")
                print(f"Text: {tx_frame.get('TEXT')}")
            
            time.sleep(5)  # Check every 5 seconds
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.close()

if __name__ == "__main__":
    monitor_messages() 