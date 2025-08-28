"""
OpenFire API Client

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0

This module provides a client for connecting to the OpenFire REST API.
"""

import requests
from typing import Optional, Tuple, Any


class OpenFireAPIClient:
    """A client for connecting to the OpenFire REST API."""
    
    def __init__(self, base_url: str, username: Optional[str] = None, 
                 password: Optional[str] = None, auth_header: Optional[str] = None, 
                 insecure: bool = False):
        """
        Initialize the OpenFire API client.
        
        Args:
            base_url: The base URL of the OpenFire REST API
            username: Username for basic authentication
            password: Password for basic authentication
            auth_header: Authorization header value
            insecure: Skip SSL certificate validation
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.auth_header = auth_header
        self.insecure = insecure
        self.session = requests.Session()
        
        # Set up authentication
        if auth_header:
            self.session.headers['Authorization'] = auth_header
        
    def _get_auth(self) -> Optional[Tuple[str, str]]:
        """Get authentication tuple for basic auth."""
        if self.username and self.password:
            return (self.username, self.password)
        return None
        
    def _get_headers(self) -> dict:
        """Get headers for the request."""
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        if self.auth_header:
            headers['Authorization'] = self.auth_header
        return headers
        
    def get(self, endpoint: str, params: Optional[dict] = None) -> requests.Response:
        """
        Make a GET request to the OpenFire API.
        
        Args:
            endpoint: The API endpoint to call
            params: Query parameters to include in the request
            
        Returns:
            The response from the API
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        auth = self._get_auth()
        headers = self._get_headers()
        
        response = self.session.get(
            url, 
            auth=auth, 
            headers=headers, 
            params=params,
            verify=not self.insecure
        )
        
        return response
        
    def post(self, endpoint: str, data: Optional[Any] = None, 
             headers: Optional[dict] = None) -> requests.Response:
        """
        Make a POST request to the OpenFire API.
        
        Args:
            endpoint: The API endpoint to call
            data: Data to send in the request body
            headers: Additional headers to include in the request
            
        Returns:
            The response from the API
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        auth = self._get_auth()
        default_headers = self._get_headers()
        if headers:
            default_headers.update(headers)
        
        response = self.session.post(
            url,
            auth=auth,
            headers=default_headers,
            data=data,
            verify=not self.insecure
        )
        
        return response
        
    def put(self, endpoint: str, data: Optional[Any] = None, 
            headers: Optional[dict] = None) -> requests.Response:
        """
        Make a PUT request to the OpenFire API.
        
        Args:
            endpoint: The API endpoint to call
            data: Data to send in the request body
            headers: Additional headers to include in the request
            
        Returns:
            The response from the API
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        auth = self._get_auth()
        default_headers = self._get_headers()
        if headers:
            default_headers.update(headers)
        
        response = self.session.put(
            url,
            auth=auth,
            headers=default_headers,
            data=data,
            verify=not self.insecure
        )
        
        return response
        
    def delete(self, endpoint: str) -> requests.Response:
        """
        Make a DELETE request to the OpenFire API.
        
        Args:
            endpoint: The API endpoint to call
            
        Returns:
            The response from the API
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        auth = self._get_auth()
        headers = self._get_headers()
        
        response = self.session.delete(
            url,
            auth=auth,
            headers=headers,
            verify=not self.insecure
        )
        
        return response
        
    def close(self):
        """Close the session."""
        self.session.close()


def create_client(url: str, username: Optional[str] = None, 
                  password: Optional[str] = None, auth_header: Optional[str] = None, 
                  insecure: bool = False) -> OpenFireAPIClient:
    """
    Create an OpenFire API client.
    
    Args:
        url: The base URL of the OpenFire REST API
        username: Username for basic authentication
        password: Password for basic authentication
        auth_header: Authorization header value
        insecure: Skip SSL certificate validation
        
    Returns:
        An OpenFireAPIClient instance
    """
    return OpenFireAPIClient(url, username, password, auth_header, insecure)
