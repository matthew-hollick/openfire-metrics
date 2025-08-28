#!/usr/bin/env python3
"""
Authentication utilities for OpenFire API

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
"""

from typing import Dict, Optional, Tuple


class AuthManager:
    """
    Manages authentication for OpenFire API requests.
    Centralizes all authentication methods in one place.
    """
    
    def __init__(
        self, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        auth_header: Optional[str] = None
    ):
        """
        Initialize the authentication manager.
        
        Args:
            username: Username for basic authentication
            password: Password for basic authentication
            auth_header: Authorization header value
        """
        self.username = username
        self.password = password
        self.auth_header = auth_header
        
    def get_auth_tuple(self) -> Optional[Tuple[str, str]]:
        """
        Get authentication tuple for basic auth.
        
        Returns:
            Optional[Tuple[str, str]]: Auth tuple or None
        """
        if self.username and self.password:
            return (self.username, self.password)
        return None
        
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers.
        
        Returns:
            Dict[str, str]: Headers dictionary with auth information
        """
        headers = {}
        if self.auth_header:
            headers['Authorization'] = self.auth_header
        return headers
        
    def update_session_auth(self, session) -> None:
        """
        Update a requests.Session object with authentication.
        
        Args:
            session: requests.Session object to update
        """
        if self.auth_header:
            session.headers['Authorization'] = self.auth_header


def create_auth_manager(
    username: Optional[str] = None, 
    password: Optional[str] = None,
    auth_header: Optional[str] = None
) -> AuthManager:
    """
    Create an authentication manager.
    
    Args:
        username: Username for basic authentication
        password: Password for basic authentication
        auth_header: Authorization header value
        
    Returns:
        AuthManager: Authentication manager instance
    """
    return AuthManager(username, password, auth_header)


def get_auth_tuple(
    username: Optional[str], 
    password: Optional[str]
) -> Optional[Tuple[str, str]]:
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


def get_auth_headers(auth_header: Optional[str] = None) -> Dict[str, str]:
    """
    Get authentication headers.
    
    Args:
        auth_header: Authorization header value
        
    Returns:
        Dict[str, str]: Headers dictionary with auth information
    """
    headers = {}
    if auth_header:
        headers['Authorization'] = auth_header
    return headers
