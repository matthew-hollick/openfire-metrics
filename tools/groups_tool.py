#!/usr/bin/env python3
"""
OpenFire Groups Tool

A command-line tool for retrieving and displaying OpenFire group information.
"""

import sys
import os

# Add the parent directory to the path so we can import the openfire_api module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.groups import GroupsAPI
from openfire_api.base_tool import BaseTool
from openfire_api.client import create_client


class GroupsTool(BaseTool):
    """Groups tool implementation."""
    
    def __init__(self):
        """Initialize the groups tool."""
        super().__init__('Retrieve group information from OpenFire')
        self._add_groups_arguments()
    
    def _add_groups_arguments(self):
        """Add groups-specific command-line arguments."""
        self.parser.add_argument('--group-name', help='Name of a specific group to retrieve')
    
    def run(self):
        """Run the groups tool."""
        args = self.parse_args()
        
        # Create a client
        client = create_client(
            url=args.url,
            auth_header=args.auth_header,
            insecure=args.insecure
        )
        
        try:
            groups_api = GroupsAPI(client)
            
            if args.group_name:
                # Get specific group
                group = groups_api.get_group(args.group_name)
                group_data = {
                    'name': group.name,
                    'description': group.description,
                    'shared': group.is_shared,
                    'members': group.members,
                    'admins': group.admins
                }
                self.output_data(group_data)
            else:
                # Get all groups
                groups = groups_api.get_groups()
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
                self.output_data(groups_data)
        
        finally:
            client.close()
    
    def _output_as_text(self, data):
        """Output data as text."""
        if 'groups' in data:
            # All groups format
            print(f"Found {len(data['groups'])} groups:")
            for group in data['groups']:
                print(f"  {group['name']}")
                
                # Display admins
                admins = group.get('admins', [])
                if admins:
                    print(f"    Admins ({len(admins)}):")
                    for admin in admins:
                        print(f"      {admin}")
                else:
                    print("    Admins: None")
                
                # Display members
                members = group.get('members', [])
                if members:
                    print(f"    Members ({len(members)}):")
                    for member in members:
                        print(f"      {member}")
                else:
                    print("    Members: None")
        else:
            # Single group format
            print(f"Group: {data['name']}")
            print(f"  Description: {data.get('description', 'N/A')}")
            print(f"  Shared: {data.get('shared', 'N/A')}")
            
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

def main():
    """Main function for the groups tool."""
    tool = GroupsTool()
    tool.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
