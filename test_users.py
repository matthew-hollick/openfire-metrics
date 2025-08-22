"""
Test script for the OpenFire API users endpoint.
"""

import sys
import os

# Add the parent directory to the path so we can import the openfire_api module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client
from openfire_api.users import UsersAPI
from openfire_api.message_archive import MessageArchiveAPI


def main():
    """Test the OpenFire API users endpoint."""
    # Create a client
    client = create_client(
        url="http://localhost:9090/plugins/restapi/v1",
        auth_header="fred",
        insecure=True
    )
    
    # Create users API instance
    users_api = UsersAPI(client)
    
    # Create message archive API instance
    message_archive_api = MessageArchiveAPI(client)
    
    try:
        # Test getting all users
        print("Getting all users...")
        users = users_api.get_users()
        print(f"Found {len(users.users)} users")
        
        for user in users.users:
            print(f"  - {user.username}: {user.name} ({user.email})")
            if user.properties:
                print(f"    Properties: {len(user.properties)}")
        
        # Test getting all users with search filter
        print("\nGetting users with 'admin' in username...")
        users = users_api.get_users(search="admin")
        print(f"Found {len(users.users)} matching users")
        
        for user in users.users:
            print(f"  - {user.username}: {user.name} ({user.email})")
        
        # Test getting a specific user
        print("\nGetting specific user 'admin'...")
        user = users_api.get_user("admin")
        print(f"User: {user.username}: {user.name} ({user.email})")
        if user.properties:
            print(f"Properties: {len(user.properties)}")
            for prop in user.properties:
                print(f"  - {prop.key}: {prop.value}")
        
        # Test getting unread message count for a user
        print("\nGetting unread message count for 'admin'...")
        try:
            # Use the username as JID for now - in a real implementation, 
            # you might need the full JID including domain
            jid = f"{user.username}@localhost"  # Adjust domain as needed
            unread_count = message_archive_api.get_unread_message_count(jid)
            print(f"Unread messages for {user.username}: {unread_count}")
        except Exception as e:
            print(f"Could not retrieve unread message count: {e}")
        
        # Test getting unread message count for user 'dave'
        print("\nGetting specific user 'dave'...")
        try:
            user = users_api.get_user("dave")
            print(f"User: {user.username}: {user.name} ({user.email})")
            # Get unread message count for 'dave'
            print("\nGetting unread message count for 'dave'...")
            try:
                # Use the username as JID for now - in a real implementation, 
                # you might need the full JID including domain
                jid = f"{user.username}@localhost"  # Adjust domain as needed
                unread_count = message_archive_api.get_unread_message_count(jid)
                print(f"Unread messages for {user.username}: {unread_count}")
            except Exception as e:
                print(f"Could not retrieve unread message count: {e}")
        except Exception as e:
            print(f"Could not retrieve user 'dave': {e}")
        
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return 1
    
    finally:
        client.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
