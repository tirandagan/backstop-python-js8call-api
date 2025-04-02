# JS8Call API Python Client

<div align="center">

![JS8Call Logo](js8call-logo.png)

[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![JS8Call](https://img.shields.io/badge/JS8Call-API-green.svg)](https://js8call.com/)

**A comprehensive Python client library for interacting with JS8Call's TCP API**

*Developed by [Tiran Dagan](https://github.com/tirandagan), [BackstopRadio.com](https://backstopradio.com)*

</div>

---

## Table of Contents

- [Overview](#overview)
- [API Features Summary](#api-features-summary)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Provided Examples](#provided-examples)
- [Advanced Examples](#advanced-examples)
  - [Using the Direct Implementation](#using-the-direct-implementation)
  - [Messaging Operations](#messaging-operations)
  - [Station Monitoring](#station-monitoring)
  - [Mode Control](#mode-control)
  - [GPS Integration](#gps-integration)
  - [Frequency Control](#frequency-control)
- [API Reference](#api-reference)
  - [JS8CallAPI Class](#js8callapi-class)
  - [Class Constants](#class-constants)
  - [Connection Methods](#connection-methods)
  - [Frequency Methods](#frequency-methods)
  - [Station Information Methods](#station-information-methods)
  - [Messaging Methods](#messaging-methods)
  - [Activity Monitoring Methods](#activity-monitoring-methods)
  - [Mode Control Methods](#mode-control-methods)
  - [Inbox Methods](#inbox-methods)
  - [UI Control Methods](#ui-control-methods)
  - [GPS Methods](#gps-methods)
- [Response Data Structures](#response-data-structures)
- [Error Handling](#error-handling)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License and Legal](#license-and-legal)
- [Acknowledgments](#acknowledgments)

---

## Overview

This Python client library provides a comprehensive, high-level interface to JS8Call's TCP API. It allows you to programmatically control JS8Call and integrate it with other applications or systems.

The package includes:
- A robust API client library (`JS8CallAPI.py`)
- An interactive demo script (`demo.py`) showcasing all features
- Supporting utilities for the demo interface (`demo_functions.py`)

### Key Features

<table>
  <tr>
    <td width="50%">
      <ul>
        <li>🔌 Complete TCP API support</li>
        <li>📡 Control transceiver frequency</li>
        <li>📋 Manage station information</li>
        <li>💬 Send and receive messages</li>
        <li>📊 Monitor band activity</li>
      </ul>
    </td>
    <td width="50%">
      <ul>
        <li>📬 Access inbox messages</li>
        <li>🌐 GPS position integration</li>
        <li>🔄 Grid square conversion</li>
        <li>⚙️ Control JS8Call modes</li>
        <li>🛡️ Robust error handling</li>
      </ul>
    </td>
  </tr>
</table>

---

## API Features Summary

The following table provides a complete overview of all available API methods:

<table>
  <thead>
    <tr>
      <th width="20%">Feature</th>
      <th width="15%">Get</th>
      <th width="15%">Set</th>
      <th width="20%">Return Type</th>
      <th width="30%">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Frequency</td>
      <td>✅ <code>get_frequency()</code></td>
      <td>✅ <code>set_frequency()</code></td>
      <td><code>Dict[str, int]</code></td>
      <td>Get/set current dial frequency and offset</td>
    </tr>
    <tr>
      <td>Callsign</td>
      <td>✅ <code>get_callsign()</code></td>
      <td>❌</td>
      <td><code>str</code></td>
      <td>Get current station callsign</td>
    </tr>
    <tr>
      <td>Grid Square</td>
      <td>✅ <code>get_grid()</code></td>
      <td>✅ <code>set_grid()</code></td>
      <td><code>str</code> / <code>bool</code></td>
      <td>Get/set station grid locator</td>
    </tr>
    <tr>
      <td>Station Info</td>
      <td>✅ <code>get_station_info()</code></td>
      <td>✅ <code>set_station_info()</code></td>
      <td><code>str</code> / <code>bool</code></td>
      <td>Get/set station information text</td>
    </tr>
    <tr>
      <td>Status</td>
      <td>✅ <code>get_status()</code></td>
      <td>✅ <code>set_status()</code></td>
      <td><code>str</code> / <code>bool</code></td>
      <td>Get/set current station status message</td>
    </tr>
    <tr>
      <td>Call Activity</td>
      <td>✅ <code>get_call_activity()</code></td>
      <td>❌</td>
      <td><code>Dict[str, Dict[str, Any]]</code></td>
      <td>Get structured list of recently heard stations</td>
    </tr>
    <tr>
      <td>Selected Call</td>
      <td>✅ <code>get_selected_call()</code></td>
      <td>❌</td>
      <td><code>str</code></td>
      <td>Get currently selected callsign in UI</td>
    </tr>
    <tr>
      <td>Band Activity</td>
      <td>✅ <code>get_band_activity()</code></td>
      <td>❌</td>
      <td><code>Dict[str, Dict[str, Any]]</code></td>
      <td>Get structured activity across the band</td>
    </tr>
    <tr>
      <td>RX Text</td>
      <td>✅ <code>get_rx_text()</code></td>
      <td>❌</td>
      <td><code>str</code></td>
      <td>Get text from receive window</td>
    </tr>
    <tr>
      <td>TX Text</td>
      <td>✅ <code>get_tx_text()</code></td>
      <td>✅ <code>set_tx_text()</code></td>
      <td><code>str</code> / <code>bool</code></td>
      <td>Get/set text in transmit buffer</td>
    </tr>
    <tr>
      <td>Send Message</td>
      <td>❌</td>
      <td>✅ <code>send_message_text()</code></td>
      <td><code>bool</code></td>
      <td>Send a message immediately</td>
    </tr>
    <tr>
      <td>Speed</td>
      <td>✅ <code>get_speed()</code></td>
      <td>✅ <code>set_speed()</code></td>
      <td><code>int</code> / <code>bool</code></td>
      <td>Get/set JS8Call speed mode</td>
    </tr>
    <tr>
      <td>Inbox</td>
      <td>✅ <code>get_inbox_messages()</code></td>
      <td>✅ <code>store_message()</code></td>
      <td><code>List[Dict[str, Any]]</code> / <code>Dict[str, Any]</code></td>
      <td>Get/store inbox messages</td>
    </tr>
    <tr>
      <td>Window</td>
      <td>❌</td>
      <td>✅ <code>raise_window()</code></td>
      <td><code>bool</code></td>
      <td>Raise JS8Call window to foreground</td>
    </tr>
    <tr>
      <td>GPS Grid</td>
      <td>✅ <code>get_gps_grid_square()</code></td>
      <td>❌</td>
      <td><code>Optional[str]</code></td>
      <td>Get grid square from current GPS position</td>
    </tr>
    <tr>
      <td>Ping</td>
      <td>✅ <code>ping()</code></td>
      <td>❌</td>
      <td><code>bool</code></td>
      <td>Check if JS8Call is responsive</td>
    </tr>
    <tr>
      <td>PTT Status</td>
      <td>✅ <code>get_ptt_status()</code></td>
      <td>❌</td>
      <td><code>bool</code></td>
      <td>Get current PTT status</td>
    </tr>
    <tr>
      <td>Directed Message</td>
      <td>✅ <code>get_directed_message()</code></td>
      <td>❌</td>
      <td><code>Optional[Dict[str, Any]]</code></td>
      <td>Get last directed message received</td>
    </tr>
    <tr>
      <td>Spot</td>
      <td>✅ <code>get_spot()</code></td>
      <td>❌</td>
      <td><code>Optional[Dict[str, Any]]</code></td>
      <td>Get last spot received</td>
    </tr>
    <tr>
      <td>TX Frame</td>
      <td>✅ <code>get_tx_frame()</code></td>
      <td>❌</td>
      <td><code>Optional[Dict[str, Any]]</code></td>
      <td>Get last TX frame sent</td>
    </tr>
    <tr>
      <td>Connection Status</td>
      <td>✅ <code>is_closed()</code></td>
      <td>❌</td>
      <td><code>bool</code></td>
      <td>Check if JS8Call connection is closed</td>
    </tr>
  </tbody>
</table>



## Installation

### Prerequisites

- Python 3.6 or higher
- JS8Call running with TCP API enabled
- Network connectivity to the JS8Call server
- gpsd (for GPS functionality)

### Quick Install

Install directly from PyPI:

```bash
pip install backstop-python-js8call-api
```

### Development Install

If you want to contribute or modify the code:

1. Clone this repository:
```bash
git clone https://github.com/tirandagan/backstop-python-js8call-api.git
cd backstop-python-js8call-api
```

2. Install in development mode:
```bash
pip install -e .
```

### File Structure

The repository contains the following main files:
- `JS8CallAPI.py`: The main API client library
- `demo.py`: An interactive demo script showcasing all API features
- `demo_functions.py`: Supporting functions for the demo script's UI and utilities

---

## Basic Usage

The simplest way to use the library is through the `JS8CallAPI` class, which ensures proper message formatting for the JS8Call API.

```python
from JS8CallAPI import JS8CallAPI

# Create API client
api = JS8CallAPI()

try:
    # Connect to JS8Call
    api.connect()
    
    # Get current frequency
    freq = api.get_frequency()
    print(f"Current frequency: {freq['freq']:,} Hz")
    print(f"Dial frequency: {freq['dial']:,} Hz")
    print(f"Offset: {freq['offset']} Hz")
    
    # Get station information
    callsign = api.get_callsign()
    grid = api.get_grid()
    print(f"Station: {callsign} in {grid}")
    
finally:
    # Always close the connection
    api.close()
```

### Running the Interactive Demo

The package includes an interactive demo script (`demo.py`) that showcases all API features:

```bash
python demo.py
```

This will launch a menu-driven interface allowing you to:
- Test basic API connectivity
- View and update station information
- Monitor station and band activity
- Send and receive messages
- Control JS8Call modes and speeds
- Integrate with GPS for grid square updates

## Provided Examples

The package includes several example scripts in the `examples` directory demonstrating different use cases:

### 1. Basic Connection (`01_basic_connection.py`)
Demonstrates the fundamental connection to JS8Call and retrieving basic information like frequency. This example shows how to:
- Establish a connection to JS8Call
- Retrieve current frequency information
- Safely close the connection

Example output:
```
Connected to JS8Call
Current frequency: 14,078,000 Hz
Dial frequency: 14,077,000 Hz
Offset: 1,000 Hz
Connection closed
```

### 2. Message Sending (`02_send_message.py`)
Shows how to send messages to other stations using the API. This example demonstrates:
- Connecting to JS8Call
- Sending a message to a specific callsign
- Verifying message transmission

Example output:
```
Connected to JS8Call
Sending message to W1AW: "Hello from JS8Call API!"
Message sent successfully
Connection closed
```

### 3. Frequency Control (`03_change_frequencies.py`)
Illustrates how to change and monitor JS8Call frequencies. This example shows:
- Reading current frequency
- Changing to a new frequency (20m band)
- Verifying the frequency change
- Returning to original frequency

Example output:
```
Connected to JS8Call
Current frequency: 7,040,000 Hz
Changing to 20m band (14,078,000 Hz)
New frequency: 14,078,000 Hz
Returning to original frequency
Connection closed
```

### 4. Message Monitoring (`04_monitor_messages.py`)
Demonstrates real-time monitoring of incoming messages. This example shows:
- Continuous monitoring of the receive window
- Displaying message details (sender, recipient, text)
- Graceful handling of connection closure

Example output:
```
Connected to JS8Call
Monitoring messages (Press Ctrl+C to stop)...

[14:30:15] From: W1AW To: ALL Text: CQ CQ CQ
[14:30:45] From: K1ABC To: W1AW Text: Hello W1AW
[14:31:00] From: N1XYZ To: ALL Text: QSY 20m
Connection closed
```

### 5. Station Information (`05_get_station_info.py`)
Shows how to retrieve and display station information. This example demonstrates:
- Getting station details
- Displaying callsign and grid square
- Handling missing information

Example output:
```
Connected to JS8Call
Station Information:
Callsign: W1AW
Grid Square: FN31
Status: Active
Connection closed
```

### 6. Mode Control (`06_get_mode_info.py`)
Demonstrates how to check and control JS8Call operating modes. This example shows:
- Reading current mode
- Changing mode settings
- Verifying mode changes

Example output:
```
Connected to JS8Call
Current mode: JS8
Changing to JS8Fast mode
Mode changed successfully
Connection closed
```

### 7. Signal Quality (`07_get_snr.py`)
Shows how to monitor signal-to-noise ratio. This example demonstrates:
- Reading current SNR
- Monitoring SNR changes
- Displaying signal quality information

Example output:
```
Connected to JS8Call
Current SNR: 12 dB
Signal Quality: Good
Monitoring SNR for 60 seconds...
SNR fluctuated between 8-15 dB
Connection closed
```

### 8. Speed Control (`08_get_speed.py`)
Illustrates how to control JS8Call's speed settings. This example shows:
- Reading current speed
- Changing speed modes
- Verifying speed changes

Example output:
```
Connected to JS8Call
Current speed: Normal
Changing to Turbo mode
Speed changed successfully
Connection closed
```

### 9. Callsign Operations (`09_get_callsign.py`)
Demonstrates how to work with station callsigns. This example shows:
- Reading current callsign
- Validating callsign format
- Displaying station identification

Example output:
```
Connected to JS8Call
Current callsign: W1AW
Callsign format: Valid
Station identification complete
Connection closed
```

### 10. Grid Square Operations (`10_get_grid.py`)
Shows how to handle Maidenhead grid square operations. This example demonstrates:
- Reading current grid square
- Validating grid square format
- Updating grid square from GPS (if available)

Example output:
```
Connected to JS8Call
Current grid square: FN31
Grid square format: Valid
GPS grid square: FN31pr
Grid square updated successfully
Connection closed
```

### 11. Band Predictor (`11_band_predictor.py`)
A comprehensive example that demonstrates how to use the JS8Call API along with GPS, weather, and solar data to recommend the optimal band for operation. This example includes:

- GPS integration for location and time
- Weather data fetching from OpenWeatherMap API
- Solar conditions from HamQSL API
- Smart band prediction based on:
  - Time of day
  - Location (latitude)
  - Temperature and weather conditions
  - Solar flux and K-index
  - Maximum Usable Frequency (MUF)
- Automatic JS8Call frequency switching
- Detailed explanation of recommendation rationale

To use this example, you'll need:
1. A GPS device connected to your system
2. An OpenWeatherMap API key (set as OPENWEATHERMAP_API_KEY in .env)
3. Internet connectivity for weather and solar data
4. JS8Call running and configured for API access

The script will:
1. Get your location from GPS
2. Fetch current weather and solar conditions
3. Analyze conditions to recommend the best band
4. Explain the rationale behind the recommendation
5. Offer to automatically switch JS8Call to the recommended frequency

Example output:
```
Location: 40.9000°N, -74.3000°E
Time: 14:30 America/New_York

Solar Conditions:
Solar Flux: 125
K-index: 2
Maximum Usable Frequency: 15.2 MHz

What this means:
• Moderate solar activity - Fair conditions for long-distance communication
• Quiet geomagnetic field - Good conditions for HF propagation
• Maximum usable frequency of 15.2 MHz suggests limited high-band propagation

Recommended: 20m (14.078 MHz)

Recommendation rationale:
• Current temperature: 78°F
• Weather conditions: partly cloudy
• Mid-day conditions typically support higher frequency bands
• Early morning/late afternoon conditions favor mid-range frequencies

Would you like to switch JS8Call to this band? (y/n):
```

## Advanced Examples

### Using the Direct Implementation

```python
from JS8CallAPI import JS8CallAPI

api = JS8CallAPI()

try:
    api.connect()
    
    # Get current frequency
    freq = api.get_frequency()
    print(f"Current frequency: {freq['freq']:,} Hz")
    
    # Get current grid and update it
    current_grid = api.get_grid()
    print(f"Current grid: {current_grid}")
    
    # Update grid square (correctly sends in 'value' field)
    success = api.set_grid("FN42")
    if success:
        print("Grid updated successfully")
    
finally:
    api.close()
```

### Messaging Operations

```python
from JS8CallAPI import JS8CallAPI

api = JS8CallAPI()

try:
    api.connect()
    
    # Get the content of the transmit buffer
    tx_text = api.get_tx_text()
    print(f"Current TX text: {tx_text}")
    
    # Set new text to transmit
    api.set_tx_text("CQ CQ CQ DE K1ABC")
    
    # Send a message immediately 
    api.send_message_text("CQ CQ CQ DE K1ABC")
    
    # Get received text
    rx_text = api.get_rx_text()
    print(f"Received text: {rx_text}")
    
    # Store a message in the inbox
    response = api.store_message("W1AW", "Hello from my API script!")
    print(f"Message ID: {response['params'].get('ID')}")
    
    # Get messages from the inbox
    messages = api.get_inbox_messages()
    for msg in messages:
        print(f"From: {msg['params'].get('FROM')}")
        print(f"Text: {msg['params'].get('TEXT')}")
        print(f"Time: {msg['params'].get('UTC')}")
        print("---")
    
finally:
    api.close()
```

### Station Monitoring

```python
from JS8CallAPI import JS8CallAPI
import time
from datetime import datetime

api = JS8CallAPI()

try:
    api.connect()
    
    # Monitor call activity for 60 seconds
    end_time = time.time() + 60
    while time.time() < end_time:
        # Get all recently heard stations
        stations = api.get_call_activity()
        
        print(f"\n--- Station Activity at {datetime.now().strftime('%H:%M:%S')} ---")
        # Display info for each station
        for call, info in stations.items():
            print(f"Call: {call}")
            print(f"  SNR: {info.get('SNR')} dB")
            print(f"  Grid: {info.get('GRID')}")
            print(f"  Time: {datetime.fromtimestamp(info.get('UTC', 0)/1000).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get band activity
        band = api.get_band_activity()
        print(f"\n--- Band Activity: {len(band)} frequencies ---")
        
        time.sleep(10)  # Check every 10 seconds
    
finally:
    api.close()
```

### Mode Control

```python
from JS8CallAPI import JS8CallAPI

api = JS8CallAPI()

try:
    api.connect()
    
    # Get current speed mode
    speed = api.get_speed()
    speed_names = {
        api.JS8_NORMAL: "Normal",
        api.JS8_FAST: "Fast",
        api.JS8_TURBO: "Turbo",
        api.JS8_SLOW: "Slow",
        api.JS8_ULTRA: "Ultra"
    }
    print(f"Current speed: {speed_names.get(speed, 'Unknown')}")
    
    # Set to turbo mode
    api.set_speed(api.JS8_TURBO)
    print("Switched to Turbo mode")
    
    # Set to normal mode
    api.set_speed(api.JS8_NORMAL)
    print("Switched back to Normal mode")
    
finally:
    api.close()
```

### GPS Integration

```python
from JS8CallAPI import JS8CallAPI

api = JS8CallAPI()

try:
    api.connect()
    
    # Get current grid from JS8Call
    js8call_grid = api.get_grid()
    print(f"JS8Call grid: {js8call_grid}")
    
    # Connect to GPS and get current position as grid square
    api.connect_gps()
    gps_grid = api.get_gps_grid_square()
    
    if gps_grid:
        print(f"GPS grid: {gps_grid}")
        
        # Compare and update if different
        if gps_grid.upper() != js8call_grid.upper():
            print("Grid square mismatch detected!")
            success = api.set_grid(gps_grid)
            if success:
                print(f"Grid square updated to: {gps_grid}")
            else:
                print("Error updating grid square")
    
finally:
    api.close()
```

### Frequency Control

```python
from JS8CallAPI import JS8CallAPI
import time

api = JS8CallAPI()

try:
    api.connect()
    
    # Store current frequency
    current_freq = api.get_frequency()
    print(f"Current dial frequency: {current_freq['dial']:,} Hz")
    print(f"Current offset: {current_freq['offset']} Hz")
    print(f"Current operating frequency: {current_freq['freq']:,} Hz")
    
    # Change to 14.078 MHz
    api.set_frequency(dial_freq=14078000)
    print("Changed to 14.078 MHz")
    time.sleep(5)
    
    # Change back to original frequency
    api.set_frequency(dial_freq=current_freq['dial'])
    print(f"Changed back to {current_freq['dial']/1000000:.3f} MHz")
    
finally:
    api.close()
```

---

## API Reference

### JS8CallAPI Class

The main class for interacting with JS8Call's TCP API. This class handles all message formatting and response parsing.

#### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `JS8_NORMAL` | 0 | Normal speed mode (JS8) |
| `JS8_FAST` | 1 | Fast speed mode (JS8Fast) |
| `JS8_TURBO` | 2 | Turbo speed mode (JS8Turbo) |
| `JS8_SLOW` | 3 | Slow speed mode (JS8Slow) |
| `JS8_ULTRA` | 4 | Ultra slow mode (JS8Ultra) |

#### Constructor

```python
JS8CallAPI(host='127.0.0.1', port=2442)
```

**Parameters:**
- `host` (str): JS8Call server hostname/IP (default: '127.0.0.1')
- `port` (int): TCP port for JS8Call API (default: 2442)

### Connection Methods

#### `connect()`
Establishes connection to JS8Call server.

**Returns:** None

**Raises:**
- `ConnectionRefusedError`: If JS8Call is not running or API not enabled
- `Exception`: For other connection errors

#### `connect_gps()`
Connects to GPS daemon (gpsd).

**Returns:** None

**Raises:**
- `Exception`: If connection to gpsd fails

#### `close()`
Closes socket connection to JS8Call.

**Returns:** None

#### `ping()`
Checks if JS8Call is responsive.

**Returns:**
- `bool`: True if JS8Call responds, False otherwise

### Frequency Methods

#### `get_frequency()`
Gets current frequency information.

**Returns:**
```python
{
    'freq': int,    # Operating frequency in Hz
    'dial': int,    # Dial frequency in Hz
    'offset': int   # Frequency offset in Hz
}
```

#### `set_frequency(dial_freq=None, offset=None)`
Sets current frequency.

**Parameters:**
- `dial_freq` (int, optional): Dial frequency in Hz
- `offset` (int, optional): Frequency offset in Hz

**Returns:**
- `bool`: True if command sent successfully

### Station Information Methods

#### `get_callsign()`
Gets current station callsign.

**Returns:**
- `str`: Current station callsign

#### `get_grid()`
Gets current grid locator.

**Returns:**
- `str`: Current Maidenhead grid locator

#### `set_grid(grid)`
Sets current grid locator.

**Parameters:**
- `grid` (str): Maidenhead grid locator to set

**Returns:**
- `bool`: True if successful

#### `get_station_info()`
Gets station information text.

**Returns:**
- `str`: Station information text

#### `set_station_info(info)`
Sets station information text.

**Parameters:**
- `info` (str): Station information text to set

**Returns:**
- `bool`: True if successful

#### `get_status()`
Gets current station status text.

**Returns:**
- `str`: Current status message

#### `set_status(status)`
Sets current station status text.

**Parameters:**
- `status` (str): Status text to set

**Returns:**
- `bool`: True if successful

### Messaging Methods

#### `get_rx_text()`
Gets text from receive window.

**Returns:**
- `str`: Received text (up to 1024 characters)

#### `get_tx_text()`
Gets text from transmit buffer.

**Returns:**
- `str`: Text in transmit buffer

#### `set_tx_text(text)`
Sets text in transmit buffer.

**Parameters:**
- `text` (str): Text to set in transmit buffer

**Returns:**
- `bool`: True if successful

#### `send_message_text(text)`
Sends a message immediately.

**Parameters:**
- `text` (str): Message text to send

**Returns:**
- `bool`: True if command sent successfully

### Activity Monitoring Methods

#### `get_call_activity()`
Gets information about recently heard stations.

**Returns:**
```python
{
    'CALLSIGN1': {
        'SNR': int,        # Signal-to-noise ratio in dB
        'GRID': str,       # Grid square
        'UTC': int         # UTC timestamp in milliseconds
    },
    'CALLSIGN2': {
        # Same structure...
    }
}
```

#### `get_selected_call()`
Gets currently selected callsign in UI.

**Returns:**
- `str`: Selected callsign or empty string if none selected

#### `get_band_activity()`
Gets activity across the band.

**Returns:**
```python
{
    'OFFSET1': {
        'FREQ': int,       # Operating frequency in Hz
        'DIAL': int,       # Dial frequency in Hz
        'OFFSET': int,     # Frequency offset in Hz
        'TEXT': str,       # Decoded text
        'SNR': int,        # Signal-to-noise ratio in dB
        'UTC': int         # UTC timestamp in milliseconds
    },
    'OFFSET2': {
        # Same structure...
    }
}
```

### Mode Control Methods

#### `get_speed()`
Gets current JS8Call speed setting.

**Returns:**
- `int`: Current speed mode (use class constants to interpret)

#### `set_speed(speed)`
Sets JS8Call speed mode.

**Parameters:**
- `speed` (int): Speed mode (use class constants, e.g., JS8_NORMAL)

**Returns:**
- `bool`: True if successful

### Inbox Methods

#### `get_inbox_messages(callsign=None)`
Gets messages from the inbox.

**Parameters:**
- `callsign` (str, optional): Filter messages by callsign

**Returns:**
```python
[
    {
        'type': str,       # Message type
        'value': str,      # Message value
        'params': {
            'FROM': str,   # Sender callsign
            'TO': str,     # Recipient callsign
            'TEXT': str,   # Message text
            'UTC': int     # UTC timestamp in milliseconds
        }
    }
]
```

#### `store_message(callsign, text)`
Stores a message in the inbox.

**Parameters:**
- `callsign` (str): Destination callsign
- `text` (str): Message text

**Returns:**
```python
{
    'type': 'INBOX.MESSAGE',
    'params': {
        '_ID': int,        # Message request ID
        'ID': int          # Stored message ID
    }
}
```

### UI Control Methods

#### `raise_window()`
Raises JS8Call window to foreground.

**Returns:**
- `bool`: True if command sent successfully

### GPS Methods

#### `get_gps_grid_square()`
Gets current grid square from GPS coordinates.

**Returns:**
- `str`: Maidenhead grid square calculated from current GPS position
- `None`: If GPS error or no fix

### Additional Methods

#### `get_directed_message()`
Gets last directed message received.

**Returns:**
- `Optional[Dict[str, Any]]`: Last directed message received

#### `get_spot()`
Gets last spot received.

**Returns:**
- `Optional[Dict[str, Any]]`: Last spot received

#### `get_tx_frame()`
Gets last TX frame sent.

**Returns:**
- `Optional[Dict[str, Any]]`: Last TX frame sent

#### `is_closed()`
Checks if JS8Call connection has been closed.

**Returns:**
- `bool`: True if JS8Call has been closed, False otherwise

---

## Response Data Structures

Most API methods return structured data extracted from the JS8Call API response. The library automatically parses JSON responses and provides appropriate Python data types.

### Frequency Data
```python
{
    'freq': 14074000,      # Current operating frequency in Hz
    'dial': 14073000,      # Current dial frequency in Hz  
    'offset': 1000         # Current offset in Hz
}
```

### Call Activity Data
```python
{
    'K1ABC': {
        'SNR': -5,
        'GRID': 'FN42eq',
        'UTC': 1617981234567
    },
    'W1XYZ': {
        'SNR': 12,
        'GRID': 'EM73',
        'UTC': 1617981234123
    }
}
```

### Inbox Message Data
```python
[
    {
        'type': 'MESSAGE',
        'value': '',
        'params': {
            'FROM': 'K1ABC',
            'TO': 'W1XYZ',
            'TEXT': 'Hello there!',
            'UTC': 1617981234567
        }
    }
]
```

---

## Error Handling

The library includes comprehensive error handling with informative messages for common issues:

```python
from JS8CallAPI import JS8CallAPI

api = JS8CallAPI()

try:
    api.connect()
    
    # Structured error handling for different operations
    try:
        api.connect_gps()
        gps_grid = api.get_gps_grid_square()
        if gps_grid:
            print(f"GPS grid: {gps_grid}")
    except ConnectionError as e:
        print(f"GPS connection error: {e}")
    except TimeoutError as e:
        print(f"GPS timeout: {e}")
    except Exception as e:
        print(f"GPS error: {e}")
    
    # Frequency operations
    try:
        freq = api.get_frequency()
        print(f"Current frequency: {freq['freq']:,} Hz")
    except ConnectionError:
        print("Connection to JS8Call lost")
    except TimeoutError:
        print("JS8Call did not respond in time")
    except Exception as e:
        print(f"Error getting frequency: {e}")
    
finally:
    api.close()
```

---

## Requirements

- **Python 3.6+**: For type annotations and modern language features
- **JS8Call**: Running with TCP API enabled (Settings -> Reporting -> "Enable TCP Server API")
- **gpsd** (optional): For GPS functionality, install with `sudo apt install gpsd` on Linux
- **Network connectivity**: To the JS8Call server

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

For bug reports, please open an issue with a detailed description.

---

## License and Legal

### Copyright Notice
© 2023 Tiran Dagan, [BackstopRadio.com](https://backstopradio.com). All rights reserved.

### MIT License
This project is licensed under the MIT License - see the LICENSE file for details.

### Disclaimer
This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

JS8Call is a separate project created by Jordan Sherer (KN4CRD). This API client is not officially affiliated with or endorsed by JS8Call.

### Amateur Radio Notice
This software is designed for use by licensed amateur radio operators. Users are responsible for ensuring all transmissions comply with local regulations and licensing requirements.

---

## Acknowledgments

- [JS8Call](https://js8call.com/) by Jordan Sherer (KN4CRD)
- [gpsd-py3](https://github.com/MartijnBraam/gpsd-py3) for GPS integration
- All contributors to this project

---

<div align="center">

*Developed with ❤️ for the amateur radio community*  
[BackstopRadio.com](https://backstopradio.com)

</div> 