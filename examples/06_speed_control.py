#!/usr/bin/env python3
"""
Example 6: Speed Control
Demonstrates how to control JS8Call speed modes
"""
from JS8CallAPI import JS8CallAPI
import time

def test_speeds():
    api = JS8CallAPI()
    
    # Speed mode names
    speed_names = {
        api.JS8_NORMAL: "Normal",
        api.JS8_FAST: "Fast",
        api.JS8_TURBO: "Turbo",
        api.JS8_SLOW: "Slow",
        api.JS8_ULTRA: "Ultra"
    }
    
    try:
        print("Connecting to JS8Call...")
        api.connect()
        
        # Get current speed
        current_speed = api.get_speed()
        print(f"Current speed: {speed_names.get(current_speed, 'Unknown')}")
        
        # Test each speed mode
        speeds = [
            api.JS8_NORMAL,
            api.JS8_FAST,
            api.JS8_TURBO,
            api.JS8_SLOW,
            api.JS8_ULTRA
        ]
        
        for speed in speeds:
            print(f"\nSetting speed to {speed_names.get(speed, 'Unknown')}...")
            api.set_speed(speed)
            time.sleep(5)  # Wait 5 seconds in each mode
            
        # Return to original speed
        print(f"\nReturning to original speed: {speed_names.get(current_speed, 'Unknown')}")
        api.set_speed(current_speed)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.close()

if __name__ == "__main__":
    test_speeds() 