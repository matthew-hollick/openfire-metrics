#!/usr/bin/env python3
"""
Error handling utilities for OpenFire API

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
"""

import sys
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('openfire_api')


class OpenFireAPIError(Exception):
    """Base exception for all OpenFire API errors."""
    pass


class AuthenticationError(OpenFireAPIError):
    """Authentication error."""
    pass


class ConnectionError(OpenFireAPIError):
    """Connection error."""
    pass


class ResourceNotFoundError(OpenFireAPIError):
    """Resource not found error."""
    pass


class ValidationError(OpenFireAPIError):
    """Validation error."""
    pass


class ServerError(OpenFireAPIError):
    """Server error."""
    pass


def handle_request_error(error: Exception, context: Optional[str] = None) -> None:
    """
    Handle request errors consistently.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    """
    error_prefix = f"{context}: " if context else ""
    
    if hasattr(error, 'response') and error.response is not None:
        status_code = error.response.status_code
        
        if status_code == 401:
            logger.error(f"{error_prefix}Authentication failed (401)")
            print("Error: Authentication failed. Please check your credentials.", file=sys.stderr)
        elif status_code == 403:
            logger.error(f"{error_prefix}Permission denied (403)")
            print("Error: Permission denied. Your account doesn't have access to this resource.", file=sys.stderr)
        elif status_code == 404:
            logger.error(f"{error_prefix}Resource not found (404)")
            print("Error: Resource not found. The requested endpoint doesn't exist.", file=sys.stderr)
        elif 400 <= status_code < 500:
            logger.error(f"{error_prefix}Client error: {status_code}")
            print(f"Error: Client error ({status_code}). {str(error)}", file=sys.stderr)
        elif 500 <= status_code < 600:
            logger.error(f"{error_prefix}Server error: {status_code}")
            print(f"Error: Server error ({status_code}). Please try again later.", file=sys.stderr)
        else:
            logger.error(f"{error_prefix}HTTP error: {status_code}")
            print(f"Error: HTTP error ({status_code}). {str(error)}", file=sys.stderr)
    else:
        logger.error(f"{error_prefix}Request failed: {str(error)}")
        print(f"Error: Request failed. {str(error)}", file=sys.stderr)


def raise_for_status(response, context: Optional[str] = None) -> None:
    """
    Check response status and raise appropriate exception.
    
    Args:
        response: Response object
        context: Additional context about where the error occurred
        
    Raises:
        AuthenticationError: If status code is 401
        ResourceNotFoundError: If status code is 404
        ValidationError: If status code is 400
        ServerError: If status code is 500
        OpenFireAPIError: For other error status codes
    """
    if response.status_code >= 400:
        error_prefix = f"{context}: " if context else ""
        
        if response.status_code == 401:
            raise AuthenticationError(f"{error_prefix}Authentication failed")
        elif response.status_code == 404:
            raise ResourceNotFoundError(f"{error_prefix}Resource not found")
        elif response.status_code == 400:
            raise ValidationError(f"{error_prefix}Invalid request")
        elif response.status_code >= 500:
            raise ServerError(f"{error_prefix}Server error")
        else:
            raise OpenFireAPIError(f"{error_prefix}HTTP error {response.status_code}")


def log_request(method: str, url: str, params: Optional[Dict[str, Any]] = None) -> None:
    """
    Log request details.
    
    Args:
        method: HTTP method
        url: Request URL
        params: Request parameters
    """
    logger.debug(f"Request: {method} {url}")
    if params:
        logger.debug(f"Params: {params}")


def log_response(response, include_body: bool = False) -> None:
    """
    Log response details.
    
    Args:
        response: Response object
        include_body: Whether to include response body in log
    """
    logger.debug(f"Response: {response.status_code} {response.reason}")
    if include_body and response.content:
        try:
            logger.debug(f"Body: {response.text[:1000]}")
        except Exception:
            logger.debug("Could not log response body")
