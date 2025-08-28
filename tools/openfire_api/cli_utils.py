#!/usr/bin/env python3
"""
Shared CLI utilities for OpenFire tools

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
"""

import sys
import click
from typing import Dict


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


def parse_http_headers(header_args: tuple) -> Dict[str, str]:
    """
    Parse HTTP header arguments into a dictionary.
    
    Args:
        header_args: Tuple of header strings in format 'name:value'
        
    Returns:
        Dict[str, str]: Dictionary of headers
    """
    headers = {}
    for header_str in header_args:
        if ':' in header_str:
            name, value = header_str.split(':', 1)
            headers[name.strip()] = value.strip()
    return headers
