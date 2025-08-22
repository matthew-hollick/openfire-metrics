"""
Test cases for the OpenFire system properties API.
"""

import unittest
from unittest.mock import Mock
import sys
import os

# Add the parent directory to the path so we can import the openfire_api package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from openfire_api.system_properties import SystemProperty, SystemProperties, SystemPropertiesAPI


class TestSystemProperty(unittest.TestCase):
    """Test cases for the SystemProperty class."""
    
    def test_system_property_creation(self):
        """Test creating a SystemProperty instance."""
        prop = SystemProperty("test.key", "test_value")
        self.assertEqual(prop.key, "test.key")
        self.assertEqual(prop.value, "test_value")


class TestSystemProperties(unittest.TestCase):
    """Test cases for the SystemProperties class."""
    
    def test_system_properties_creation(self):
        """Test creating a SystemProperties instance."""
        prop1 = SystemProperty("key1", "value1")
        prop2 = SystemProperty("key2", "value2")
        properties = SystemProperties([prop1, prop2])
        self.assertEqual(len(properties.properties), 2)
        self.assertEqual(properties.properties[0].key, "key1")
        self.assertEqual(properties.properties[1].value, "value2")


class TestSystemPropertiesAPI(unittest.TestCase):
    """Test cases for the SystemPropertiesAPI class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = SystemPropertiesAPI(self.mock_client)
    
    def test_get_system_properties(self):
        """Test getting all system properties."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "properties": [
                {"key": "key1", "value": "value1"},
                {"key": "key2", "value": "value2"}
            ]
        }
        mock_response.raise_for_status.return_value = None
        self.mock_client.get.return_value = mock_response
        
        # Call the method
        result = self.api.get_system_properties()
        
        # Verify the result
        self.assertEqual(len(result.properties), 2)
        self.assertEqual(result.properties[0].key, "key1")
        self.assertEqual(result.properties[0].value, "value1")
        self.assertEqual(result.properties[1].key, "key2")
        self.assertEqual(result.properties[1].value, "value2")
        
        # Verify the client was called correctly
        self.mock_client.get.assert_called_once_with('system/properties')
    
    def test_get_system_property(self):
        """Test getting a specific system property."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {"key": "test.key", "value": "test_value"}
        mock_response.raise_for_status.return_value = None
        self.mock_client.get.return_value = mock_response
        
        # Call the method
        result = self.api.get_system_property("test.key")
        
        # Verify the result
        self.assertEqual(result.key, "test.key")
        self.assertEqual(result.value, "test_value")
        
        # Verify the client was called correctly
        self.mock_client.get.assert_called_once_with('system/properties/test.key')
    
    def test_create_system_property(self):
        """Test creating a system property."""
        # Mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        self.mock_client.post.return_value = mock_response
        
        # Create a property
        prop = SystemProperty("new.key", "new_value")
        
        # Call the method
        self.api.create_system_property(prop)
        
        # Verify the client was called correctly
        self.mock_client.post.assert_called_once()
        call_args = self.mock_client.post.call_args
        self.assertEqual(call_args[0][0], 'system/properties')
        self.assertIn('headers', call_args[1])
        self.assertEqual(call_args[1]['headers']['Content-Type'], 'application/xml')
    
    def test_update_system_property(self):
        """Test updating a system property."""
        # Mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        self.mock_client.put.return_value = mock_response
        
        # Create a property
        prop = SystemProperty("existing.key", "updated_value")
        
        # Call the method
        self.api.update_system_property("existing.key", prop)
        
        # Verify the client was called correctly
        self.mock_client.put.assert_called_once()
        call_args = self.mock_client.put.call_args
        self.assertEqual(call_args[0][0], 'system/properties/existing.key')
        self.assertIn('headers', call_args[1])
        self.assertEqual(call_args[1]['headers']['Content-Type'], 'application/xml')
    
    def test_delete_system_property(self):
        """Test deleting a system property."""
        # Mock response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        self.mock_client.delete.return_value = mock_response
        
        # Call the method
        self.api.delete_system_property("delete.key")
        
        # Verify the client was called correctly
        self.mock_client.delete.assert_called_once_with('system/properties/delete.key')


if __name__ == '__main__':
    unittest.main()
