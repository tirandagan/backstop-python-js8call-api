#!/usr/bin/env python3
"""
JS8Call API Python Client Demo Script

This script demonstrates the usage of the JS8Call API library to control JS8Call
and interact with its features.

Copyright (c) 2023 Tiran Dagan, BackstopRadio.com
Licensed under MIT License

Features demonstrated:
- Connecting to JS8Call
- Getting frequency information
- Getting station information (callsign, grid)
- Comparing JS8Call grid with GPS grid
- Updating JS8Call grid square from GPS
"""

import time
import sys
from datetime import datetime

# Import from the JS8CallAPI package
from JS8CallAPI import JS8CallAPI, lat_lon_to_grid_square
from JS8CallAPI import JS8_NORMAL, JS8_FAST, JS8_TURBO, JS8_SLOW, JS8_ULTRA

# Import supporting functions
from demo_functions import (
    Colors, clear_screen, print_header, print_section, print_subsection,
    print_info, print_warning, print_error, print_success, print_data,
    print_json, prompt_continue, prompt_yes_no, print_test_description,
    ensure_connected
)

def main():
    """
    Main interactive demo program for JS8Call API.
    
    Shows a menu of demos and allows the user to select which to run.
    """
    clear_screen()
    print_header("JS8Call API Interactive Demo")
    print(f"\n{Colors.BOLD}Copyright (c) 2023 Tiran Dagan, BackstopRadio.com{Colors.END}")
    print("Licensed under MIT License\n")
    
    # Create API client
    api = JS8CallAPI()
    
    # Check if JS8Call is running before showing the menu
    print_section("JS8Call Availability Check")
    print_info("Checking if JS8Call is running...")
    
    try:
        # Try to connect
        api.connect()
        
        # Verify with a ping
        if api.ping():
            print_success("JS8Call is running and responsive!")
        else:
            print_warning("Connected to JS8Call, but it's not responding to pings.")
            print_info("Continuing anyway, but some features may not work correctly.")
            
        print_info("Ready to proceed with the demo.")
        prompt_continue()
        
    except ConnectionRefusedError:
        # Simple, clear message when JS8Call isn't running
        print_error("JS8Call is not running or the TCP API is not enabled.")
        print_info("To use this demo, please:")
        print_info("1. Start JS8Call")
        print_info("2. Enable the TCP Server API in File > Settings > Reporting")
        print_info("3. Run this demo again")
        sys.exit(1)
    except Exception as e:
        # Keep error message simple but informative
        print_error(f"Connection error: {str(e).split(':', 1)[0]}")
        print_info("Please check that JS8Call is running with the TCP API enabled.")
        sys.exit(1)
    
    # Menu of demo options
    demos = [
        ("Connection Test", "Test basic connection to JS8Call", run_connection_test),
        ("Station Information", "Get and set station information (callsign, grid, info text)", run_station_info_demo),
        ("GPS Integration", "Compare JS8Call grid with GPS and update if needed", run_gps_demo),
        ("Frequency Control", "View current frequency and optionally change it", run_frequency_demo),
        ("Station Monitoring", "Monitor activity from other stations", run_monitoring_demo),
        ("Message Operations", "Send and receive messages, manage inbox", run_messaging_demo),
        ("Mode Control", "Change JS8Call speed modes", run_mode_control_demo),
        ("Exit", "Exit the demo program", None)
    ]
    
    while True:
        clear_screen()
        print_header("JS8Call API Interactive Demo")
        print("\n\n" + Colors.BOLD + "Available Demos:" + Colors.END)
        
        # Print menu options
        for i, (name, desc, _) in enumerate(demos):
            print(f"{Colors.CYAN}{i+1}.{Colors.END} {Colors.BOLD}{name}{Colors.END}: {desc}")
        
        # Get user choice
        try:
            choice = int(input(f"\n{Colors.YELLOW}Enter your choice (1-{len(demos)}): {Colors.END}")) - 1
            if choice < 0 or choice >= len(demos):
                print_error(f"Please enter a number between 1 and {len(demos)}")
                continue
        except ValueError:
            print_error("Please enter a valid number")
            continue
        
        # Exit if last option selected
        if choice == len(demos) - 1:
            print_info("Exiting demo program...")
            break
            
        # Run selected demo
        demo_name, _, demo_func = demos[choice]
        clear_screen()
        print_header(f"Running Demo: {demo_name}")
        
        try:
            # Run demo function
            demo_func(api)
        except Exception as e:
            print_error(f"Error in demo: {e}")
        
        prompt_continue()
    
    # Close connection
    try:
        api.close()
    except:
        pass

def run_connection_test(api):
    """Test connection to JS8Call"""
    print_test_description("Connection Test", """
    This test will:
    1. Attempt to connect to the JS8Call TCP API server
    2. Send a PING message to verify connectivity
    3. Display basic server information
    """)
    
    # Connect to server
    try:
        print_info("Connecting to JS8Call...")
        api.connect()
        print_success("Connected to JS8Call API server")
        print_data("Host", api.host)
        print_data("Port", api.port)
        
        # Try ping
        print_info("Sending PING to verify connection...")
        if api.ping():
            print_success("PING successful! JS8Call is responsive")
        else:
            print_warning("PING failed, but connection is established")
            
        # Get version information if available (not directly supported by the API)
        print_info("Connection test completed successfully")
        
    except ConnectionRefusedError:
        print_error("Connection refused! Make sure JS8Call is running")
        print_info("Check that JS8Call has the TCP Server API enabled:")
        print_info("  File > Settings > Reporting > 'Enable TCP Server API'")
    except Exception as e:
        print_error(f"Connection failed: {e}")

def run_station_info_demo(api):
    """Demo for getting and setting station information"""
    print_test_description("Station Information Demo", """
    This demo will:
    1. Display current station information (callsign, grid square)
    2. Show the current station information and status text
    3. Allow you to update station information and status
    """)
    
    # Connect if not connected
    ensure_connected(api)
    
    # Get basic station info
    print_section("Current Station Information")
    try:
        # Get callsign
        callsign = api.get_callsign()
        print_data("Callsign", callsign)
        
        # Get grid
        grid = api.get_grid()
        print_data("Grid Square", grid)
        
        # Get station info text
        info = api.get_station_info()
        print_data("Info Text", info if info else "(None set)")
        
        # Get status
        status = api.get_status()
        print_data("Status", status if status else "(None set)")
        
        # Allow user to update info text
        print_section("Update Station Information")
        
        if prompt_yes_no("Would you like to update the station info text?"):
            new_info = input("Enter new station info text: ")
            print_info(f"Setting station info to: '{new_info}'")
            success = api.set_station_info(new_info)
            if success:
                print_success("Station info updated successfully")
            else:
                print_error("Failed to update station info")
                
        # Allow user to update status text
        if prompt_yes_no("Would you like to update the station status text?"):
            new_status = input("Enter new status text: ")
            print_info(f"Setting status to: '{new_status}'")
            success = api.set_status(new_status)
            if success:
                print_success("Status updated successfully")
            else:
                print_error("Failed to update status")
                
    except Exception as e:
        print_error(f"Error retrieving station information: {e}")

def run_gps_demo(api):
    """Demo for GPS integration"""
    print_test_description("GPS Integration Demo", """
    This demo will:
    1. Connect to your GPS device (if available)
    2. Get your current GPS position and convert it to a Maidenhead grid square
    3. Compare it with your current JS8Call grid square
    4. Offer to update JS8Call with your GPS-derived grid square if different
    """)
    
    # Connect if not connected
    ensure_connected(api)
    
    # Get current grid from JS8Call
    print_section("Current Grid Information")
    try:
        js8call_grid = api.get_grid()
        print_data("JS8Call Grid", js8call_grid)
        
        # Try to connect to GPS
        print_section("GPS Information")
        print_info("Attempting to connect to GPS...")
        
        try:
            api.connect_gps()
            print_success("Connected to GPS daemon")
            
            # Get GPS grid square
            print_info("Getting position from GPS...")
            gps_grid = api.get_gps_grid_square()
            
            if gps_grid:
                print_success("GPS position acquired")
                print_data("GPS Grid", gps_grid)
                
                # Compare grid squares (case insensitive)
                if gps_grid.upper() != js8call_grid.upper():
                    print_warning("Grid square mismatch detected!")
                    print_data("JS8Call Grid", js8call_grid)
                    print_data("GPS Grid", gps_grid)
                    
                    if prompt_yes_no("Would you like to update JS8Call's grid square?"):
                        print_info(f"Updating grid square to: {gps_grid}")
                        success = api.set_grid(gps_grid)
                        
                        # Wait a short time for the update to take effect
                        print_info("Waiting for JS8Call to update...")
                        time.sleep(1)
                        
                        # Verify the update
                        new_grid = api.get_grid()
                        print_data("New grid square", new_grid)
                        
                        if success and new_grid.upper() == gps_grid.upper():
                            print_success(f"Grid square successfully updated to: {gps_grid}")
                        else:
                            print_warning(f"Grid square may not have updated correctly")
                else:
                    print_success("JS8Call grid matches GPS grid - no update needed")
            else:
                print_error("Could not get GPS position")
                print_info("Make sure you have a GPS fix and gpsd is running")
        
        except Exception as e:
            print_error(f"GPS Error: {e}")
            print_info("Make sure gpsd is installed and running")
            print_info("On Linux: 'sudo apt install gpsd gpsd-clients'")
            print_info("Start with: 'sudo systemctl start gpsd'")
    
    except Exception as e:
        print_error(f"Error: {e}")

def run_frequency_demo(api):
    """Demo for frequency control"""
    print_test_description("Frequency Control Demo", """
    This demo will:
    1. Display current frequency information (dial, offset, operating frequency)
    2. Allow you to change the frequency (with confirmation)
    3. Optionally change back to the original frequency
    """)
    
    # Connect if not connected
    ensure_connected(api)
    
    try:
        # Get current frequency info
        print_section("Current Frequency")
        freq = api.get_frequency()
        current_freq = freq['dial']
        
        print_data("Operating", f"{freq['freq']:,}", " Hz")
        print_data("Dial", f"{freq['dial']:,}", " Hz")
        print_data("Offset", f"{freq['offset']:,}", " Hz")
        print_data("", f"{freq['dial']/1000000:.6f}", " MHz")
        
        # Ask if user wants to change frequency
        print_section("Frequency Change")
        if prompt_yes_no("Would you like to change the frequency?"):
            # Get new frequency
            while True:
                try:
                    new_freq_mhz = float(input("Enter new frequency in MHz (e.g. 14.078): "))
                    new_freq_hz = int(new_freq_mhz * 1000000)
                    break
                except ValueError:
                    print_error("Please enter a valid frequency")
            
            # Confirm with user
            print_warning(f"About to change frequency to {new_freq_mhz:.6f} MHz ({new_freq_hz:,} Hz)")
            print_warning("This will tune your radio if CAT control is enabled in JS8Call!")
            
            if prompt_yes_no("Are you sure you want to proceed?"):
                # Change frequency
                print_info(f"Changing frequency to {new_freq_mhz:.6f} MHz...")
                api.set_frequency(dial_freq=new_freq_hz)
                
                # Wait a moment
                time.sleep(2)
                
                # Get new frequency to confirm change
                new_freq_info = api.get_frequency()
                print_success("Frequency changed")
                print_data("New Dial", f"{new_freq_info['dial']:,}", " Hz")
                print_data("New Operating", f"{new_freq_info['freq']:,}", " Hz")
                
                # Ask if user wants to change back
                if prompt_yes_no("Would you like to change back to the original frequency?"):
                    print_info(f"Changing back to {current_freq/1000000:.6f} MHz...")
                    api.set_frequency(dial_freq=current_freq)
                    time.sleep(2)
                    
                    # Confirm we're back
                    final_freq = api.get_frequency()
                    print_success("Frequency restored")
                    print_data("Dial", f"{final_freq['dial']:,}", " Hz")
            else:
                print_info("Frequency change cancelled")
    
    except Exception as e:
        print_error(f"Error controlling frequency: {e}")

def run_monitoring_demo(api):
    """Demo for monitoring station and band activity"""
    print_test_description("Station Monitoring Demo", """
    This demo will:
    1. Display recently heard stations with signal reports and grids
    2. Show band activity with frequency information
    3. Get recently received text from the RX window
    4. Continue monitoring for a specified duration
    """)
    
    # Connect if not connected
    ensure_connected(api)
    
    try:
        # Ask for monitoring duration
        while True:
            try:
                duration = int(input("Enter monitoring duration in seconds (10-300): "))
                if 10 <= duration <= 300:
                    break
                print_warning("Please enter a value between 10 and 300")
            except ValueError:
                print_error("Please enter a valid number")
        
        # Calculate end time
        end_time = time.time() + duration
        iterations = 0
        
        # Monitoring loop
        while time.time() < end_time:
            iterations += 1
            remaining = int(end_time - time.time())
            
            clear_screen()
            print_header("JS8Call Monitoring")
            print_info(f"Monitoring JS8Call activity. Remaining time: {remaining} seconds")
            print_info(f"Press Ctrl+C to stop early")
            
            try:
                # Get call activity
                print_section("Station Activity")
                stations = api.get_call_activity()
                
                if stations:
                    # Remove _ID field if present
                    if '_ID' in stations:
                        del stations['_ID']
                    
                    print_data("Stations heard", len(stations))
                    print()
                    
                    # Create table header with colors
                    header = f"{Colors.BOLD}{'CALLSIGN':<10} {'GRID':<8} {'SNR':>5} {'TIME':>20}{Colors.END}"
                    print("  " + header)
                    print("  " + "-" * (10 + 8 + 5 + 20 + 3))  # Separator line with proper spacing
                    
                    # Sort stations by SNR (strongest signals first)
                    sorted_stations = sorted(
                        stations.items(), 
                        key=lambda x: x[1].get('SNR', -999) if isinstance(x[1].get('SNR'), (int, float)) else -999,
                        reverse=True
                    )
                    
                    # Display each station's info in a table row
                    for callsign, info in sorted_stations:
                        grid = info.get('GRID', '') if info.get('GRID') else ''
                        snr = f"{info.get('SNR', '')} dB" if 'SNR' in info else ''
                        
                        # Format time
                        time_str = ''
                        if 'UTC' in info:
                            timestamp = datetime.fromtimestamp(info['UTC']/1000)
                            time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        
                        # Print row
                        print(f"  {callsign:<10} {grid:<8} {snr:>5} {time_str:>20}")
                        
                        # Add a separator line every 10 stations for better readability
                        row_num = sorted_stations.index((callsign, info)) + 1
                        if row_num % 10 == 0 and row_num < len(sorted_stations):
                            print("  " + "-" * (10 + 8 + 5 + 20 + 3))
                else:
                    print_info("No stations heard recently")
                
                # Get selected call
                selected = api.get_selected_call()
                if selected:
                    print_data("\nSelected Call", selected)
                
                # Get band activity
                print_section("Band Activity")
                band = api.get_band_activity()
                
                if band:
                    # Remove _ID field if present
                    if '_ID' in band:
                        del band['_ID']
                    
                    print_data("Active signals", len(band))
                    print()
                    
                    # Create table header with colors
                    header = f"{Colors.BOLD}{'FREQ (MHz)':<12} {'OFFSET':>8} {'SNR':>5} {'TEXT':<45}{Colors.END}"
                    print("  " + header)
                    print("  " + "-" * (12 + 8 + 5 + 45 + 3))  # Separator line
                    
                    # Sort by frequency offset
                    sorted_band = sorted(
                        band.items(),
                        key=lambda x: int(x[0]) if x[0].isdigit() else 0
                    )
                    
                    # Display activity in table format (show up to 15 signals)
                    for offset_str, info in sorted_band[:15]:
                        freq_mhz = ""
                        if 'DIAL' in info and 'OFFSET' in info:
                            freq_hz = info.get('FREQ', info['DIAL'] + info['OFFSET'])
                            freq_mhz = f"{freq_hz/1000000:.6f}"
                        
                        offset = f"{offset_str} Hz" if offset_str.isdigit() else offset_str
                        snr = f"{info.get('SNR', '')} dB" if 'SNR' in info else ''
                        
                        # Truncate text for display
                        text = ""
                        if 'TEXT' in info and info['TEXT']:
                            text = info['TEXT']
                            if len(text) > 45:
                                text = text[:42] + "..."
                        
                        # Print row
                        print(f"  {freq_mhz:<12} {offset:>8} {snr:>5} {text:<45}")
                    
                    # Show indication if there are more signals
                    if len(band) > 15:
                        print_info(f"...and {len(band)-15} more signals not shown")
                else:
                    print_info("No band activity detected")
                
                # Get latest RX text
                print_section("Received Text")
                rx_text = api.get_rx_text()
                if rx_text:
                    lines = rx_text.strip().split('\n')
                    if len(lines) > 5:
                        print_info(f"Showing last 5 lines of {len(lines)} total")
                        displayed_text = '\n'.join(lines[-5:])
                    else:
                        displayed_text = rx_text
                    
                    print(f"\n{displayed_text}")
                else:
                    print_info("No text received")
                
                # Wait before next poll
                interval = min(5, remaining)
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print_info("\nMonitoring stopped by user")
                break
            except Exception as e:
                print_error(f"Error during monitoring: {e}")
                time.sleep(5)  # Wait before retry
        
        print_success(f"\nCompleted {iterations} monitoring cycles over {duration} seconds")
    
    except Exception as e:
        print_error(f"Error in monitoring demo: {e}")

def run_messaging_demo(api):
    """Demo for message operations"""
    print_test_description("Messaging Operations Demo", """
    This demo will:
    1. Show current text in the TX buffer
    2. Allow you to set new text in the TX buffer
    3. Display inbox messages
    4. Allow you to store a new message in the inbox
    5. Optionally allow you to send a message (with careful confirmation)
    """)
    
    # Connect if not connected
    ensure_connected(api)
    
    try:
        # Get current TX text
        print_section("Current TX Text")
        tx_text = api.get_tx_text()
        if tx_text:
            print(f"\n{tx_text}")
        else:
            print_info("TX buffer is empty")
        
        # Set TX text
        print_section("Update TX Text")
        if prompt_yes_no("Would you like to set new text in the TX buffer?"):
            new_text = input("Enter new TX text: ")
            print_info(f"Setting TX text to: '{new_text}'")
            success = api.set_tx_text(new_text)
            if success:
                print_success("TX text updated successfully")
            else:
                print_error("Failed to update TX text")
        
        # Get inbox messages
        print_section("Inbox Messages")
        messages = api.get_inbox_messages()
        if messages:
            print_data("Messages in inbox", len(messages))
            
            for i, msg in enumerate(messages, 1):
                print(f"\n  {Colors.BOLD}Message {i}{Colors.END}")
                params = msg.get('params', {})
                if 'FROM' in params:
                    print(f"    From: {params['FROM']}")
                if 'TO' in params:
                    print(f"    To: {params['TO']}")
                if 'TEXT' in params:
                    print(f"    Text: {params['TEXT']}")
                if 'UTC' in params:
                    timestamp = datetime.fromtimestamp(params['UTC']/1000)
                    print(f"    Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print_info("No messages in inbox")
        
        # Store a message
        print_section("Store Message")
        if prompt_yes_no("Would you like to store a message in the inbox?"):
            dest_call = input("Enter destination callsign: ")
            msg_text = input("Enter message text: ")
            
            print_info(f"Storing message to {dest_call}: '{msg_text}'")
            try:
                response = api.store_message(dest_call, msg_text)
                if 'params' in response and 'ID' in response['params']:
                    print_success(f"Message stored with ID: {response['params']['ID']}")
                else:
                    print_success("Message stored successfully")
            except Exception as e:
                print_error(f"Failed to store message: {e}")
        
        # Send a message (with careful confirmation)
        print_section("Send Message")
        print_warning("⚠ This will actually transmit on your radio if JS8Call is properly configured!")
        if prompt_yes_no("Would you like to prepare a message for transmission?"):
            msg_text = input("Enter message text to transmit: ")
            
            print_warning("⚠ TRANSMISSION WARNING ⚠")
            print_warning("The following text will be transmitted:")
            print(f"\n{msg_text}\n")
            print_warning("This will key your transmitter if JS8Call is properly connected to your radio!")
            print_warning("Make sure you're on a clear frequency and won't cause interference")
            print_warning("Make sure you're licensed to transmit on the current frequency")
            
            # Double-confirm
            if prompt_yes_no("Are you ABSOLUTELY SURE you want to transmit?"):
                if prompt_yes_no("Final confirmation: Transmit this message?"):
                    print_info("Setting message text in TX buffer...")
                    api.set_tx_text(msg_text)
                    
                    # Give user one last chance to check JS8Call UI before sending
                    print_warning("Message is now in the TX buffer")
                    print_warning("Check JS8Call to confirm it's correct before proceeding")
                    
                    if prompt_yes_no("Send the message now?"):
                        print_info("Sending message...")
                        try:
                            api.send_message_text(msg_text)
                            print_success("Message transmission initiated")
                            print_info("Check JS8Call for transmission status")
                        except Exception as e:
                            print_error(f"Transmission error: {e}")
                    else:
                        print_info("Transmission cancelled, but text remains in TX buffer")
                else:
                    print_info("Transmission cancelled")
            else:
                print_info("Transmission cancelled")
    
    except Exception as e:
        print_error(f"Error in messaging demo: {e}")

def run_mode_control_demo(api):
    """Demo for JS8Call speed mode control"""
    print_test_description("Mode Control Demo", """
    This demo will:
    1. Show the current JS8Call speed mode
    2. Explain the different JS8Call modes
    3. Allow you to change to a different mode
    4. Change back to the original mode if desired
    """)
    
    # Connect if not connected
    ensure_connected(api)
    
    # Speed mode explanations
    mode_info = {
        JS8_NORMAL: {
            "name": "Normal",
            "desc": "Standard JS8 mode (50Hz bandwidth, ~16 WPM)",
            "time": "15 seconds per transmission"
        },
        JS8_FAST: {
            "name": "Fast",
            "desc": "Faster mode with 80Hz bandwidth (~24 WPM)",
            "time": "10 seconds per transmission"
        },
        JS8_TURBO: {
            "name": "Turbo",
            "desc": "Fastest mode with 160Hz bandwidth (~40 WPM)",
            "time": "6 seconds per transmission"
        },
        JS8_SLOW: {
            "name": "Slow",
            "desc": "Slow mode with 25Hz bandwidth (~8 WPM)",
            "time": "30 seconds per transmission"
        },
        JS8_ULTRA: {
            "name": "Ultra",
            "desc": "Ultra slow mode with 16Hz bandwidth (~4 WPM)",
            "time": "1 minute per transmission"
        }
    }
    
    try:
        # Get current mode
        print_section("Current Mode")
        current_mode = api.get_speed()
        mode_name = mode_info.get(current_mode, {}).get("name", "Unknown")
        
        print_data("Current mode", f"{mode_name} (value: {current_mode})")
        
        if current_mode in mode_info:
            print_data("Description", mode_info[current_mode]["desc"])
            print_data("Timing", mode_info[current_mode]["time"])
        
        # Show available modes
        print_section("Available Modes")
        for mode, info in mode_info.items():
            print(f"  {Colors.BOLD}{info['name']}{Colors.END} (value: {mode})")
            print(f"    {info['desc']}")
            print(f"    {info['time']}")
        
        # Change mode
        print_section("Change Mode")
        if prompt_yes_no("Would you like to change the JS8Call speed mode?"):
            # Show mode options
            print("\nSelect a new mode:")
            for mode, info in mode_info.items():
                print(f"  {mode}: {info['name']}")
            
            # Get user choice
            while True:
                try:
                    new_mode = int(input("\nEnter mode number (0-4): "))
                    if new_mode in mode_info:
                        break
                    print_warning("Please enter a valid mode number (0-4)")
                except ValueError:
                    print_error("Please enter a valid number")
            
            # Change to new mode
            print_info(f"Changing to {mode_info[new_mode]['name']} mode...")
            success = api.set_speed(new_mode)
            
            if success:
                print_success(f"Mode changed to {mode_info[new_mode]['name']}")
                
                # Ask if user wants to change back
                if prompt_yes_no("Would you like to change back to the original mode?"):
                    print_info(f"Changing back to {mode_info[current_mode]['name']} mode...")
                    api.set_speed(current_mode)
                    print_success(f"Mode restored to {mode_info[current_mode]['name']}")
            else:
                print_error("Failed to change mode")
    
    except Exception as e:
        print_error(f"Error in mode control demo: {e}")

if __name__ == "__main__":
    main() 

# PING Command Implementation Notes:
# -------------------------------
# The PING command is a simple request-response mechanism to check if JS8Call is responsive.
#
# In JS8Call's source:
# - When the client sends a "PING" message type, JS8Call receives it and processes it
# - JS8Call's MessageClient::impl::heartbeat() method also uses a PING message for periodic heartbeats
# - This PING message includes NAME, VERSION, and UTC timestamp parameters
#
# In our implementation:
# - We send a simple "PING" message type without additional parameters
# - If we receive any response, we consider the PING successful
# - No specific response data is expected or processed from the PING command
# - The ping() method returns boolean True/False to indicate success/failure
#
# This is used by various parts of the demo app to check connectivity without
# requiring a more complex API call or data processing. 