#!/usr/bin/env python3
"""
Unit tests for the base tool class.
"""

import unittest
import sys
import os

# Add the tools directory to the path so we can import the base tool class
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

from base_tool import BaseTool


class TestBaseTool(unittest.TestCase):
    """Test cases for the base tool class."""
    
    def test_initialization(self):
        """Test that the base tool initializes correctly."""
        tool = BaseTool("Test tool")
        self.assertIsNotNone(tool.parser)
        self.assertIsNone(tool.args)
    
    def test_common_arguments(self):
        """Test that common arguments are added correctly."""
        tool = BaseTool("Test tool")
        args = tool.parser.parse_args(['--auth-header', 'test'])
        
        # Check that common arguments are present
        self.assertEqual(args.url, 'http://localhost:9090/plugins/restapi/v1')
        self.assertEqual(args.auth_header, 'test')
        self.assertEqual(args.output_format, 'json')
        self.assertFalse(args.insecure)
    
    def test_output_format_choices(self):
        """Test that output format choices are correct."""
        tool = BaseTool("Test tool")
        
        # Test valid choices
        args = tool.parser.parse_args(['--auth-header', 'test', '--output-format', 'json'])
        self.assertEqual(args.output_format, 'json')
        
        args = tool.parser.parse_args(['--auth-header', 'test', '--output-format', 'text'])
        self.assertEqual(args.output_format, 'text')
        
        args = tool.parser.parse_args(['--auth-header', 'test', '--output-format', 'http'])
        self.assertEqual(args.output_format, 'http')
    
    def test_http_arguments(self):
        """Test that HTTP arguments are added correctly."""
        tool = BaseTool("Test tool")
        args = tool.parser.parse_args([
            '--auth-header', 'test',
            '--output-format', 'http',
            '--output-destination', 'http://example.com',
            '--http-username', 'user',
            '--http-password', 'pass',
            '--http-header', 'X-Custom: value'
        ])
        
        self.assertEqual(args.output_format, 'http')
        self.assertEqual(args.output_destination, 'http://example.com')
        self.assertEqual(args.http_username, 'user')
        self.assertEqual(args.http_password, 'pass')
        self.assertEqual(args.http_header, ['X-Custom: value'])


class TestBaseToolSubclass(BaseTool):
    """Test subclass of BaseTool for testing _output_as_text."""
    
    def _output_as_text(self, data):
        """Implementation of abstract method for testing."""
        return f"Text output: {data}"


class TestBaseToolOutput(unittest.TestCase):
    """Test cases for the base tool output functionality."""
    
    def test_output_as_text_not_implemented(self):
        """Test that _output_as_text raises NotImplementedError when not implemented."""
        tool = BaseTool("Test tool")
        with self.assertRaises(NotImplementedError):
            tool._output_as_text("test data")


if __name__ == '__main__':
    unittest.main()
