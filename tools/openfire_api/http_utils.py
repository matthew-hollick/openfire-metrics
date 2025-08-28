#!/usr/bin/env python3
"""
Shared HTTP utilities for OpenFire tools

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
"""

import sys
import requests
from typing import Dict, List, Optional, Union


def send_to_http_endpoint(
    data: Union[Dict, List, str],
    url: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None
) -> bool:
    """
    Send data to an HTTP endpoint.
    
    Args:
        data: Data to send (dict, list, or string)
        url: Destination URL
        username: HTTP Basic Auth username
        password: HTTP Basic Auth password
        headers: Additional HTTP headers
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Prepare headers
    request_headers = {
        'User-Agent': 'OpenFire-Metrics-Tool/1.0'
    }
    
    # Add custom headers
    if headers:
        request_headers.update(headers)
    
    # Prepare auth
    auth = None
    if username and password:
        auth = (username, password)
    
    try:
        # Send POST request with appropriate data parameter
        if isinstance(data, (dict, list)):
            # For structured data, use json= parameter which automatically sets Content-Type
            response = requests.post(
                url,
                json=data,
                headers=request_headers,
                auth=auth,
                timeout=30
            )
        else:
            # For string data, use data= parameter
            # Only set Content-Type if explicitly provided in headers
            if 'Content-Type' not in request_headers and headers:
                request_headers['Content-Type'] = 'text/plain'
            elif 'Content-Type' not in request_headers:
                request_headers['Content-Type'] = 'text/plain'
            
            response = requests.post(
                url,
                data=data,
                headers=request_headers,
                auth=auth,
                timeout=30
            )
        
        # Check if request was successful
        response.raise_for_status()
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to HTTP endpoint: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False


def parse_http_header(header_str: str) -> Dict[str, str]:
    """
    Parse an HTTP header string in format 'name:value' into a dictionary.
    
    Args:
        header_str: Header string in format 'name:value'
        
    Returns:
        Dict[str, str]: Dictionary with header name as key and value as value
    """
    if not header_str or ':' not in header_str:
        return {}
    
    name, value = header_str.split(':', 1)
    return {name.strip(): value.strip()}


def validate_http_destination(url: str) -> bool:
    """
    Validate that a URL is a valid HTTP/HTTPS destination.
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not url:
        return False
    
    return url.startswith(('http://', 'https://'))
