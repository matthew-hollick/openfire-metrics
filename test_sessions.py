"""
Test script for the OpenFire API sessions endpoint.
"""

import sys
import os

# Add the parent directory to the path so we can import the openfire_api module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client
from openfire_api.sessions import SessionsAPI

def main():
    """Test the OpenFire API sessions endpoint."""
    # Create a client
    client = create_client(
        url="http://localhost:9090/plugins/restapi/v1",
        auth_header="fred",
        insecure=True
    )
    
    # Create sessions API instance
    sessions_api = SessionsAPI(client)
    
    try:
        # Test getting all sessions
        print("Getting all sessions...")
        sessions = sessions_api.get_sessions()
        print(f"Found {len(sessions.sessions)} sessions")
        
        for session in sessions.sessions:
            print(f"  - {session.username}: {session.session_id} ({session.session_status})")
            print(f"    JID: {session.jid or 'N/A'}")
            print(f"    Host Address: {session.host_address or 'N/A'}")
            print(f"    Host Name: {session.host_name or 'N/A'}")
        
        # Test getting sessions for a specific user (if any users exist)
        if sessions.sessions:
            username = sessions.sessions[0].username
            print(f"\nGetting sessions for user '{username}'...")
            user_sessions = sessions_api.get_user_sessions(username)
            print(f"Found {len(user_sessions.sessions)} sessions for user '{username}'")
            
            for session in user_sessions.sessions:
                print(f"  - {session.session_id}: {session.session_status}")
        
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return 1
    
    finally:
        client.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
