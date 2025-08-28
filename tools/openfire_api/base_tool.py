#!/usr/bin/env python3
"""
Base tool class for OpenFire tools

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0
"""

import argparse
import sys
import os

# Add the parent directory to the path so we can import the openfire_api module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from http_utils import send_to_http_endpoint
from cli_utils import parse_http_headers
from format_utils import format_as_json


class BaseTool:
    """
    Base class for OpenFire tools.
    """
    
    def __init__(self, description: str):
        """
        Initialize the base tool.
        
        Args:
            description: Tool description
        """
        self.parser = argparse.ArgumentParser(description=description)
        self.args = None
        self._add_common_arguments()
    
    def _add_common_arguments(self):
        """Add common command-line arguments."""
        self.parser.add_argument('--url', default='http://localhost:9090/plugins/restapi/v1',
                            help='OpenFire REST API URL')
        self.parser.add_argument('--auth-header', required=True,
                            help='Authorization header value')
        self.parser.add_argument('--insecure', action='store_true',
                            help='Skip SSL certificate validation')
        self.parser.add_argument('--output-format', choices=['json', 'text', 'http'], default='json',
                            help='Output format (json, text, or http)')
        self.parser.add_argument('--output-destination', help='HTTP endpoint URL for output')
        self.parser.add_argument('--http-username', help='Username for HTTP basic auth')
        self.parser.add_argument('--http-password', help='Password for HTTP basic auth')
        self.parser.add_argument('--http-header', action='append', help='Custom headers for HTTP requests (format: name:value)')
    
    def parse_args(self):
        """Parse command-line arguments."""
        self.args = self.parser.parse_args()
        return self.args
    
    def output_data(self, data):
        """
        Output data in the specified format.
        
        Args:
            data: Data to output
        """
        if self.args.output_format == 'json':
            print(format_as_json(data))
        elif self.args.output_format == 'http':
            if not self.args.output_destination:
                raise Exception("HTTP output format requires --output-destination")
            # Parse custom headers
            http_headers = {}
            if self.args.http_header:
                http_headers = parse_http_headers(self.args.http_header)
            username = self.args.http_username
            password = self.args.http_password
            send_to_http_endpoint(data, self.args.output_destination, 
                                username, password, http_headers)
            print("Data sent to HTTP endpoint successfully")
        else:
            self._output_as_text(data)
    
    def _output_as_text(self, data):
        """
        Output data as text (to be implemented by subclasses).
        
        Args:
            data: Data to output
        """
        raise NotImplementedError("Subclasses must implement _output_as_text method")
