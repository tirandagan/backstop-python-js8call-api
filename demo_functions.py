#!/usr/bin/env python3
"""
Supporting functions for the JS8Call API Python Client Demo

This module contains utility functions used by the demo.py script to format
output, handle user input, and manage the UI of the demo application.

Copyright (c) 2023 Tiran Dagan, BackstopRadio.com
Licensed under MIT License
"""

import os
import sys
import platform
import time
from datetime import datetime
import json

# Terminal colors - will be disabled if not supported
COLORS_ENABLED = True
if platform.system() == "Windows":
    try:
        import colorama
        colorama.init()
    except ImportError:
        COLORS_ENABLED = False

# Color codes
class Colors:
    HEADER = '\033[95m' if COLORS_ENABLED else ''
    BLUE = '\033[94m' if COLORS_ENABLED else ''
    CYAN = '\033[96m' if COLORS_ENABLED else ''
    GREEN = '\033[92m' if COLORS_ENABLED else ''
    YELLOW = '\033[93m' if COLORS_ENABLED else ''
    RED = '\033[91m' if COLORS_ENABLED else ''
    BOLD = '\033[1m' if COLORS_ENABLED else ''
    UNDERLINE = '\033[4m' if COLORS_ENABLED else ''
    END = '\033[0m' if COLORS_ENABLED else ''

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_header(title):
    """Print a main header"""
    width = min(os.get_terminal_size().columns, 80) if hasattr(os, 'get_terminal_size') else 80
    print(f"\n{Colors.HEADER}{Colors.BOLD}" + "=" * width + f"{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}  {title.center(width-4)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}" + "=" * width + f"{Colors.END}")

def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BLUE}" + "-" * len(title) + f"{Colors.END}")

def print_subsection(title):
    """Print a subsection header"""
    print(f"\n{Colors.CYAN}• {title}{Colors.END}")

def print_info(message):
    """Print an info message"""
    print(f"{Colors.GREEN}ℹ {message}{Colors.END}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.RED}✖ {message}{Colors.END}")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_data(label, value, unit=""):
    """Print a labeled data value"""
    print(f"  {Colors.BOLD}{label}:{Colors.END} {value}{unit}")

def print_json(label, data):
    """Print JSON data with indentation"""
    print(f"  {Colors.BOLD}{label}:{Colors.END}")
    formatted = json.dumps(data, indent=2)
    for line in formatted.split('\n'):
        print(f"    {line}")

def prompt_continue():
    """Prompt user to continue"""
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def prompt_yes_no(question):
    """Prompt for yes/no answer"""
    # Strip any trailing punctuation and spaces to prevent duplication in the prompt
    if question.endswith('?'):
        # Remove ? to avoid displaying "? (y/n): "
        question = question[:-1].strip()
        
    sys.stdout.write(f"{Colors.YELLOW}{question}? (y/n): {Colors.END}")
    sys.stdout.flush()
    
    while True:
        response = input().lower().strip()
        if not response:
            # Re-prompt without duplicating the question
            sys.stdout.write(f"{Colors.YELLOW}Please enter y or n: {Colors.END}")
            sys.stdout.flush()
            continue
        elif response[0] in ['y']:
            return True
        elif response[0] in ['n']:
            return False
        else:
            # Re-prompt without duplicating the question
            sys.stdout.write(f"{Colors.YELLOW}Please enter y or n: {Colors.END}")
            sys.stdout.flush()

def print_test_description(title, description):
    """Print a test description block"""
    print_section(title)
    lines = description.strip().split('\n')
    for line in lines:
        print(f"{Colors.GREEN}  {line.strip()}{Colors.END}")
    print()

def ensure_connected(api):
    """Make sure API is connected, connect if not"""
    try:
        # Try a ping to check connection
        api.ping()
    except:
        # Not connected, try to connect
        print_info("Not connected to JS8Call. Connecting...")
        try:
            api.connect()
            print_success("Connected to JS8Call")
        except Exception as e:
            print_error(f"Failed to connect: {e}")
            raise 