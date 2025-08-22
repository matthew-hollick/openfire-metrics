#!/usr/bin/env python3
"""
Debug script for chatrooms tool to see what's happening.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client
from openfire_api.chatrooms import ChatroomsAPI

def debug_chatrooms():
    """Debug chatrooms retrieval."""
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
        except Exception as e:
            print(f"Failed to get chat services: {e}")
            
        # Try to get chatrooms without specifying a service
        print("\nAttempting to get chatrooms without specifying service...")
        try:
            chatrooms = chatrooms_api.get_chatrooms()
            print(f"Successfully retrieved {len(chatrooms.chat_rooms)} chatrooms")
        except Exception as e:
            print(f"Failed to get chatrooms: {e}")
            
    except Exception as e:
        print(f"General error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    debug_chatrooms()
