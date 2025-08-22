"""
Tests for the OpenFire Security Audit Log API module.
"""

import unittest
from unittest.mock import Mock
import sys
import os

# Add the openfire_api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'openfire_api'))

from openfire_api.security_audit_log import SecurityAuditLog, SecurityAuditLogs, SecurityAuditLogAPI


class TestSecurityAuditLog(unittest.TestCase):
    """Test cases for the SecurityAuditLog class."""
    
    def test_init(self):
        """Test SecurityAuditLog initialization."""
        log = SecurityAuditLog(
            log_id=1,
            username="admin",
            timestamp=1234567890,
            summary="Test log",
            node="localhost",
            details="Test details"
        )
        
        self.assertEqual(log.log_id, 1)
        self.assertEqual(log.username, "admin")
        self.assertEqual(log.timestamp, 1234567890)
        self.assertEqual(log.summary, "Test log")
        self.assertEqual(log.node, "localhost")
        self.assertEqual(log.details, "Test details")


class TestSecurityAuditLogs(unittest.TestCase):
    """Test cases for the SecurityAuditLogs class."""
    
    def test_init(self):
        """Test SecurityAuditLogs initialization."""
        log1 = SecurityAuditLog(1, "admin", 1234567890, "Test log 1", "localhost", "Details 1")
        log2 = SecurityAuditLog(2, "user", 1234567891, "Test log 2", "localhost", "Details 2")
        
        logs_collection = SecurityAuditLogs([log1, log2])
        
        self.assertEqual(len(logs_collection.logs), 2)
        self.assertEqual(logs_collection.logs[0].log_id, 1)
        self.assertEqual(logs_collection.logs[1].log_id, 2)


class TestSecurityAuditLogAPI(unittest.TestCase):
    """Test cases for the SecurityAuditLogAPI class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = SecurityAuditLogAPI(self.mock_client)
    
    def test_init(self):
        """Test SecurityAuditLogAPI initialization."""
        self.assertEqual(self.api.client, self.mock_client)
    
    def test_get_security_audit_logs(self):
        """Test get_security_audit_logs method."""
        # Mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
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
        
        self.mock_client.get.return_value = mock_response
        
        # Call the method
        logs = self.api.get_security_audit_logs(start_time=1234567000, end_time=0)
        
        # Verify the client was called with correct parameters
        self.mock_client.get.assert_called_once_with('logs/security', params={
            'offset': 0,
            'limit': 100,
            'startTime': 1234567000,
            'endTime': 0
        })
        
        # Verify the result
        self.assertIsInstance(logs, SecurityAuditLogs)
        self.assertEqual(len(logs.logs), 1)
        self.assertEqual(logs.logs[0].log_id, 1)
        self.assertEqual(logs.logs[0].username, 'admin')
    
    def test_get_security_audit_logs_with_username(self):
        """Test get_security_audit_logs method with username filter."""
        # Mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'logs': []}
        
        self.mock_client.get.return_value = mock_response
        
        # Call the method
        self.api.get_security_audit_logs(username='admin', start_time=1234567000, end_time=0)
        
        # Verify the client was called with correct parameters
        self.mock_client.get.assert_called_once_with('logs/security', params={
            'offset': 0,
            'limit': 100,
            'username': 'admin',
            'startTime': 1234567000,
            'endTime': 0
        })


if __name__ == '__main__':
    # Run the tests
    unittest.main()
