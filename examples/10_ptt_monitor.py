#!/usr/bin/env python3
"""
Example 10: PTT Monitor
Demonstrates how to monitor PTT status
"""
from JS8CallAPI import JS8CallAPI
import time
from datetime import datetime

def monitor_ptt():
    api = JS8CallAPI()
    
    try:
        print("Connecting to JS8Call...")
        api.connect()
        
        # Monitor for 60 seconds
        end_time = time.time() + 60
        print("\nMonitoring PTT status for 60 seconds...")
        print("Press PTT to see status changes")
        
        last_status = None
        while time.time() < end_time:
            current_status = api.get_ptt_status()
            
            # Only print when status changes
            if current_status != last_status:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] PTT Status: {'Active' if current_status else 'Inactive'}")
                last_status = current_status
            
            time.sleep(0.1)  # Check frequently
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.close()

if __name__ == "__main__":
    monitor_ptt() 