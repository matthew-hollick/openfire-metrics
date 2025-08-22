#!/usr/bin/env python3
"""
Test script for verifying chatrooms tool with dynamic service retrieval.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client
from openfire_api.chatrooms import ChatroomsAPI

def test_chat_services_retrieval():
    """Test that we can retrieve chat services dynamically."""
    # Create client (using default values for testing)
    client = create_client(
        url='http://localhost:9090/plugins/restapi/v1',
        auth_header='Bearer your-auth-token-here',
        insecure=True
    )
    
    try:
        chatrooms_api = ChatroomsAPI(client)
        
        # Test getting chat services
        print("Testing chat services retrieval...")
        chat_services = chatrooms_api.get_chat_services()
        
        print(f"Found {len(chat_services.services)} chat services:")
        for service in chat_services.services:
            print(f"  - {service.service_name}: {service.description}")
            
        # Test getting chatrooms for each service
        for service in chat_services.services:
            print(f"\nGetting chatrooms for service: {service.service_name}")
            chatrooms = chatrooms_api.get_chatrooms(service_name=service.service_name)
            print(f"  Found {len(chatrooms.chat_rooms)} chatrooms")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    test_chat_services_retrieval()
