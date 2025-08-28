#!/usr/bin/env python3
"""
OpenFire System Properties Tool

A command-line tool for retrieving OpenFire system properties (read-only monitoring).
"""

import sys

from openfire_api.system_properties import SystemPropertiesAPI
from openfire_api.base_tool import BaseTool
from openfire_api.client import create_client


class SystemPropertiesTool(BaseTool):
    """System properties tool implementation."""
    
    def __init__(self):
        """Initialize the system properties tool."""
        super().__init__('Retrieve system properties from OpenFire (read-only monitoring)')
        # No additional arguments needed for system properties
    
    def run(self):
        """Run the system properties tool."""
        args = self.parse_args()
        
        # Create a client with auth from auth_utils
        client = create_client(
            url=args.url,
            auth_header=args.auth_header,
            insecure=args.insecure
        )
        
        try:
            properties_api = SystemPropertiesAPI(client)
            properties = properties_api.get_system_properties()
            
            # Convert to dictionary format for output
            properties_data = {
                'properties': [
                    {
                        'key': prop.key,
                        'value': prop.value
                    }
                    for prop in properties.properties
                ]
            }
            self.output_data(properties_data)
        
        finally:
            client.close()
    
    def _output_as_text(self, data):
        """Output data as text."""
        if 'properties' in data:
            # All properties format
            print(f"Found {len(data['properties'])} system properties:")
            for prop in data['properties']:
                print(f"  {prop['key']}: {prop['value']}")
        else:
            # Single property format
            print(f"{data['key']}: {data['value']}")

def main():
    """Main function for the system properties tool."""
    tool = SystemPropertiesTool()
    tool.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
