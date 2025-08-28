#!/usr/bin/env python3
"""
OpenFire Users Tool

A standalone tool for retrieving user information from OpenFire.
"""

import sys
#import os

#sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.users import UsersAPI
from openfire_api.sessions import SessionsAPI
from openfire_api.chatrooms import ChatroomsAPI
from openfire_api.base_tool import BaseTool
from openfire_api.client import create_client


class UsersTool(BaseTool):
    """Users tool implementation."""
    
    def __init__(self):
        """Initialize the users tool."""
        super().__init__('Retrieve user information from OpenFire')
        self._add_users_arguments()
    
    def _add_users_arguments(self):
        """Add users-specific command-line arguments."""
        self.parser.add_argument('--username',
                            help='Retrieve specific user by username')
        self.parser.add_argument('--search',
                            help='Search/Filter by username')
        self.parser.add_argument('--property-key',
                            help='Filter by a user property name')
        self.parser.add_argument('--property-value',
                            help='Filter by user property value')
    
    def run(self):
        """Run the users tool."""
        args = self.parse_args()
        
        # Create a client with auth from auth_utils
        client = create_client(
            url=args.url,
            auth_header=args.auth_header,
            insecure=args.insecure
        )
        
        try:
            # Create users API instance
            users_api = UsersAPI(client)
            
            # Create sessions API instance
            sessions_api = SessionsAPI(client)
            
            # Create chatrooms API instance
            chatrooms_api = ChatroomsAPI(client)
            
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
            
            if args.username:
                # Get specific user
                user = users_api.get_user(args.username)
                user_data = {
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'logged_on': user.username in logged_in_users,
                    'local_user': local_user_status.get(user.username, True),
                    'rooms': user_rooms.get(user.username, []),
                    'properties': [{'key': p.key, 'value': p.value} for p in user.properties]
                }
                self.output_data(user_data)
            else:
                # Get all users
                users = users_api.get_users(
                    search=args.search,
                    property_key=args.property_key,
                    property_value=args.property_value
                )
                
                users_data = []
                for user in users.users:
                    user_data = {
                        'username': user.username,
                        'name': user.name,
                        'email': user.email,
                        'logged_on': user.username in logged_in_users,
                        'local_user': local_user_status.get(user.username, True),
                        'rooms': user_rooms.get(user.username, []),
                        'properties': [{'key': p.key, 'value': p.value} for p in user.properties]
                    }
                    users_data.append(user_data)
                self.output_data({'users': users_data})
        
        finally:
            client.close()
    
    def _output_as_text(self, data):
        """Output data as text."""
        if 'username' in data and 'users' not in data:
            # Single user
            logged_on_status = " (logged on)" if data['logged_on'] else " (not logged on)"
            local_status = " (local)" if data.get('local_user', True) else " (remote)"
            
            print(f"Username: {data['username']}{logged_on_status}{local_status}")
            print(f"Name: {data['name']}")
            print(f"Email: {data['email']}")
            # Display rooms user is in
            rooms = data.get('rooms', [])
            if rooms:
                print(f"Rooms: {', '.join(rooms)}")
            else:
                print("Rooms: None")
            properties = data.get('properties', [])
            if properties:
                print("Properties:")
                for prop in properties:
                    print(f"  {prop['key']}: {prop['value']}")
        else:
            # Multiple users
            users = data.get('users', [])
            print(f"Found {len(users)} users:")
            for user in users:
                logged_on_status = " (logged on)" if user['logged_on'] else ""
                local_status = " (local)" if user.get('local_user', True) else " (remote)"
                
                rooms = user.get('rooms', [])
                rooms_info = f" (Rooms: {', '.join(rooms)})" if rooms else ""
                print(f"  {user['username']}: {user['name']} ({user['email']}){logged_on_status}{local_status}{rooms_info}")
                properties = user.get('properties', [])
                if properties:
                    print(f"    Properties: {len(properties)}")


def main():
    """Main function for the users tool."""
    tool = UsersTool()
    tool.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
