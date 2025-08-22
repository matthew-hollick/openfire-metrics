"""
Test script for the OpenFire API client with chatrooms endpoint.
"""

import json
import sys
import os

# Add the parent directory to the path so we can import the openfire_api module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client


def main():
    """Test the OpenFire API client with chatrooms endpoint."""
    # Create a client
    client = create_client(
        url="http://localhost:9090/plugins/restapi/v1",
        auth_header="fred",
        insecure=True
    )
    
    # Test a GET request with query parameters
    try:
        params = {
            'servicename': 'conference',
            'type': 'all',
            'expandGroups': 'true'
        }
        response = client.get("chatrooms", params=params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Chatrooms JSON:")
            print(json.dumps(data, indent=2))
            
            # If there are chatrooms, test getting occupants for the first one
            if data.get('chatRooms'):
                room_name = data['chatRooms'][0]['roomName']
                print(f"\nGetting occupants for room '{room_name}'...")
                occupants_response = client.get(f"chatrooms/{room_name}/occupants")
                print(f"Occupants Status Code: {occupants_response.status_code}")
                
                if occupants_response.status_code == 200:
                    occupants_data = occupants_response.json()
                    print("Occupants JSON:")
                    print(json.dumps(occupants_data, indent=2))
                else:
                    print(f"Error getting occupants: {occupants_response.status_code} - {occupants_response.text}")
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
