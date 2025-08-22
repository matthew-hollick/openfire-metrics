"""
Standalone tool for retrieving and displaying OpenFire group information.
"""

import sys
import os
import argparse
import json

# Add the parent directory to the path so we can import the openfire_api package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from openfire_api.client import create_client


def format_groups_as_json(groups_data: dict) -> str:
    """Format groups data as JSON."""
    return json.dumps(groups_data, indent=2)


def format_groups_as_text(groups_data: dict) -> str:
    """Format groups data as text."""
    if 'groups' in groups_data:
        # All groups format
        output = f"Found {len(groups_data['groups'])} groups:\n"
        for group in groups_data['groups']:
            output += f"  {group['name']}\n"
            
            # Display admins
            admins = group.get('admins', [])
            if admins:
                output += f"    Admins ({len(admins)}):\n"
                for admin in admins:
                    output += f"      {admin}\n"
            else:
                output += "    Admins: None\n"
            
            # Display members
            members = group.get('members', [])
            if members:
                output += f"    Members ({len(members)}):\n"
                for member in members:
                    output += f"      {member}\n"
            else:
                output += "    Members: None\n"
        return output
    else:
        # Single group format
        output = f"Group: {groups_data['name']}\n"
        output += f"  Description: {groups_data.get('description', 'N/A')}\n"
        output += f"  Shared: {groups_data.get('shared', 'N/A')}\n"
        
        # Display admins
        admins = groups_data.get('admins', [])
        if admins:
            output += f"  Admins ({len(admins)}):\n"
            for admin in admins:
                output += f"    {admin}\n"
        else:
            output += "  Admins: None\n"
        
        # Display members
        members = groups_data.get('members', [])
        if members:
            output += f"  Members ({len(members)}):\n"
            for member in members:
                output += f"    {member}\n"
        else:
            output += "  Members: None\n"
        return output


def get_all_groups(client, output_format: str = 'json'):
    """Get all groups and format them according to the specified output format."""
    try:
        from openfire_api.groups import GroupsAPI
        groups_api = GroupsAPI(client)
        groups = groups_api.get_groups()
        
        # Convert to dictionary format for output
        groups_data = {
            'groups': [
                {
                    'name': group.name,
                    'description': group.description,
                    'shared': group.is_shared,
                    'members': group.members,
                    'admins': group.admins
                }
                for group in groups.groups
            ]
        }
        
        if output_format == 'json':
            return format_groups_as_json(groups_data)
        else:
            return format_groups_as_text(groups_data)
            
    except Exception as e:
        raise Exception(f"Failed to retrieve groups: {e}")


def get_group(client, group_name: str, output_format: str = 'json'):
    """Get a specific group and format it according to the specified output format."""
    try:
        from openfire_api.groups import GroupsAPI
        groups_api = GroupsAPI(client)
        group = groups_api.get_group(group_name)
        
        # Convert to dictionary format for output
        group_data = {
            'name': group.name,
            'description': group.description,
            'shared': group.is_shared,
            'members': group.members,
            'admins': group.admins
        }
        
        if output_format == 'json':
            return format_groups_as_json(group_data)
        else:
            return format_groups_as_text(group_data)
            
    except Exception as e:
        raise Exception(f"Failed to retrieve group '{group_name}': {e}")




def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Retrieve and manage OpenFire group information.')
    parser.add_argument('--api-url', default='http://localhost:9090/plugins/restapi/v1', 
                        help='OpenFire REST API URL')
    parser.add_argument('--username', help='Username for basic authentication')
    parser.add_argument('--password', help='Password for basic authentication')
    parser.add_argument('--auth-header', help='Authorization header value')
    parser.add_argument('--insecure', action='store_true', 
                        help='Skip SSL certificate validation')
    parser.add_argument('--output-format', choices=['json', 'text'], default='json',
                        help='Output format (json or text)')
    parser.add_argument('--group-name', help='Name of a specific group to retrieve')
    
    args = parser.parse_args()
    
    # Create client
    client = create_client(
        url=args.api_url,
        username=args.username,
        password=args.password,
        auth_header=args.auth_header,
        insecure=args.insecure
    )
    
    try:
        # Handle group retrieval
        if args.group_name:
            # Get specific group
            result = get_group(client, args.group_name, args.output_format)
        else:
            # Get all groups
            result = get_all_groups(client, args.output_format)
        
        print(result)
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main())
