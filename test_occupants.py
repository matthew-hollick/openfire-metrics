#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client
from openfire_api.chatrooms import ChatroomsAPI

# Create a client
client = create_client(
    url='http://localhost:9090/plugins/restapi/v1',
    auth_header='fred',
    insecure=False
)

try:
    # Create chatrooms API instance
    chatrooms_api = ChatroomsAPI(client)
    
    # Get all chat rooms
    chatrooms = chatrooms_api.get_chatrooms()
    print("Chat rooms:")
    for room in chatrooms.chat_rooms:
        print(f"  - {room.room_name}")
        
        # Get occupants for this room
        occupants = chatrooms_api.get_room_occupants(room.room_name)
        print(f"    Occupants ({len(occupants.occupants)}):")
        for occupant in occupants.occupants:
            print(f"      - {occupant.jid} (role: {occupant.role}, affiliation: {occupant.affiliation})")
            
finally:
    client.close()
