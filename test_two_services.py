#!/usr/bin/env python3
"""
Test script to verify handling of multiple chat services.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client
from openfire_api.chatrooms import ChatroomsAPI

def test_two_services():
    """Test handling of two chat services with rooms."""
    # Create client with the same parameters as the user used
    client = create_client(
        url='http://localhost:9090/plugins/restapi/v1',
        auth_header='fred',
        insecure=False
    )
    
    try:
        chatrooms_api = ChatroomsAPI(client)
        
        # Try to get chat services first
        print("Attempting to get chat services...")
        try:
            chat_services = chatrooms_api.get_chat_services()
            print(f"Successfully retrieved {len(chat_services.services)} chat services")
            for service in chat_services.services:
                print(f"  Service: {service.service_name}")
                
                # Get chatrooms for this service
                chatrooms = chatrooms_api.get_chatrooms(service_name=service.service_name)
                print(f"    Rooms in service: {len(chatrooms.chat_rooms)}")
                for room in chatrooms.chat_rooms:
                    print(f"      Room: {room.room_name}")
        except Exception as e:
            print(f"Failed to get chat services: {e}")
            
    except Exception as e:
        print(f"General error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    test_two_services()
