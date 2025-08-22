#!/usr/bin/env python3
"""
OpenFire Sessions Tool

A standalone tool for retrieving session information from OpenFire.
"""

import json
import sys
import os
import argparse
from datetime import datetime

# Add the parent directory to the path so we can import the openfire_api module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client
from openfire_api.sessions import SessionsAPI


def main():
    """Main function for the sessions tool."""
    parser = argparse.ArgumentParser(description='Retrieve session information from OpenFire')
    parser.add_argument('--url', default='http://localhost:9090/plugins/restapi/v1',
                        help='OpenFire REST API URL')
    parser.add_argument('--auth-header', required=True,
                        help='Authorization header value')
    parser.add_argument('--insecure', action='store_true',
                        help='Skip SSL certificate validation')
    parser.add_argument('--username',
                        help='Retrieve sessions for a specific user')
    parser.add_argument('--output-format', choices=['json', 'text'], default='json',
                        help='Output format')
    
    args = parser.parse_args()
    
    # Create a client
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
            if args.output_format == 'json':
                sessions_data = []
                for session in sessions.sessions:
                    session_data = {
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
                    sessions_data.append(session_data)
                print(json.dumps({'sessions': sessions_data}, indent=2))
            else:
                print(f"Found {len(sessions.sessions)} sessions for user '{args.username}':")
                for session in sessions.sessions:
                    print(f"  Session ID: {session.session_id}")
                    print(f"    Username: {session.username}")
                    print(f"    Resource: {session.resource or 'N/A'}")
                    print(f"    Node: {session.node or 'N/A'}")
                    print(f"    Session Status: {session.session_status or 'N/A'}")
                    print(f"    Presence Status: {session.presence_status or 'N/A'}")
                    print(f"    Presence Message: {session.presence_message or 'N/A'}")
                    print(f"    Priority: {session.priority or 'N/A'}")
                    print(f"    Host Address: {session.host_address or 'N/A'}")
                    print(f"    Host Name: {session.host_name or 'N/A'}")
                    print(f"    Creation Date: {datetime.fromtimestamp(session.creation_date/1000).strftime('%Y-%m-%d %H:%M:%S') if session.creation_date else 'N/A'}")
                    print(f"    Last Action Date: {datetime.fromtimestamp(session.last_action_date/1000).strftime('%Y-%m-%d %H:%M:%S') if session.last_action_date else 'N/A'}")
                    print(f"    Secure: {session.secure or 'N/A'}")
                    print(f"    JID: {session.session_id.split('/')[0] if session.session_id else 'N/A'}")
        else:
            # Get all sessions
            sessions = sessions_api.get_sessions()
            if args.output_format == 'json':
                sessions_data = []
                for session in sessions.sessions:
                    session_data = {
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
                    sessions_data.append(session_data)
                print(json.dumps({'sessions': sessions_data}, indent=2))
            else:
                print(f"Found {len(sessions.sessions)} sessions:")
                for session in sessions.sessions:
                    print(f"  {session.username}: {session.session_id} ({session.session_status or 'N/A'})")
                    print(f"    JID: {session.session_id.split('/')[0] if session.session_id else 'N/A'}")
                    print(f"    Host: {session.host_name or session.host_address or 'N/A'}")
                    print(f"    Resource: {session.resource or 'N/A'}")
                    print(f"    Node: {session.node or 'N/A'}")
                    print(f"    Creation Date: {datetime.fromtimestamp(session.creation_date/1000).strftime('%Y-%m-%d %H:%M:%S') if session.creation_date else 'N/A'}")
                    print(f"    Last Action Date: {datetime.fromtimestamp(session.last_action_date/1000).strftime('%Y-%m-%d %H:%M:%S') if session.last_action_date else 'N/A'}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    finally:
        client.close()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
