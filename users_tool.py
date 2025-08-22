#!/usr/bin/env python3
"""
OpenFire Users Tool

A standalone tool for retrieving user information from OpenFire.
"""

import json
import sys
import os
import argparse

# Add the parent directory to the path so we can import the openfire_api module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client
from openfire_api.users import UsersAPI
from openfire_api.sessions import SessionsAPI
from openfire_api.chatrooms import ChatroomsAPI
from openfire_api.message_archive import MessageArchiveAPI


def main():
    """Main function for the users tool."""
    parser = argparse.ArgumentParser(description='Retrieve user information from OpenFire')
    parser.add_argument('--url', default='http://localhost:9090/plugins/restapi/v1',
                        help='OpenFire REST API URL')
    parser.add_argument('--auth-header', required=True,
                        help='Authorization header value')
    parser.add_argument('--insecure', action='store_true',
                        help='Skip SSL certificate validation')
    parser.add_argument('--username',
                        help='Retrieve specific user by username')
    parser.add_argument('--search',
                        help='Search/Filter by username')
    parser.add_argument('--property-key',
                        help='Filter by a user property name')
    parser.add_argument('--property-value',
                        help='Filter by user property value')
    parser.add_argument('--output-format', choices=['json', 'text'], default='json',
                        help='Output format')
    
    args = parser.parse_args()
    
    # Create a client
    client = create_client(
        url=args.url,
        auth_header=args.auth_header,
        insecure=args.insecure
    )
    
    # Create users API instance
    users_api = UsersAPI(client)
    
    # Create sessions API instance
    sessions_api = SessionsAPI(client)
    
    # Create chatrooms API instance
    chatrooms_api = ChatroomsAPI(client)
    
    # Create message archive API instance
    message_archive_api = MessageArchiveAPI(client)
    
    # Get all sessions to determine login status and local user status
    try:
        sessions = sessions_api.get_sessions()
        # Create a set of logged in usernames for quick lookup
        logged_in_users = {session.username for session in sessions.sessions}
        # Create a dictionary mapping usernames to their local status
        local_user_status = {}
        for session in sessions.sessions:
            # If node is "Local", mark user as local
            # For remote users, node would have a different value
            is_local = session.node == "Local" if session.node else True
            local_user_status[session.username] = is_local
    except Exception as e:
        print(f"Warning: Could not retrieve sessions: {e}", file=sys.stderr)
        logged_in_users = set()
        local_user_status = {}
    
    # Get all chat rooms and their occupants
    try:
        chatrooms = chatrooms_api.get_chatrooms()
        # Create a dictionary mapping usernames to the rooms they're in
        user_rooms = {}
        for room in chatrooms.chat_rooms:
            try:
                occupants = chatrooms_api.get_room_occupants(room.room_name)
                for occupant in occupants.occupants:
                    # Extract username from JID (room@conference.domain/username)
                    if '/' in occupant.jid:
                        username = occupant.jid.split('/')[-1]
                        if username not in user_rooms:
                            user_rooms[username] = []
                        user_rooms[username].append(room.room_name)
            except Exception as e:
                print(f"Warning: Could not retrieve occupants for room {room.room_name}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Warning: Could not retrieve chatrooms: {e}", file=sys.stderr)
        user_rooms = {}
    
    try:
        if args.username:
            # Get specific user
            user = users_api.get_user(args.username)
            if args.output_format == 'json':
                # Get unread message count for the user
                unread_count = 0
                try:
                    # Use the username as JID for now - in a real implementation, 
                    # you might need the full JID including domain
                    jid = f"{user.username}@localhost"  # Adjust domain as needed
                    unread_count = message_archive_api.get_unread_message_count(jid)
                except Exception as e:
                    print(f"Warning: Could not retrieve unread message count for {user.username}: {e}", file=sys.stderr)
                
                user_data = {
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'logged_on': user.username in logged_in_users,
                    'local_user': local_user_status.get(user.username, True),
                    'unread_messages': unread_count,
                    'rooms': user_rooms.get(user.username, []),
                    'properties': [{'key': p.key, 'value': p.value} for p in user.properties]
                }
                print(json.dumps(user_data, indent=2))
            else:
                logged_on_status = " (logged on)" if user.username in logged_in_users else " (not logged on)"
                local_status = " (local)" if local_user_status.get(user.username, True) else " (remote)"
                
                # Get unread message count for the user
                unread_count = 0
                try:
                    # Use the username as JID for now - in a real implementation, 
                    # you might need the full JID including domain
                    jid = f"{user.username}@localhost"  # Adjust domain as needed
                    unread_count = message_archive_api.get_unread_message_count(jid)
                except Exception as e:
                    print(f"Warning: Could not retrieve unread message count for {user.username}: {e}", file=sys.stderr)
                
                print(f"Username: {user.username}{logged_on_status}{local_status}")
                print(f"Name: {user.name}")
                print(f"Email: {user.email}")
                print(f"Unread messages: {unread_count}")
                # Display rooms user is in
                rooms = user_rooms.get(user.username, [])
                if rooms:
                    print(f"Rooms: {', '.join(rooms)}")
                else:
                    print("Rooms: None")
                if user.properties:
                    print("Properties:")
                    for prop in user.properties:
                        print(f"  {prop.key}: {prop.value}")
        else:
            # Get all users
            users = users_api.get_users(
                search=args.search,
                property_key=args.property_key,
                property_value=args.property_value
            )
            
            if args.output_format == 'json':
                users_data = []
                for user in users.users:
                    # Get unread message count for the user
                    unread_count = 0
                    try:
                        # Use the username as JID for now - in a real implementation, 
                        # you might need the full JID including domain
                        jid = f"{user.username}@localhost"  # Adjust domain as needed
                        unread_count = message_archive_api.get_unread_message_count(jid)
                    except Exception as e:
                        print(f"Warning: Could not retrieve unread message count for {user.username}: {e}", file=sys.stderr)
                    
                    user_data = {
                        'username': user.username,
                        'name': user.name,
                        'email': user.email,
                        'logged_on': user.username in logged_in_users,
                        'local_user': local_user_status.get(user.username, True),
                        'unread_messages': unread_count,
                        'rooms': user_rooms.get(user.username, []),
                        'properties': [{'key': p.key, 'value': p.value} for p in user.properties]
                    }
                    users_data.append(user_data)
                print(json.dumps({'users': users_data}, indent=2))
            else:
                print(f"Found {len(users.users)} users:")
                for user in users.users:
                    logged_on_status = " (logged on)" if user.username in logged_in_users else ""
                    local_status = " (local)" if local_user_status.get(user.username, True) else " (remote)"
                    
                    # Get unread message count for the user
                    unread_count = 0
                    try:
                        # Use the username as JID for now - in a real implementation, 
                        # you might need the full JID including domain
                        jid = f"{user.username}@localhost"  # Adjust domain as needed
                        unread_count = message_archive_api.get_unread_message_count(jid)
                    except Exception as e:
                        print(f"Warning: Could not retrieve unread message count for {user.username}: {e}", file=sys.stderr)
                    
                    rooms = user_rooms.get(user.username, [])
                    rooms_info = f" (Rooms: {', '.join(rooms)})" if rooms else ""
                    print(f"  {user.username}: {user.name} ({user.email}){logged_on_status}{local_status} (Unread: {unread_count}){rooms_info}")
                    if user.properties:
                        print(f"    Properties: {len(user.properties)}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    finally:
        client.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
