"""
Test the security audit log API module with the actual API response structure.
"""

import unittest
from unittest.mock import Mock
import sys
import os

# Add the openfire_api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'openfire_api'))

from openfire_api.security_audit_log import SecurityAuditLogs, SecurityAuditLogAPI


class TestSecurityAuditLogAPIWithActualResponse(unittest.TestCase):
    """Test the SecurityAuditLogAPI with the actual API response structure."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = SecurityAuditLogAPI(self.mock_client)
    
    def test_get_security_audit_logs_with_actual_response_structure(self):
        """Test get_security_audit_logs method with actual API response structure."""
        # Mock response with the actual structure we observed
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "logs": [
                {
                    "logId": 16,
                    "username": "admin",
                    "timestamp": 1755864103,
                    "summary": "created new MUC room thisisa3rdroom",
                    "node": "192.168.5.15",
                    "details": "subject = \nroomdesc = this is a 3rd room description\nroomname = this is a 3rd room name\nmaxusers = 30"
                },
                {
                    "logId": 15,
                    "username": "admin",
                    "timestamp": 1755862993,
                    "summary": "created new MUC room test2",
                    "node": "192.168.5.15",
                    "details": "subject = \nroomdesc = some text\nroomname = a second test room\nmaxusers = 30"
                },
                {
                    "logId": 14,
                    "username": "admin",
                    "timestamp": 1755860936,
                    "summary": "updated group membership for this is a test group",
                    "node": "192.168.5.15"
                }
            ]
        }
        
        self.mock_client.get.return_value = mock_response
        
        # Call the method
        logs = self.api.get_security_audit_logs(start_time=1755860936, end_time=0)
        
        # Verify the client was called with correct parameters
        self.mock_client.get.assert_called_once_with('logs/security', params={
            'offset': 0,
            'limit': 100,
            'startTime': 1755860936,
            'endTime': 0
        })
        
        # Verify the result
        self.assertIsInstance(logs, SecurityAuditLogs)
        self.assertEqual(len(logs.logs), 3)
        
        # Verify first log
        self.assertEqual(logs.logs[0].log_id, 16)
        self.assertEqual(logs.logs[0].username, "admin")
        self.assertEqual(logs.logs[0].timestamp, 1755864103)
        self.assertEqual(logs.logs[0].summary, "created new MUC room thisisa3rdroom")
        self.assertEqual(logs.logs[0].node, "192.168.5.15")
        self.assertIn("this is a 3rd room description", logs.logs[0].details)
        
        # Verify second log
        self.assertEqual(logs.logs[1].log_id, 15)
        self.assertEqual(logs.logs[1].username, "admin")
        self.assertEqual(logs.logs[1].timestamp, 1755862993)
        self.assertEqual(logs.logs[1].summary, "created new MUC room test2")
        self.assertEqual(logs.logs[1].node, "192.168.5.15")
        self.assertIn("a second test room", logs.logs[1].details)
        
        # Verify third log (missing details field)
        self.assertEqual(logs.logs[2].log_id, 14)
        self.assertEqual(logs.logs[2].username, "admin")
        self.assertEqual(logs.logs[2].timestamp, 1755860936)
        self.assertEqual(logs.logs[2].summary, "updated group membership for this is a test group")
        self.assertEqual(logs.logs[2].node, "192.168.5.15")
        self.assertEqual(logs.logs[2].details, "")  # Should default to empty string


if __name__ == '__main__':
    unittest.main()
