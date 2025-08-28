#!/usr/bin/env python3
"""
Shared HTTP utilities for OpenFire tools

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
"""

import sys
import os.path
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, List, Optional, Union, Tuple, Any

# Default CA certificate path
DEFAULT_CA_CERT_PATH = '/etc/ssl/certs/ca-certificates.crt'

# Global session for connection pooling
_SESSION = None

# Default retry configuration
DEFAULT_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.3
DEFAULT_STATUS_FORCELIST = [500, 502, 503, 504]


def get_session(retries: int = DEFAULT_RETRIES, 
               backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
               status_forcelist: List[int] = None) -> requests.Session:
    """
    Get a requests session with connection pooling and retry configuration.
    
    Args:
        retries: Number of retries for failed requests
        backoff_factor: Backoff factor for retries
        status_forcelist: List of status codes to retry on
        
    Returns:
        requests.Session: Configured session object
    """
    global _SESSION
    
    if _SESSION is None:
        _SESSION = requests.Session()
        
        # Configure retry strategy
        if status_forcelist is None:
            status_forcelist = DEFAULT_STATUS_FORCELIST
            
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        
        # Mount the adapter to the session
        adapter = HTTPAdapter(max_retries=retry_strategy, 
                             pool_connections=10,  # Number of connection pools
                             pool_maxsize=100)     # Connections per pool
        _SESSION.mount("http://", adapter)
        _SESSION.mount("https://", adapter)
        
    return _SESSION


def send_to_http_endpoint(
    data: Union[Dict, List, str],
    url: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    verify: Union[bool, str] = True
) -> bool:
    """
    Send data to an HTTP endpoint.
    
    Args:
        data: Data to send (dict, list, or string)
        url: Destination URL
        username: HTTP Basic Auth username
        password: HTTP Basic Auth password
        headers: Additional HTTP headers
        verify: SSL verification option
        
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
    auth = get_auth(username, password)
    
    # Determine if we should use insecure mode
    insecure = verify is False
    
    try:
        # Send POST request with appropriate data parameter
        if isinstance(data, (dict, list)):
            # For structured data, use json= parameter which automatically sets Content-Type
            response = make_request(
                method='POST',
                url=url,
                json_data=data,
                headers=request_headers,
                auth=auth,
                timeout=30,
                insecure=insecure
            )
        else:
            # For string data, use data= parameter
            # Only set Content-Type if explicitly provided in headers
            if 'Content-Type' not in request_headers and headers:
                request_headers['Content-Type'] = 'text/plain'
            elif 'Content-Type' not in request_headers:
                request_headers['Content-Type'] = 'text/plain'
            
            response = make_request(
                method='POST',
                url=url,
                data=data,
                headers=request_headers,
                auth=auth,
                timeout=30,
                insecure=insecure
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


def get_verify_option(insecure: bool) -> Union[bool, str]:
    """
    Get the appropriate verify option for requests based on insecure flag.
    
    Args:
        insecure: Whether to skip SSL certificate validation
        
    Returns:
        Union[bool, str]: Path to CA cert file or False if insecure
    """
    if insecure:
        return False
    elif os.path.exists(DEFAULT_CA_CERT_PATH):
        return DEFAULT_CA_CERT_PATH
    else:
        return True


def get_auth(username: Optional[str], password: Optional[str]) -> Optional[Tuple[str, str]]:
    """
    Get authentication tuple for basic auth.
    
    Args:
        username: Username for basic authentication
        password: Password for basic authentication
        
    Returns:
        Optional[Tuple[str, str]]: Auth tuple or None
    """
    if username and password:
        return (username, password)
    return None


def get_default_headers(auth_header: Optional[str] = None) -> Dict[str, str]:
    """
    Get default headers for API requests.
    
    Args:
        auth_header: Optional authorization header value
        
    Returns:
        Dict[str, str]: Headers dictionary
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'OpenFire-Metrics-Tool/1.0'
    }
    
    if auth_header:
        headers['Authorization'] = auth_header
        
    return headers


def make_request(
    method: str, 
    url: str, 
    auth: Optional[Tuple[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None,
    data: Optional[Any] = None,
    json_data: Optional[Dict] = None,
    insecure: bool = False,
    timeout: int = 30,
    retries: int = DEFAULT_RETRIES
) -> requests.Response:
    """
    Make an HTTP request with consistent handling.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        url: URL to request
        auth: Authentication tuple
        headers: Request headers
        params: Query parameters
        data: Request body data
        json_data: JSON data for request body
        insecure: Whether to skip SSL certificate validation
        timeout: Request timeout in seconds
        retries: Number of retries for failed requests
        
    Returns:
        requests.Response: Response object
    """
    verify = get_verify_option(insecure)
    session = get_session(retries=retries)
    
    # Use the session for the request
    return session.request(
        method=method.upper(),
        url=url,
        auth=auth,
        headers=headers,
        params=params,
        data=data,
        json=json_data,
        verify=verify,
        timeout=timeout
    )
