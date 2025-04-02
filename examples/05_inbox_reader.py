#!/usr/bin/env python3
"""
Example 5: Inbox Reader
Demonstrates how to read messages from the inbox
"""
from JS8CallAPI import JS8CallAPI
from datetime import datetime

def read_inbox():
    api = JS8CallAPI()
    
    try:
        print("Connecting to JS8Call...")
        api.connect()
        
        # Get all messages from inbox
        print("\nReading inbox messages...")
        messages = api.get_inbox_messages()
        
        if not messages:
            print("No messages in inbox")
            return
            
        print(f"\nFound {len(messages)} messages:")
        for msg in messages:
            print("\n--- Message ---")
            print(f"From: {msg['params'].get('FROM')}")
            print(f"To: {msg['params'].get('TO')}")
            print(f"Text: {msg['params'].get('TEXT')}")
            print(f"Time: {datetime.fromtimestamp(msg['params'].get('UTC', 0)/1000).strftime('%Y-%m-%d %H:%M:%S')}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.close()

if __name__ == "__main__":
    read_inbox() 