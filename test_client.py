"""
Test script for the OpenFire API client.
"""

import json
import sys
import os

# Add the parent directory to the path so we can import the openfire_api module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client


def main():
    """Test the OpenFire API client."""
    # Create a client
    client = create_client(
        url="http://localhost:9090/plugins/restapi/v1",
        auth_header="fred",
        insecure=True
    )
    
    # Test a simple GET request
    try:
        response = client.get("sessions")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return 1
    
    finally:
        client.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
