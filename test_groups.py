"""
Test script for the OpenFire groups endpoint.
"""

import sys
import os

# Add the parent directory to the path so we can import the openfire_api package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from openfire_api.client import create_client
from openfire_api.groups import GroupsAPI


def test_groups_api():
    """Test the groups API functionality."""
    # Create client
    client = create_client(
        url='http://localhost:9090/plugins/restapi/v1',
        auth_header='fred',
        insecure=True
    )
    
    try:
        # Initialize the groups API
        groups_api = GroupsAPI(client)
        
        # Test getting all groups
        print("Getting all groups...")
        groups = groups_api.get_groups()
        print(f"Found {len(groups.groups)} groups:")
        for group in groups.groups:
            print(f"  - {group.name}: {group.description}")
            if group.admins:
                print(f"    Admins ({len(group.admins)}): {', '.join(group.admins)}")
            else:
                print("    Admins: None")
            if group.members:
                print(f"    Members ({len(group.members)}): {', '.join(group.members)}")
            else:
                print("    Members: None")
        
        # If there are groups, test getting a specific group
        if groups.groups:
            first_group_name = groups.groups[0].name
            print(f"\nGetting details for group '{first_group_name}'...")
            group = groups_api.get_group(first_group_name)
            print(f"Group details: {group.name}: {group.description}")
            if group.admins:
                print(f"Admins ({len(group.admins)}): {', '.join(group.admins)}")
            else:
                print("Admins: None")
            if group.members:
                print(f"Members ({len(group.members)}): {', '.join(group.members)}")
            else:
                print("Members: None")
        
        print("\nAll tests passed!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    finally:
        client.close()
    
    return 0


def main():
    """Main function."""
    return test_groups_api()


if __name__ == "__main__":
    sys.exit(main())
