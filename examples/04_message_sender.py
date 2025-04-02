#!/usr/bin/env python3
"""
Example 4: Message Sender
Demonstrates how to send messages and store them in the inbox
"""
from JS8CallAPI import JS8CallAPI
import time

def send_messages():
    api = JS8CallAPI()
    
    try:
        print("Connecting to JS8Call...")
        api.connect()
        
        # Get current callsign
        my_call = api.get_callsign()
        print(f"Station callsign: {my_call}")
        
        # Example messages to send
        messages = [
            "CQ CQ CQ DE " + my_call,
            "TEST TEST DE " + my_call,
            "73 DE " + my_call
        ]
        
        # Send each message
        for msg in messages:
            print(f"\nSending: {msg}")
            api.set_tx_text(msg)
            api.send_message_text(msg)
            time.sleep(2)  # Wait between messages
            
        # Store a message in the inbox
        print("\nStoring message in inbox...")
        response = api.store_message("W1AW", "Hello from the message sender example!")
        print(f"Message stored with ID: {response['params'].get('ID')}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.close()

if __name__ == "__main__":
    send_messages() 