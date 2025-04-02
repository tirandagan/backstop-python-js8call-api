import socket
import json
import random
import logging
import time
import gpsd
from typing import Dict, List, Optional, Union, Any, Tuple
from .grid_utils import lat_lon_to_grid_square

# Set up logging - but don't display to console by default
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# Create null handler to avoid messages being printed to console
logger.addHandler(logging.NullHandler())

class JS8CallAPI:
    """
    A Python client for the JS8Call TCP API.
    
    This class provides a comprehensive interface to interact with JS8Call's TCP API,
    allowing you to control various aspects of the JS8Call application programmatically.
    
    Attributes:
        host (str): The hostname or IP address of the JS8Call server (default: '127.0.0.1')
        port (int): The TCP port number for the JS8Call API (default: 2442)
        sock (socket.socket): The TCP socket connection to JS8Call
    """
    
    # JS8Call Speed Constants
    JS8_NORMAL = 0
    JS8_FAST = 1
    JS8_TURBO = 2
    JS8_SLOW = 3
    JS8_ULTRA = 4
    
    def __init__(self, host='127.0.0.1', port=2442):
        """
        Initialize the JS8Call API client.
        
        Args:
            host (str): The hostname or IP address of the JS8Call server (default: '127.0.0.1')
            port (int): The TCP port number for the JS8Call API (default: 2442)
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        self._gps_connected = False
        self._closed = False
        self._message_handlers = {
            'CLOSE': self._handle_close,
            'RX.DIRECTED': self._handle_directed,
            'RX.SPOT': self._handle_spot,
            'TX.FRAME': self._handle_tx_frame
        }

    def _handle_close(self, message: Dict[str, Any]) -> None:
        """Handle CLOSE message from JS8Call."""
        self._closed = True
        logger.info("JS8Call closed")

    def _handle_directed(self, message: Dict[str, Any]) -> None:
        """Handle RX.DIRECTED message from JS8Call."""
        params = message.get('params', {})
        logger.info(f"Directed message from {params.get('FROM')}: {params.get('TEXT')}")

    def _handle_spot(self, message: Dict[str, Any]) -> None:
        """Handle RX.SPOT message from JS8Call."""
        params = message.get('params', {})
        logger.info(f"Spot: {params.get('CALL')} at {params.get('FREQ')} Hz")

    def _handle_tx_frame(self, message: Dict[str, Any]) -> None:
        """Handle TX.FRAME message from JS8Call."""
        params = message.get('params', {})
        logger.info(f"TX Frame: {params.get('TEXT')}")

    def connect(self) -> None:
        """
        Connect to the JS8Call TCP server.
        
        Raises:
            ConnectionRefusedError: If the connection is refused (JS8Call not running)
            Exception: For other connection-related errors
        """
        try:
            self.sock.connect((self.host, self.port))
        except ConnectionRefusedError:
            logger.error(f"Connection refused. Make sure JS8Call is running and TCP API is enabled on port {self.port}")
            raise
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    def connect_gps(self) -> None:
        """
        Connect to the GPS daemon (gpsd).
        
        Raises:
            Exception: If connection to gpsd fails
        """
        try:
            gpsd.connect()
            self._gps_connected = True
        except Exception as e:
            logger.error(f"Failed to connect to GPS: {e}")
            self._gps_connected = False
            raise

    def get_gps_grid_square(self) -> Optional[str]:
        """
        Get the current grid square based on GPS coordinates.
        
        Returns:
            str: The Maidenhead grid square calculated from current GPS position, or None if GPS error
        
        Raises:
            Exception: If GPS information cannot be obtained
        """
        if not self._gps_connected:
            self.connect_gps()
        
        try:
            packet = gpsd.get_current()
            if packet.mode < 2:
                raise Exception("No GPS fix available")
            
            return lat_lon_to_grid_square(packet.lat, packet.lon)
        except Exception as e:
            logger.error(f"Error getting GPS grid square: {e}")
            return None
            
    def send_message(self, type: str, value: str = '', params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a message to the JS8Call API server and wait for a response.
        
        Args:
            type (str): The message type (e.g., 'RIG.GET_FREQ')
            value (str): The message value (used for some API calls)
            params (dict): Additional parameters for the message
        
        Returns:
            dict: The parsed response from JS8Call
        
        Raises:
            TimeoutError: If no response is received within the timeout period
            ConnectionError: If the connection is lost
            Exception: For other errors
        """
        if params is None:
            params = {}
            
        # Generate message ID
        msg_id = random.randint(100000000000, 999999999999)
        params['_ID'] = msg_id
        
        # Create message
        message = {
            "type": type,
            "value": value,
            "params": params
        }
        
        # Send message
        message_str = json.dumps(message) + "\n"
        logger.debug(f"Sending: {message_str.strip()}")
        self.sock.sendall(message_str.encode())
        
        # For commands that don't expect responses or have special handling, return immediately
        if type in ["RIG.SET_FREQ", "TX.SEND_MESSAGE", "WINDOW.RAISE"]:
            return {"type": type, "params": params}
        
        # Wait for response
        try:
            while True:
                # Read until newline
                data = b""
                while b"\n" not in data:
                    chunk = self.sock.recv(4096)
                    if not chunk:
                        raise ConnectionError("Connection closed by server")
                    data += chunk
                
                # Process messages
                messages = data.split(b"\n")
                for msg in messages:
                    if not msg:
                        continue
                    try:
                        response = json.loads(msg.decode())
                        logger.debug(f"Received: {msg.decode()}")
                        
                        # Handle special messages
                        msg_type = response.get('type')
                        if msg_type in self._message_handlers:
                            self._message_handlers[msg_type](response)
                        
                        # Check if this is the response we're waiting for
                        response_id = response.get('params', {}).get('_ID')
                        if response_id == msg_id:
                            return response
                    except json.JSONDecodeError:
                        continue
                
        except socket.timeout:
            raise TimeoutError(f"No response received for message type: {type}")
        except Exception as e:
            raise
    
    def get_frequency(self) -> Dict[str, int]:
        """
        Get the current frequency information from JS8Call.
        
        Returns:
            dict: A dictionary containing:
                - freq (int): The actual operating frequency in Hz
                - dial (int): The dial frequency in Hz
                - offset (int): The frequency offset in Hz
        """
        response = self.send_message("RIG.GET_FREQ")
        return {
            'freq': response['params'].get('FREQ', 0),
            'dial': response['params'].get('DIAL', 0),
            'offset': response['params'].get('OFFSET', 0)
        }
    
    def get_callsign(self) -> str:
        """
        Get the current station callsign.
        
        Returns:
            str: The current station callsign
        """
        response = self.send_message("STATION.GET_CALLSIGN")
        return response.get('value', '')
    
    def get_grid(self) -> str:
        """
        Get the current grid locator.
        
        Returns:
            str: The current Maidenhead grid locator
        """
        response = self.send_message("STATION.GET_GRID")
        return response.get('value', '')
    
    def set_grid(self, grid: str) -> bool:
        """
        Set the current grid locator.
        
        Args:
            grid (str): The Maidenhead grid locator to set
        
        Returns:
            bool: True if successful
        """
        # Send grid as 'value', not in 'params'
        response = self.send_message("STATION.SET_GRID", value=grid.upper())
        # Verify by checking the response value
        return response.get('value', '').upper() == grid.upper()
    
    def set_frequency(self, dial_freq: Optional[int] = None, offset: Optional[int] = None) -> bool:
        """
        Set the current frequency.
        
        Args:
            dial_freq (int, optional): The dial frequency in Hz
            offset (int, optional): The frequency offset in Hz
            
        Returns:
            bool: True if the command was sent successfully
        """
        params = {}
        if dial_freq is not None:
            params['DIAL'] = dial_freq
        if offset is not None:
            params['OFFSET'] = offset
        response = self.send_message("RIG.SET_FREQ", params=params)
        return True  # JS8Call doesn't return confirmation for this command
    
    def get_station_info(self) -> str:
        """
        Get the station information text.
        
        Returns:
            str: The station information text
        """
        response = self.send_message("STATION.GET_INFO")
        return response.get('value', '')
    
    def set_station_info(self, info: str) -> bool:
        """
        Set the station information text.
        
        Args:
            info (str): The station information text to set
            
        Returns:
            bool: True if successful
        """
        response = self.send_message("STATION.SET_INFO", value=info)
        return response.get('value', '') == info
    
    def get_status(self) -> str:
        """
        Get the current station status text.
        
        Returns:
            str: The current status message
        """
        response = self.send_message("STATION.GET_STATUS")
        return response.get('value', '')
    
    def set_status(self, status: str) -> bool:
        """
        Set the current station status.
        
        Args:
            status (str): The status text to set
            
        Returns:
            bool: True if successful
        """
        response = self.send_message("STATION.SET_STATUS", value=status)
        return response.get('value', '') == status
    
    def get_call_activity(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about recently heard stations.
        
        Returns:
            dict: Dictionary mapping callsigns to their details:
                {
                    'CALLSIGN1': {
                        'SNR': int,
                        'GRID': str,
                        'UTC': int (UTC timestamp in milliseconds)
                    },
                    ...
                }
        """
        response = self.send_message("RX.GET_CALL_ACTIVITY")
        # Remove the _ID field from the params
        activity = response.get('params', {}).copy()
        if '_ID' in activity:
            del activity['_ID']
        return activity
    
    def get_selected_call(self) -> str:
        """
        Get the currently selected callsign in the UI.
        
        Returns:
            str: The selected callsign or empty string if none selected
        """
        response = self.send_message("RX.GET_CALL_SELECTED")
        return response.get('value', '')
    
    def get_band_activity(self) -> Dict[str, Dict[str, Any]]:
        """
        Get activity across the band.
        
        Returns:
            dict: Dictionary mapping frequency offsets to activity details:
                {
                    'OFFSET1': {
                        'FREQ': int,
                        'DIAL': int,
                        'OFFSET': int,
                        'TEXT': str,
                        'SNR': int,
                        'UTC': int (UTC timestamp in milliseconds)
                    },
                    ...
                }
        """
        response = self.send_message("RX.GET_BAND_ACTIVITY")
        # Remove the _ID field from the params
        activity = response.get('params', {}).copy()
        if '_ID' in activity:
            del activity['_ID']
        return activity
    
    def get_rx_text(self) -> str:
        """
        Get text from the receive window.
        
        Returns:
            str: The received text (up to 1024 characters)
        """
        response = self.send_message("RX.GET_TEXT")
        return response.get('value', '')
    
    def get_tx_text(self) -> str:
        """
        Get text from the transmit buffer.
        
        Returns:
            str: The text in the transmit buffer
        """
        response = self.send_message("TX.GET_TEXT")
        return response.get('value', '')
    
    def set_tx_text(self, text: str) -> bool:
        """
        Set text in the transmit buffer.
        
        Args:
            text (str): The text to set in the transmit buffer
            
        Returns:
            bool: True if successful
        """
        response = self.send_message("TX.SET_TEXT", value=text)
        return response.get('value', '') == text
    
    def send_message_text(self, text: str) -> bool:
        """
        Send a message immediately.
        
        Args:
            text (str): The message text to send
            
        Returns:
            bool: True if the command was sent successfully
        """
        self.send_message("TX.SEND_MESSAGE", value=text)
        return True  # JS8Call doesn't return confirmation for this command
    
    def get_speed(self) -> int:
        """
        Get the current JS8Call speed setting.
        
        Returns:
            int: The current speed mode (see JS8Call speed constants)
        """
        response = self.send_message("MODE.GET_SPEED")
        return response['params'].get('SPEED', self.JS8_NORMAL)
    
    def set_speed(self, speed: int) -> bool:
        """
        Set the JS8Call speed mode.
        
        Args:
            speed (int): The speed mode (use class constants, e.g., JS8_NORMAL)
            
        Returns:
            bool: True if successful
        """
        response = self.send_message("MODE.SET_SPEED", params={'SPEED': speed})
        return response['params'].get('SPEED', -1) == speed
    
    def get_inbox_messages(self, callsign: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get messages from the inbox.
        
        Args:
            callsign (str, optional): Filter messages by callsign
            
        Returns:
            list: List of message objects with the following structure:
                [
                    {
                        'type': str,
                        'value': str,
                        'params': {
                            'FROM': str,
                            'TO': str,
                            'TEXT': str,
                            'UTC': int (timestamp)
                        }
                    },
                    ...
                ]
        """
        params = {}
        if callsign:
            params['CALLSIGN'] = callsign
        response = self.send_message("INBOX.GET_MESSAGES", params=params)
        return response['params'].get('MESSAGES', [])
    
    def store_message(self, callsign: str, text: str) -> Dict[str, Any]:
        """
        Store a message in the inbox.
        
        Args:
            callsign (str): Destination callsign
            text (str): Message text
            
        Returns:
            dict: The response containing the message ID:
                {
                    'type': 'INBOX.MESSAGE',
                    'params': {
                        '_ID': int,
                        'ID': int (message ID)
                    }
                }
        """
        params = {
            'CALLSIGN': callsign,
            'TEXT': text
        }
        return self.send_message("INBOX.STORE_MESSAGE", params=params)
    
    def raise_window(self) -> bool:
        """
        Raise the JS8Call window to the foreground.
        
        Returns:
            bool: True if the command was sent successfully
        """
        self.send_message("WINDOW.RAISE")
        return True  # JS8Call doesn't return confirmation for this command
    
    def ping(self) -> bool:
        """
        Send a PING message to check if JS8Call is responsive.
        
        Unlike other API calls, PING uses a simpler approach that doesn't wait
        for a specific response. The connection is considered successful
        if we can send the message without errors.
        
        Returns:
            bool: True if message was sent successfully (JS8Call is responsive)
        """
        try:
            # Add standard parameters based on JS8Call's implementation
            params = {
                "NAME": "JS8CallAPI",
                "VERSION": "1.0",
                "UTC": int(time.time() * 1000)  # Current time in milliseconds
            }
            
            # Simple implementation - just try to send a message
            # Don't wait for a response since JS8Call may not respond to pings
            message = {
                "type": "PING",
                "value": "",
                "params": params
            }
            
            message_str = json.dumps(message) + "\n"
            self.sock.sendall(message_str.encode())
            
            # A successful send indicates JS8Call is responsive
            return True
        except Exception as e:
            logger.error(f"Ping failed: {e}")
            return False
        
    def get_ptt_status(self) -> bool:
        """
        Get the current PTT status.
        
        Returns:
            bool: True if PTT is active, False otherwise
        """
        response = self.send_message("RIG.GET_PTT")
        return response.get('params', {}).get('PTT', False)

    def close(self) -> None:
        """Close the socket connection to JS8Call."""
        try:
            self.sock.close()
        except:
            pass

    def is_closed(self) -> bool:
        """
        Check if JS8Call has been closed.
        
        Returns:
            bool: True if JS8Call has been closed, False otherwise
        """
        return self._closed

    def get_directed_message(self) -> Optional[Dict[str, Any]]:
        """
        Get the last directed message received.
        
        Returns:
            Optional[Dict[str, Any]]: The directed message details or None if no message:
                {
                    'FROM': str,      # Sender callsign
                    'TO': str,        # Recipient callsign
                    'TEXT': str,      # Message text
                    'UTC': int        # UTC timestamp in milliseconds
                }
        """
        response = self.send_message("RX.GET_DIRECTED")
        params = response.get('params', {})
        if not params:
            return None
        return {
            'FROM': params.get('FROM', ''),
            'TO': params.get('TO', ''),
            'TEXT': params.get('TEXT', ''),
            'UTC': params.get('UTC', 0)
        }

    def get_spot(self) -> Optional[Dict[str, Any]]:
        """
        Get the last spot received.
        
        Returns:
            Optional[Dict[str, Any]]: The spot details or None if no spot:
                {
                    'CALL': str,      # Station callsign
                    'FREQ': int,      # Frequency in Hz
                    'SNR': int,       # Signal-to-noise ratio
                    'UTC': int        # UTC timestamp in milliseconds
                }
        """
        response = self.send_message("RX.GET_SPOT")
        params = response.get('params', {})
        if not params:
            return None
        return {
            'CALL': params.get('CALL', ''),
            'FREQ': params.get('FREQ', 0),
            'SNR': params.get('SNR', 0),
            'UTC': params.get('UTC', 0)
        }

    def get_tx_frame(self) -> Optional[Dict[str, Any]]:
        """
        Get the last TX frame sent.
        
        Returns:
            Optional[Dict[str, Any]]: The TX frame details or None if no frame:
                {
                    'TEXT': str,      # Frame text
                    'UTC': int        # UTC timestamp in milliseconds
                }
        """
        response = self.send_message("TX.GET_FRAME")
        params = response.get('params', {})
        if not params:
            return None
        return {
            'TEXT': params.get('TEXT', ''),
            'UTC': params.get('UTC', 0)
        } 