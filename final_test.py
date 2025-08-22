#!/usr/bin/env python3
"""
Final test to verify both text and JSON output formats.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatrooms_tool import get_all_chatrooms

def test_outputs():
    """Test both text and JSON output formats."""
    try:
        print("=== Testing JSON Output ===")
        result_json = get_all_chatrooms(
            api_url='http://localhost:9090/plugins/restapi/v1',
            auth_header='fred',
            insecure=False,
            service_name=None,
            room_type=None,
            search=None,
            include_occupants=True,
            output_format='json'
        )
        print(result_json)
        
        print("\n=== Testing Text Output ===")
        result_text = get_all_chatrooms(
            api_url='http://localhost:9090/plugins/restapi/v1',
            auth_header='fred',
            insecure=False,
            service_name=None,
            room_type=None,
            search=None,
            include_occupants=True,
            output_format='text'
        )
        print(result_text)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_outputs()
