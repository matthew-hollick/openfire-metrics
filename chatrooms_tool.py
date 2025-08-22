#!/usr/bin/env python3
"""
OpenFire Chatrooms Tool

A command-line tool for retrieving and displaying OpenFire chatroom information.
"""

import argparse
import json
import sys
from typing import Dict, Any

from openfire_api.client import create_client
from openfire_api.chatrooms import ChatroomsAPI


def format_chatrooms_as_json(chatrooms_data: Dict[str, Any]) -> str:
    """Format chatrooms data as JSON."""
    return json.dumps(chatrooms_data, indent=2)


def format_chatrooms_as_text(chatrooms_data: Dict[str, Any], include_occupants: bool = False) -> str:
    """Format chatrooms data as text.
    
    Args:
        chatrooms_data: Dictionary containing chatrooms data
        include_occupants: Whether occupants data should have been included
    
    Returns:
        Formatted text string
    """
    if 'chatRooms' in chatrooms_data:
        # All chatrooms format
        output = f"Found {len(chatrooms_data['chatRooms'])} chatrooms:\n"
        for room in chatrooms_data['chatRooms']:
            output += f"  {room['roomName']} ({room.get('naturalName', 'N/A')})\n"
            output += f"    Service: {room.get('serviceName', 'N/A')}\n"
            output += f"    Description: {room.get('description', 'N/A')}\n"
            output += f"    Persistent: {room.get('persistent', 'N/A')}\n"
            output += f"    Public: {room.get('publicRoom', 'N/A')}\n"
            output += f"    Members-only: {room.get('membersOnly', 'N/A')}\n"
            
            # Display owners
            owners = room.get('owners', [])
            if owners:
                output += f"    Owners ({len(owners)}):\n"
                for owner in owners:
                    output += f"      {owner}\n"
            else:
                output += "    Owners: None\n"
            
            # Display admins
            admins = room.get('admins', [])
            if admins:
                output += f"    Admins ({len(admins)}):\n"
                for admin in admins:
                    output += f"      {admin}\n"
            else:
                output += "    Admins: None\n"
            
            # Display members
            members = room.get('members', [])
            if members:
                output += f"    Members ({len(members)}):\n"
                for member in members:
                    output += f"      {member}\n"
            else:
                output += "    Members: None\n"
            
            # Display occupants if available
            occupants = room.get('occupants', [])
            if occupants:
                output += f"    Occupants ({len(occupants)}):\n"
                for occupant in occupants:
                    output += f"      jid: {occupant.get('jid', 'N/A')}\n"
                    output += f"      user: {occupant.get('userAddress', 'N/A')}\n"
                    output += f"      role: {occupant.get('role', 'N/A')}\n"
                    output += f"      affiliation: {occupant.get('affiliation', 'N/A')}\n"
            else:
                output += "    Occupants: None\n"
            
            output += "\n"
        return output
    else:
        # Single room format (with occupants)
        output = f"Room: {chatrooms_data['roomName']} ({chatrooms_data.get('naturalName', 'N/A')})\n"
        output += f"  Description: {chatrooms_data.get('description', 'N/A')}\n"
        output += f"  Persistent: {chatrooms_data.get('persistent', 'N/A')}\n"
        output += f"  Public: {chatrooms_data.get('publicRoom', 'N/A')}\n"
        output += f"  Members-only: {chatrooms_data.get('membersOnly', 'N/A')}\n"
        
        # Display owners
        owners = chatrooms_data.get('owners', [])
        if owners:
            output += f"  Owners ({len(owners)}):\n"
            for owner in owners:
                output += f"    {owner}\n"
        else:
            output += "  Owners: None\n"
        
        # Display admins
        admins = chatrooms_data.get('admins', [])
        if admins:
            output += f"  Admins ({len(admins)}):\n"
            for admin in admins:
                output += f"    {admin}\n"
        else:
            output += "  Admins: None\n"
        
        # Display members
        members = chatrooms_data.get('members', [])
        if members:
            output += f"  Members ({len(members)}):\n"
            for member in members:
                output += f"    {member}\n"
        else:
            output += "  Members: None\n"
        
        # Display occupants
        occupants = chatrooms_data.get('occupants', [])
        if occupants:
            output += f"  Occupants ({len(occupants)}):\n"
            for occupant in occupants:
                output += f"    jid: {occupant.get('jid', 'N/A')}\n"
                output += f"    user: {occupant.get('userAddress', 'N/A')}\n"
                output += f"    role: {occupant.get('role', 'N/A')}\n"
                output += f"    affiliation: {occupant.get('affiliation', 'N/A')}\n"
        else:
            output += "  Occupants: None\n"
        
        return output


def get_all_chatrooms(api_url: str, auth_header: str, insecure: bool,
                     service_name: str = None, room_type: str = None, 
                     search: str = None, include_occupants: bool = False,
                     output_format: str = 'json') -> str:
    """Get all chatrooms and format the output."""
    # Create client
    client = create_client(
        url=api_url,
        auth_header=auth_header,
        insecure=insecure
    )
    
    try:
        chatrooms_api = ChatroomsAPI(client)
        
        # Convert to dictionary format for output
        chatrooms_data = {
            'chatRooms': []
        }
        
        # If a specific service name is provided, use it
        if service_name:
            services = [type('Service', (), {'service_name': service_name})()]
            # Iterate over the specified service to get chatrooms
            for service in services:
                chatrooms = chatrooms_api.get_chatrooms(
                    service_name=service.service_name,
                    room_type=room_type,
                    search=search
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
                    
                    # If requested, get occupants for each room
                    if include_occupants:
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
                        room_type=room_type,
                        search=search
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
                        
                        # If requested, get occupants for each room
                        if include_occupants:
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
                    room_type=room_type,
                    search=search
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
                    
                    # If requested, get occupants for each room
                    if include_occupants:
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
        
        if output_format == 'json':
            return format_chatrooms_as_json(chatrooms_data)
        else:
            return format_chatrooms_as_text(chatrooms_data, include_occupants)
            
    except Exception as e:
        raise Exception(f"Failed to retrieve chatrooms: {e}")
    finally:
        client.close()


def get_room_occupants(api_url: str, auth_header: str, insecure: bool,
                       room_name: str, output_format: str = 'json') -> str:
    """Get occupants for a specific room and format the output."""
    # Create client
    client = create_client(
        url=api_url,
        auth_header=auth_header,
        insecure=insecure
    )
    
    try:
        chatrooms_api = ChatroomsAPI(client)
        
        # First get the room details
        # We need to get all chatrooms and find the specific one
        # This is a limitation of the OpenFire API - there's no direct endpoint to get a single room
        chatrooms = chatrooms_api.get_chatrooms()
        room_details = None
        for room in chatrooms.chat_rooms:
            if room.room_name == room_name:
                room_details = room
                break
        
        # Then get the occupants
        occupants = chatrooms_api.get_room_occupants(room_name)
        
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
                'roomName': room_name,
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
        
        if output_format == 'json':
            return format_chatrooms_as_json(occupants_data)
        else:
            return format_chatrooms_as_text(occupants_data)
            
    except Exception as e:
        raise Exception(f"Failed to retrieve occupants for room '{room_name}': {e}")
    finally:
        client.close()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Retrieve and manage OpenFire chatroom information.')
    parser.add_argument('--api-url', default='http://localhost:9090/plugins/restapi/v1',
                        help='OpenFire REST API URL')
    parser.add_argument('--username', help='Username for basic authentication')
    parser.add_argument('--password', help='Password for basic authentication')
    parser.add_argument('--auth-header', help='Authorization header value')
    parser.add_argument('--insecure', action='store_true',
                        help='Skip SSL certificate validation')
    parser.add_argument('--output-format', choices=['json', 'text'], default='json',
                        help='Output format (json or text)')
    
    # Chatrooms specific arguments
    parser.add_argument('--service-name', help='The name of the MUC service')
    parser.add_argument('--room-type', choices=['all', 'public'], help='Room type filter')
    parser.add_argument('--search', help='Search/Filter by room name')
    # Occupants are now always included by default
    # This argument is kept for backward compatibility but has no effect
    parser.add_argument('--include-occupants', action='store_true',
                        help=argparse.SUPPRESS)
    parser.add_argument('--room-name', help='Name of a specific room to retrieve occupants')
    
    args = parser.parse_args()
    
    # Determine authentication
    auth_header = args.auth_header
    if not auth_header and args.username and args.password:
        import base64
        credentials = f"{args.username}:{args.password}"
        auth_header = "Basic " + base64.b64encode(credentials.encode()).decode()
    
    if not auth_header:
        print("Error: Either --auth-header or both --username and --password must be provided", file=sys.stderr)
        return 1
    
    try:
        # If a specific room name is provided, get its occupants
        if args.room_name:
            result = get_room_occupants(
                api_url=args.api_url,
                auth_header=auth_header,
                insecure=args.insecure,
                room_name=args.room_name,
                output_format=args.output_format
            )
            print(result)
        else:
            # Otherwise get all chatrooms
            result = get_all_chatrooms(
                api_url=args.api_url,
                auth_header=auth_header,
                insecure=args.insecure,
                service_name=args.service_name,
                room_type=args.room_type,
                search=args.search,
                include_occupants=True,
                output_format=args.output_format
            )
            print(result)
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
