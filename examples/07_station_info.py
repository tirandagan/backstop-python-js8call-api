#!/usr/bin/env python3
"""
Example 7: Station Info Manager
Demonstrates how to manage station information
"""
from JS8CallAPI import JS8CallAPI

def manage_station_info():
    api = JS8CallAPI()
    
    try:
        print("Connecting to JS8Call...")
        api.connect()
        
        # Get current station info
        print("\nCurrent Station Information:")
        print(f"Callsign: {api.get_callsign()}")
        print(f"Grid: {api.get_grid()}")
        print(f"Status: {api.get_status()}")
        print(f"Station Info: {api.get_station_info()}")
        
        # Update station information
        print("\nUpdating station information...")
        api.set_grid("FN42")
        api.set_status("Testing JS8Call API")
        api.set_station_info("Python API Example Station")
        
        # Verify updates
        print("\nUpdated Station Information:")
        print(f"Grid: {api.get_grid()}")
        print(f"Status: {api.get_status()}")
        print(f"Station Info: {api.get_station_info()}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.close()

if __name__ == "__main__":
    manage_station_info() 