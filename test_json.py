#!/usr/bin/env python3
"""
Test script to verify JSON output.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatrooms_tool import get_all_chatrooms

def test_json():
    """Test JSON output."""
    try:
        # Test with no service name specified (should fall back to default behavior)
        result = get_all_chatrooms(
            api_url='http://localhost:9090/plugins/restapi/v1',
            auth_header='fred',
            insecure=False,
            service_name=None,
            room_type=None,
            search=None,
            include_occupants=True,
            output_format='json'
        )
        print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_json()
