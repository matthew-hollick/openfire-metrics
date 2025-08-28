"""
Test script for the system properties tool (read-only monitoring).
"""

import sys
import os

# Add the repository root (parent directory) to the path so we can import the openfire_api package
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from openfire_api.system_properties import SystemProperty, SystemProperties, SystemPropertiesAPI
from openfire_api.client import OpenFireAPIClient
from unittest.mock import Mock

def test_system_property():
    """Test SystemProperty class."""
    print("Testing SystemProperty class...")
    sys.stdout.flush()
    prop = SystemProperty("test.key", "test_value")
    assert prop.key == "test.key"
    assert prop.value == "test_value"
    print("SystemProperty class test passed.")
    sys.stdout.flush()


def test_system_properties():
    """Test SystemProperties class."""
    print("Testing SystemProperties class...")
    sys.stdout.flush()
    prop1 = SystemProperty("key1", "value1")
    prop2 = SystemProperty("key2", "value2")
    properties = SystemProperties([prop1, prop2])
    assert len(properties.properties) == 2
    assert properties.properties[0].key == "key1"
    assert properties.properties[1].value == "value2"
    print("SystemProperties class test passed.")
    sys.stdout.flush()


def test_system_properties_api():
    """Test SystemPropertiesAPI class methods signatures (read-only)."""
    print("Testing SystemPropertiesAPI method signatures (read-only)...")
    sys.stdout.flush()
    
    # Create a mock client
    client = Mock(spec=OpenFireAPIClient)
    api = SystemPropertiesAPI(client)
    
    # Check that read-only methods exist
    assert hasattr(api, 'get_system_properties')
    assert hasattr(api, 'get_system_property')
    
    # Check that write methods do NOT exist
    assert not hasattr(api, 'create_system_property')
    assert not hasattr(api, 'update_system_property')
    assert not hasattr(api, 'delete_system_property')
    
    print("SystemPropertiesAPI method signatures test passed.")
    sys.stdout.flush()


def main():
    """Run all tests."""
    print("Starting system properties tests (read-only)...")
    sys.stdout.flush()
    try:
        test_system_property()
        test_system_properties()
        test_system_properties_api()
        print("\nAll tests passed!")
        sys.stdout.flush()
        return 0
    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.stdout.flush()
        return 1


if __name__ == "__main__":
    result = main()
    sys.exit(result)
