#!/usr/bin/env python3
"""
OpenFire Sessions Tool

A command-line tool for retrieving session information from OpenFire.
"""

import sys
from datetime import datetime

from openfire_api.client import create_client
from openfire_api.sessions import SessionsAPI

# Import base tool class
from openfire_api.base_tool import BaseTool


class SessionsTool(BaseTool):
    """Sessions tool implementation."""
    
    def __init__(self):
        """Initialize the sessions tool."""
        super().__init__('Retrieve session information from OpenFire')
        self._add_sessions_arguments()
    
    def _add_sessions_arguments(self):
        """Add sessions-specific command-line arguments."""
        self.parser.add_argument('--username',
                                help='Retrieve sessions for a specific user')
    
    def run(self):
        """Run the sessions tool."""
        args = self.parse_args()
        
        # Create a client with auth from auth_utils
        client = create_client(
            url=args.url,
            auth_header=args.auth_header,
            insecure=args.insecure
        )
        
        # Create sessions API instance
        sessions_api = SessionsAPI(client)
        
        try:
            if args.username:
                # Get sessions for specific user
                sessions = sessions_api.get_user_sessions(args.username)
                sessions_data = {
                    'sessions': [
                        self._session_to_dict(session)
                        for session in sessions.sessions
                    ]
                }
                self.output_data(sessions_data)
            else:
                # Get all sessions
                sessions = sessions_api.get_sessions()
                sessions_data = {
                    'sessions': [
                        self._session_to_dict(session)
                        for session in sessions.sessions
                    ]
                }
                self.output_data(sessions_data)
        
        finally:
            client.close()
    
    def _session_to_dict(self, session):
        """Convert a session object to a dictionary."""
        return {
            'session_id': session.session_id,
            'username': session.username,
            'resource': session.resource,
            'node': session.node,
            'session_status': session.session_status,
            'presence_status': session.presence_status,
            'presence_message': session.presence_message,
            'priority': session.priority,
            'host_address': session.host_address,
            'host_name': session.host_name,
            'creation_date': datetime.fromtimestamp(session.creation_date/1000).strftime('%Y-%m-%d %H:%M:%S') if session.creation_date else None,
            'last_action_date': datetime.fromtimestamp(session.last_action_date/1000).strftime('%Y-%m-%d %H:%M:%S') if session.last_action_date else None,
            'secure': session.secure,
            'jid': session.session_id.split('/')[0] if session.session_id else None  # Bare JID without resource
        }
    
    def _output_as_text(self, data):
        """Output data as text."""
        if 'sessions' in data:
            sessions = data['sessions']
            if len(sessions) > 0 and 'resource' in sessions[0]:
                # Detailed format for user-specific sessions
                print(f"Found {len(sessions)} sessions for user '{sessions[0]['username']}':")
                for session in sessions:
                    print(f"  Session ID: {session['session_id']}")
                    print(f"    Username: {session['username']}")
                    print(f"    Resource: {session['resource'] or 'N/A'}")
                    print(f"    Node: {session['node'] or 'N/A'}")
                    print(f"    Session Status: {session['session_status'] or 'N/A'}")
                    print(f"    Presence Status: {session['presence_status'] or 'N/A'}")
                    print(f"    Presence Message: {session['presence_message'] or 'N/A'}")
                    print(f"    Priority: {session['priority'] or 'N/A'}")
                    print(f"    Host Address: {session['host_address'] or 'N/A'}")
                    print(f"    Host Name: {session['host_name'] or 'N/A'}")
                    print(f"    Creation Date: {session['creation_date'] or 'N/A'}")
                    print(f"    Last Action Date: {session['last_action_date'] or 'N/A'}")
                    print(f"    Secure: {session['secure'] or 'N/A'}")
                    print(f"    JID: {session['jid'] or 'N/A'}")
            else:
                # Simple format for all sessions
                print(f"Found {len(sessions)} sessions:")
                for session in sessions:
                    print(f"  {session['username']}: {session['session_id']} ({session['session_status'] or 'N/A'})")
                    print(f"    JID: {session['jid'] or 'N/A'}")
                    print(f"    Host: {session['host_name'] or session['host_address'] or 'N/A'}")
                    print(f"    Resource: {session['resource'] or 'N/A'}")
                    print(f"    Node: {session['node'] or 'N/A'}")
                    print(f"    Creation Date: {session['creation_date'] or 'N/A'}")
                    print(f"    Last Action Date: {session['last_action_date'] or 'N/A'}")

def main():
    """Main function for the sessions tool."""
    tool = SessionsTool()
    tool.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
