#!/usr/bin/env python3
"""
Example 8: GPS Grid Square
Demonstrates how to use GPS for grid square updates
"""
from JS8CallAPI import JS8CallAPI

def update_grid_from_gps():
    api = JS8CallAPI()
    
    try:
        print("Connecting to JS8Call...")
        api.connect()
        
        # Get current grid
        current_grid = api.get_grid()
        print(f"Current grid square: {current_grid}")
        
        # Connect to GPS
        print("\nConnecting to GPS...")
        api.connect_gps()
        
        # Get grid from GPS
        gps_grid = api.get_gps_grid_square()
        if gps_grid:
            print(f"GPS grid square: {gps_grid}")
            
            # Update if different
            if gps_grid.upper() != current_grid.upper():
                print("\nUpdating grid square...")
                if api.set_grid(gps_grid):
                    print(f"Grid square updated to: {gps_grid}")
                else:
                    print("Failed to update grid square")
            else:
                print("\nGrid square is already current")
        else:
            print("Could not get grid square from GPS")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.close()

if __name__ == "__main__":
    update_grid_from_gps() 