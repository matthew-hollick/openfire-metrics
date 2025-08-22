"""
Tests for the OpenFire Security Audit Log Tool.
"""

import unittest
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from security_audit_log_tool import format_logs_as_json, format_logs_as_text


class TestSecurityAuditLogTool(unittest.TestCase):
    """Test cases for the security audit log tool functions."""
    
    def test_format_logs_as_json(self):
        """Test formatting logs as JSON."""
        logs_data = {
            'logs': [
                {
                    'logId': 1,
                    'username': 'admin',
                    'timestamp': 1234567890,
                    'summary': 'Test log',
                    'node': 'localhost',
                    'details': 'Test details'
                }
            ]
        }
        
        result = format_logs_as_json(logs_data)
        self.assertIn('"logId": 1', result)
        self.assertIn('"username": "admin"', result)
        self.assertIn('"summary": "Test log"', result)
    
    def test_format_logs_as_text_with_logs(self):
        """Test formatting logs as text with logs."""
        logs_data = {
            'logs': [
                {
                    'logId': 1,
                    'username': 'admin',
                    'timestamp': 1234567890,
                    'summary': 'Test log',
                    'node': 'localhost',
                    'details': 'Test details'
                }
            ]
        }
        
        result = format_logs_as_text(logs_data)
        self.assertIn('Security Audit Logs:', result)
        self.assertIn('ID: 1', result)
        self.assertIn('Username: admin', result)
        self.assertIn('Summary: Test log', result)
    
    def test_format_logs_as_text_no_logs(self):
        """Test formatting logs as text with no logs."""
        logs_data = {'logs': []}
        
        result = format_logs_as_text(logs_data)
        self.assertEqual(result, 'No security audit logs found.')


if __name__ == '__main__':
    unittest.main()
