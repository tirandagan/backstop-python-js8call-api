#!/usr/bin/env python3
"""
Example 1: Connection Monitor
Demonstrates how to monitor JS8Call connection status
"""
from JS8CallAPI import JS8CallAPI
import time
from datetime import datetime

def monitor_connection():
    api = JS8CallAPI()
    
    try:
        print("Connecting to JS8Call...")
        api.connect()
        print("Connected successfully!")
        
        # Monitor connection for 60 seconds
        end_time = time.time() + 60
        while time.time() < end_time:
            if api.is_closed():
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] JS8Call connection closed!")
                break
            else:
                print(f"\r[{datetime.now().strftime('%H:%M:%S')}] Connection active...", end="")
            
            time.sleep(1)
            
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if not api.is_closed():
            api.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    monitor_connection() 