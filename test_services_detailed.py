#!/usr/bin/env python3
"""
Detailed test script to understand chat services and rooms.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client
from openfire_api.chatrooms import ChatroomsAPI

def test_detailed():
    """Detailed test of services and rooms."""
    # Create client with the same parameters as the user used
    client = create_client(
        url='http://localhost:9090/plugins/restapi/v1',
        auth_header='fred',
        insecure=False
    )
    
    try:
        chatrooms_api = ChatroomsAPI(client)
        
        # Try to get chat services first
        print("=== Chat Services ===")
        try:
            chat_services = chatrooms_api.get_chat_services()
            print(f"Number of services: {len(chat_services.services)}")
            for service in chat_services.services:
                print(f"  Service: {service.service_name}")
        except Exception as e:
            print(f"Failed to get chat services: {e}")
            
        # Try to get chatrooms without specifying service
        print("\n=== Chatrooms (no service specified) ===")
        try:
            chatrooms = chatrooms_api.get_chatrooms()
            print(f"Number of rooms: {len(chatrooms.chat_rooms)}")
            for room in chatrooms.chat_rooms:
                print(f"  Room: {room.room_name}")
        except Exception as e:
            print(f"Failed to get chatrooms: {e}")
            
        # Try with common service names
        common_services = ['conference', 'muc']
        for service_name in common_services:
            print(f"\n=== Chatrooms (service: {service_name}) ===")
            try:
                chatrooms = chatrooms_api.get_chatrooms(service_name=service_name)
                print(f"Number of rooms: {len(chatrooms.chat_rooms)}")
                for room in chatrooms.chat_rooms:
                    print(f"  Room: {room.room_name}")
            except Exception as e:
                print(f"Failed to get chatrooms for {service_name}: {e}")
                
    except Exception as e:
        print(f"General error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == "__main__":
    test_detailed()
