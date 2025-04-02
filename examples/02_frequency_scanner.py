#!/usr/bin/env python3
"""
Example 2: Frequency Scanner
Demonstrates how to scan through different frequencies
"""
from JS8CallAPI import JS8CallAPI
import time

def scan_frequencies():
    api = JS8CallAPI()
    
    # Common JS8Call frequencies in Hz
    frequencies = [
        14074000,  # 20m
        7074000,   # 40m
        3574000,   # 80m
        18104000,  # 17m
        10140000,  # 30m
    ]
    
    try:
        print("Connecting to JS8Call...")
        api.connect()
        
        # Store original frequency
        original_freq = api.get_frequency()
        print(f"Original frequency: {original_freq['freq']/1000:.1f} kHz")
        
        # Scan through frequencies
        for freq in frequencies:
            print(f"\nTuning to {freq/1000:.1f} kHz...")
            api.set_frequency(dial_freq=freq)
            time.sleep(5)  # Listen for 5 seconds
            
        # Return to original frequency
        print(f"\nReturning to original frequency: {original_freq['freq']/1000:.1f} kHz")
        api.set_frequency(dial_freq=original_freq['dial'])
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.close()

if __name__ == "__main__":
    scan_frequencies() 