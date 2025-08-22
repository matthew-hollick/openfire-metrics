#!/usr/bin/env python3
"""
Test script for the OpenFire chatrooms tool.
"""

import sys
import os

# Add the parent directory to the path so we can import the openfire_api package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from openfire_api.client import create_client
from openfire_api.chatrooms import ChatroomsAPI


def test_chatrooms_api():
    """Test the chatrooms API functionality."""
    # Create client
    client = create_client(
        url='http://localhost:9090/plugins/restapi/v1',
        auth_header='fred',
        insecure=True
    )
    
    try:
        # Initialize the chatrooms API
        chatrooms_api = ChatroomsAPI(client)
        
        # Test getting all chatrooms
        print("Getting all chatrooms...")
        chatrooms = chatrooms_api.get_chatrooms()
        print(f"Found {len(chatrooms.chat_rooms)} chatrooms:")
        for room in chatrooms.chat_rooms:
            print(f"  - {room.room_name} ({room.natural_name}): {room.description}")
            print(f"    Persistent: {room.persistent}, Public: {room.public_room}")
            
            # Display owners, admins, and members
            if room.owners:
                print(f"    Owners ({len(room.owners)}): {', '.join(room.owners)}")
            else:
                print("    Owners: None")
            
            if room.admins:
                print(f"    Admins ({len(room.admins)}): {', '.join(room.admins)}")
            else:
                print("    Admins: None")
            
            if room.members:
                print(f"    Members ({len(room.members)}): {', '.join(room.members)}")
            else:
                print("    Members: None")
        
        # If there are chatrooms, test getting occupants for the first one
        if chatrooms.chat_rooms:
            first_room_name = chatrooms.chat_rooms[0].room_name
            print(f"\nGetting occupants for room '{first_room_name}'...")
            occupants = chatrooms_api.get_room_occupants(first_room_name)
            print(f"Found {len(occupants.occupants)} occupants:")
            for occupant in occupants.occupants:
                print(f"  - {occupant.jid} ({occupant.role}, {occupant.affiliation})")
        
        print("\nAll tests passed!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    finally:
        client.close()
    
    return 0


def main():
    """Main function."""
    return test_chatrooms_api()


if __name__ == "__main__":
    sys.exit(main())
