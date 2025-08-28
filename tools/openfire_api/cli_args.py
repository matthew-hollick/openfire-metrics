#!/usr/bin/env python3
"""
Consolidated CLI argument handling for OpenFire tools

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
"""

import sys
import argparse
import click
from typing import Dict, List, Optional, Any, Callable

from .format_utils import format_as_json, format_as_text
from .http_utils import send_to_http_endpoint
from .error_utils import handle_request_error


class ArgumentParser:
    """
    Enhanced argument parser for OpenFire tools.
    Provides consistent argument handling across all tools.
    """
    
    def __init__(self, description: str):
        """
        Initialize the argument parser.
        
        Args:
            description: Tool description
        """
        self.parser = argparse.ArgumentParser(description=description)
        self.args = None
        
    def add_common_arguments(self):
        """Add common command-line arguments for OpenFire tools."""
        self.parser.add_argument('--url', default='http://localhost:9090/plugins/restapi/v1',
                            help='OpenFire REST API URL')
        self.parser.add_argument('--auth-header', required=True,
                            help='Authorization header value')
        self.parser.add_argument('--insecure', action='store_true',
                            help='Skip SSL certificate validation')
        self._add_output_arguments()
        
        return self
        
    def _add_output_arguments(self):
        """Add output-related command-line arguments."""
        self.parser.add_argument('--output-format', choices=['json', 'text', 'http'], default='json',
                            help='Output format (json, text, or http)')
        self.parser.add_argument('--output-destination', help='HTTP endpoint URL for output')
        self.parser.add_argument('--http-username', help='Username for HTTP basic auth')
        self.parser.add_argument('--http-password', help='Password for HTTP basic auth')
        self.parser.add_argument('--http-header', action='append', help='Custom headers for HTTP requests (format: name:value)')
        
    def add_argument(self, *args, **kwargs):
        """
        Add an argument to the parser.
        
        Args:
            *args: Positional arguments for argparse.add_argument
            **kwargs: Keyword arguments for argparse.add_argument
            
        Returns:
            self: For method chaining
        """
        self.parser.add_argument(*args, **kwargs)
        return self
        
    def add_mutually_exclusive_group(self, required: bool = False):
        """
        Add a mutually exclusive argument group.
        
        Args:
            required: Whether one of the arguments in the group is required
            
        Returns:
            group: The mutually exclusive group
        """
        return self.parser.add_mutually_exclusive_group(required=required)
        
    def parse_args(self):
        """
        Parse command-line arguments.
        
        Returns:
            args: Parsed arguments
        """
        self.args = self.parser.parse_args()
        
        # Validate HTTP output options
        if self.args.output_format == 'http':
            if not self.args.output_destination:
                print("Error: --output-destination is required when --output-format is 'http'", file=sys.stderr)
                sys.exit(1)
            if not self.args.output_destination.startswith(('http://', 'https://')):
                print("Error: --output-destination must be a valid HTTP/HTTPS URL", file=sys.stderr)
                sys.exit(1)
                
        return self.args
        
    def output_data(self, data: Any, text_formatter: Optional[Callable[[Any], str]] = None):
        """
        Output data in the specified format.
        
        Args:
            data: Data to output
            text_formatter: Function to format data as text (if None, uses format_as_text)
        """
        if not self.args:
            raise ValueError("Arguments not parsed. Call parse_args() first.")
            
        try:
            if self.args.output_format == 'json':
                print(format_as_json(data))
            elif self.args.output_format == 'http':
                # Parse custom headers
                http_headers = {}
                if self.args.http_header:
                    http_headers = parse_http_headers(self.args.http_header)
                    
                # Use the insecure flag to determine SSL verification
                verify = not self.args.insecure if hasattr(self.args, 'insecure') else True
                
                send_to_http_endpoint(
                    data, 
                    self.args.output_destination,
                    self.args.http_username, 
                    self.args.http_password, 
                    http_headers, 
                    verify=verify
                )
                print("Data sent to HTTP endpoint successfully")
            else:  # text format
                if text_formatter:
                    print(text_formatter(data))
                else:
                    print(format_as_text(data))
        except Exception as e:
            handle_request_error(e, "Output error")
            sys.exit(1)


def parse_http_headers(header_args: List[str]) -> Dict[str, str]:
    """
    Parse HTTP header arguments into a dictionary.
    
    Args:
        header_args: List of header strings in format 'name:value'
        
    Returns:
        Dict[str, str]: Dictionary of headers
    """
    headers = {}
    for header_str in header_args:
        if ':' in header_str:
            name, value = header_str.split(':', 1)
            headers[name.strip()] = value.strip()
    return headers


# Click-based decorators for CLI tools
def add_standard_api_options(func):
    """
    Decorator to add standard OpenFire API options to Click commands.
    
    Args:
        func: Click command function to decorate
        
    Returns:
        Decorated function with standard API options
    """
    # Add URL option
    func = click.option(
        '--url',
        default='http://localhost:9090/plugins/restapi/v1',
        help='OpenFire REST API URL'
    )(func)
    
    # Add auth header option
    func = click.option(
        '--auth-header',
        required=True,
        help='Authorization header value'
    )(func)
    
    # Add insecure option
    func = click.option(
        '--insecure',
        is_flag=True,
        help='Skip SSL certificate validation'
    )(func)
    
    return func


def add_standard_output_options(func):
    """
    Decorator to add standard output options to Click commands.
    
    Args:
        func: Click command function to decorate
        
    Returns:
        Decorated function with standard output options
    """
    # Add output format option
    func = click.option(
        '--output-format',
        type=click.Choice(['json', 'text', 'http'], case_sensitive=False),
        default='json',
        help='Output format'
    )(func)
    
    # Add output destination option
    func = click.option(
        '--output-destination',
        help='HTTP endpoint URL for HTTP output format'
    )(func)
    
    # Add HTTP username option
    func = click.option(
        '--http-username',
        help='Username for HTTP Basic Authentication'
    )(func)
    
    # Add HTTP password option
    func = click.option(
        '--http-password',
        help='Password for HTTP Basic Authentication'
    )(func)
    
    # Add HTTP header option
    func = click.option(
        '--http-header',
        help='Custom HTTP header in format name:value',
        multiple=True
    )(func)
    
    return func


def validate_http_options(output_format: str, output_destination: str) -> bool:
    """
    Validate HTTP output options.
    
    Args:
        output_format: Output format (json, text, http)
        output_destination: HTTP endpoint URL
        
    Returns:
        bool: True if valid, False otherwise
    """
    if output_format == 'http':
        if not output_destination:
            print("Error: --output-destination is required when --output-format is 'http'", file=sys.stderr)
            return False
        if not output_destination.startswith(('http://', 'https://')):
            print("Error: --output-destination must be a valid HTTP/HTTPS URL", file=sys.stderr)
            return False
    return True
