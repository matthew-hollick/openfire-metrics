#!/usr/bin/env python3
"""
OpenFire Chatrooms Tool

A command-line tool for retrieving and displaying OpenFire chatroom information.
"""

import sys
#import os

#sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.chatrooms import ChatroomsAPI
from openfire_api.base_tool import BaseTool
from openfire_api.client import create_client


class ChatroomsTool(BaseTool):
    """Chatrooms tool implementation."""
    
    def __init__(self):
        """Initialize the chatrooms tool."""
        super().__init__('Retrieve chatroom information from OpenFire')
        self._add_chatrooms_arguments()
    
    def _add_chatrooms_arguments(self):
        """Add chatrooms-specific command-line arguments."""
        self.parser.add_argument('--service-name', help='The name of the MUC service')
        self.parser.add_argument('--room-type', choices=['all', 'public'], help='Room type filter')
        self.parser.add_argument('--search', help='Search/Filter by room name')
        # Occupants are now always included by default
        # This argument is kept for backward compatibility but has no effect
        self.parser.add_argument('--include-occupants', action='store_true',
                            help='Include occupants in output (always enabled)')
        self.parser.add_argument('--room-name', help='Name of a specific room to retrieve occupants')
    
    def run(self):
        """Run the chatrooms tool."""
        args = self.parse_args()
        
        # Create a client
        client = create_client(
            url=args.url,
            auth_header=args.auth_header,
            insecure=args.insecure
        )
        
        try:
            chatrooms_api = ChatroomsAPI(client)
            
            # If a specific room name is provided, get its occupants
            if args.room_name:
                # First get the room details
                # We need to get all chatrooms and find the specific one
                # This is a limitation of the OpenFire API - there's no direct endpoint to get a single room
                chatrooms = chatrooms_api.get_chatrooms()
                room_details = None
                for room in chatrooms.chat_rooms:
                    if room.room_name == args.room_name:
                        room_details = room
                        break
                
                # Then get the occupants
                occupants = chatrooms_api.get_room_occupants(args.room_name)
                
                # Convert to dictionary format for output
                if room_details:
                    occupants_data = {
                        'roomName': room_details.room_name,
                        'naturalName': room_details.natural_name,
                        'description': room_details.description,
                        'persistent': room_details.persistent,
                        'publicRoom': room_details.public_room,
                        'membersOnly': room_details.members_only,
                        'owners': room_details.owners,
                        'admins': room_details.admins,
                        'members': room_details.members,
                        'occupants': [
                            {
                                'jid': occupant.jid,
                                'userAddress': occupant.user_address,
                                'role': occupant.role,
                                'affiliation': occupant.affiliation
                            }
                            for occupant in occupants.occupants
                        ]
                    }
                else:
                    # Fallback if we can't find the room details
                    occupants_data = {
                        'roomName': args.room_name,
                        'occupants': [
                            {
                                'jid': occupant.jid,
                                'userAddress': occupant.user_address,
                                'role': occupant.role,
                                'affiliation': occupant.affiliation
                            }
                            for occupant in occupants.occupants
                        ]
                    }
                self.output_data(occupants_data)
            else:
                # Otherwise get all chatrooms
                # Convert to dictionary format for output
                chatrooms_data = {
                    'chatRooms': []
                }
                
                # If a specific service name is provided, use it
                if args.service_name:
                    services = [type('Service', (), {'service_name': args.service_name})()]
                    # Iterate over the specified service to get chatrooms
                    for service in services:
                        chatrooms = chatrooms_api.get_chatrooms(
                            service_name=service.service_name,
                            room_type=args.room_type,
                            search=args.search
                        )
                        
                        for room in chatrooms.chat_rooms:
                            room_data = {
                                'serviceName': service.service_name,
                                'roomName': room.room_name,
                                'naturalName': room.natural_name,
                                'description': room.description,
                                'subject': room.subject,
                                'creationDate': room.creation_date,
                                'modificationDate': room.modification_date,
                                'maxUsers': room.max_users,
                                'persistent': room.persistent,
                                'publicRoom': room.public_room,
                                'registrationEnabled': room.registration_enabled,
                                'canAnyoneDiscoverJID': room.can_anyone_discover_jid,
                                'canOccupantsChangeSubject': room.can_occupants_change_subject,
                                'canOccupantsInvite': room.can_occupants_invite,
                                'canChangeNickname': room.can_change_nickname,
                                'logEnabled': room.log_enabled,
                                'loginRestrictedToNickname': room.login_restricted_to_nickname,
                                'membersOnly': room.members_only,
                                'moderated': room.moderated,
                                'allowPM': room.allow_pm,
                                'owners': room.owners,
                                'admins': room.admins,
                                'members': room.members,
                                'occupants': []
                            }
                            
                            # Always get occupants for each room
                            try:
                                occupants = chatrooms_api.get_room_occupants(room.room_name)
                                room_data['occupants'] = [
                                    {
                                        'jid': occupant.jid,
                                        'userAddress': occupant.user_address,
                                        'role': occupant.role,
                                        'affiliation': occupant.affiliation
                                    }
                                    for occupant in occupants.occupants
                                ]
                            except Exception:
                                # If we can't get occupants for this room, continue with empty list
                                pass
                            
                            chatrooms_data['chatRooms'].append(room_data)
                else:
                    # Otherwise, get all chat services dynamically
                    chat_services = chatrooms_api.get_chat_services()
                    services = chat_services.services
                    
                    # If we have services, iterate over them
                    if services:
                        for service in services:
                            chatrooms = chatrooms_api.get_chatrooms(
                                service_name=service.service_name,
                                room_type=args.room_type,
                                search=args.search
                            )
                            
                            for room in chatrooms.chat_rooms:
                                room_data = {
                                    'serviceName': service.service_name,
                                    'roomName': room.room_name,
                                    'naturalName': room.natural_name,
                                    'description': room.description,
                                    'subject': room.subject,
                                    'creationDate': room.creation_date,
                                    'modificationDate': room.modification_date,
                                    'maxUsers': room.max_users,
                                    'persistent': room.persistent,
                                    'publicRoom': room.public_room,
                                    'registrationEnabled': room.registration_enabled,
                                    'canAnyoneDiscoverJID': room.can_anyone_discover_jid,
                                    'canOccupantsChangeSubject': room.can_occupants_change_subject,
                                    'canOccupantsInvite': room.can_occupants_invite,
                                    'canChangeNickname': room.can_change_nickname,
                                    'logEnabled': room.log_enabled,
                                    'loginRestrictedToNickname': room.login_restricted_to_nickname,
                                    'membersOnly': room.members_only,
                                    'moderated': room.moderated,
                                    'allowPM': room.allow_pm,
                                    'owners': room.owners,
                                    'admins': room.admins,
                                    'members': room.members,
                                    'occupants': []
                                }
                                
                                # Always get occupants for each room
                                try:
                                    occupants = chatrooms_api.get_room_occupants(room.room_name)
                                    room_data['occupants'] = [
                                        {
                                            'jid': occupant.jid,
                                            'userAddress': occupant.user_address,
                                            'role': occupant.role,
                                            'affiliation': occupant.affiliation
                                        }
                                        for occupant in occupants.occupants
                                    ]
                                except Exception:
                                    # If we can't get occupants for this room, continue with empty list
                                    pass
                                
                                chatrooms_data['chatRooms'].append(room_data)
                    else:
                        # If no services are returned, fall back to getting chatrooms without specifying service
                        # This handles the case where the API has a default service that isn't listed
                        chatrooms = chatrooms_api.get_chatrooms(
                            room_type=args.room_type,
                            search=args.search
                        )
                        
                        for room in chatrooms.chat_rooms:
                            room_data = {
                                'serviceName': 'default',
                                'roomName': room.room_name,
                                'naturalName': room.natural_name,
                                'description': room.description,
                                'subject': room.subject,
                                'creationDate': room.creation_date,
                                'modificationDate': room.modification_date,
                                'maxUsers': room.max_users,
                                'persistent': room.persistent,
                                'publicRoom': room.public_room,
                                'registrationEnabled': room.registration_enabled,
                                'canAnyoneDiscoverJID': room.can_anyone_discover_jid,
                                'canOccupantsChangeSubject': room.can_occupants_change_subject,
                                'canOccupantsInvite': room.can_occupants_invite,
                                'canChangeNickname': room.can_change_nickname,
                                'logEnabled': room.log_enabled,
                                'loginRestrictedToNickname': room.login_restricted_to_nickname,
                                'membersOnly': room.members_only,
                                'moderated': room.moderated,
                                'allowPM': room.allow_pm,
                                'owners': room.owners,
                                'admins': room.admins,
                                'members': room.members,
                                'occupants': []
                            }
                            
                            # Always get occupants for each room
                            try:
                                occupants = chatrooms_api.get_room_occupants(room.room_name)
                                room_data['occupants'] = [
                                    {
                                        'jid': occupant.jid,
                                        'userAddress': occupant.user_address,
                                        'role': occupant.role,
                                        'affiliation': occupant.affiliation
                                    }
                                    for occupant in occupants.occupants
                                ]
                            except Exception:
                                # If we can't get occupants for this room, continue with empty list
                                pass
                            
                            chatrooms_data['chatRooms'].append(room_data)
                self.output_data(chatrooms_data)
        
        finally:
            client.close()
    
    def _output_as_text(self, data):
        """Output data as text."""
        if 'chatRooms' in data:
            # All chatrooms format
            print(f"Found {len(data['chatRooms'])} chatrooms:")
            for room in data['chatRooms']:
                print(f"  {room['roomName']} ({room.get('naturalName', 'N/A')})")
                print(f"    Service: {room.get('serviceName', 'N/A')}")
                print(f"    Description: {room.get('description', 'N/A')}")
                print(f"    Persistent: {room.get('persistent', 'N/A')}")
                print(f"    Public: {room.get('publicRoom', 'N/A')}")
                print(f"    Members-only: {room.get('membersOnly', 'N/A')}")
                
                # Display owners
                owners = room.get('owners', [])
                if owners:
                    print(f"    Owners ({len(owners)}):")
                    for owner in owners:
                        print(f"      {owner}")
                else:
                    print("    Owners: None")
                
                # Display admins
                admins = room.get('admins', [])
                if admins:
                    print(f"    Admins ({len(admins)}):")
                    for admin in admins:
                        print(f"      {admin}")
                else:
                    print("    Admins: None")
                
                # Display members
                members = room.get('members', [])
                if members:
                    print(f"    Members ({len(members)}):")
                    for member in members:
                        print(f"      {member}")
                else:
                    print("    Members: None")
                
                # Display occupants if available
                occupants = room.get('occupants', [])
                if occupants:
                    print(f"    Occupants ({len(occupants)}):")
                    for occupant in occupants:
                        print(f"      jid: {occupant.get('jid', 'N/A')}")
                        print(f"      user: {occupant.get('userAddress', 'N/A')}")
                        print(f"      role: {occupant.get('role', 'N/A')}")
                        print(f"      affiliation: {occupant.get('affiliation', 'N/A')}")
                else:
                    print("    Occupants: None")
                
                print()
        else:
            # Single room format (with occupants)
            print(f"Room: {data['roomName']} ({data.get('naturalName', 'N/A')})")
            print(f"  Description: {data.get('description', 'N/A')}")
            print(f"  Persistent: {data.get('persistent', 'N/A')}")
            print(f"  Public: {data.get('publicRoom', 'N/A')}")
            print(f"  Members-only: {data.get('membersOnly', 'N/A')}")
            
            # Display owners
            owners = data.get('owners', [])
            if owners:
                print(f"  Owners ({len(owners)}):")
                for owner in owners:
                    print(f"    {owner}")
            else:
                print("  Owners: None")
            
            # Display admins
            admins = data.get('admins', [])
            if admins:
                print(f"  Admins ({len(admins)}):")
                for admin in admins:
                    print(f"    {admin}")
            else:
                print("  Admins: None")
            
            # Display members
            members = data.get('members', [])
            if members:
                print(f"  Members ({len(members)}):")
                for member in members:
                    print(f"    {member}")
            else:
                print("  Members: None")
            
            # Display occupants
            occupants = data.get('occupants', [])
            if occupants:
                print(f"  Occupants ({len(occupants)}):")
                for occupant in occupants:
                    print(f"    jid: {occupant.get('jid', 'N/A')}")
                    print(f"    user: {occupant.get('userAddress', 'N/A')}")
                    print(f"    role: {occupant.get('role', 'N/A')}")
                    print(f"    affiliation: {occupant.get('affiliation', 'N/A')}")
            else:
                print("  Occupants: None")

def main():
    """Main function for the chatrooms tool."""
    tool = ChatroomsTool()
    tool.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
