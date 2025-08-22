"""
Standalone tool for retrieving OpenFire system properties (read-only monitoring).
"""

import sys
import os
import argparse
import json

# Add the parent directory to the path so we can import the openfire_api package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from openfire_api.client import create_client


def format_properties_as_json(properties_data: dict) -> str:
    """Format system properties data as JSON."""
    return json.dumps(properties_data, indent=2)


def format_properties_as_text(properties_data: dict) -> str:
    """Format system properties data as text."""
    if 'properties' in properties_data:
        # All properties format
        output = f"Found {len(properties_data['properties'])} system properties:\n"
        for prop in properties_data['properties']:
            output += f"  {prop['key']}: {prop['value']}\n"
        return output
    else:
        # Single property format
        output = f"{properties_data['key']}: {properties_data['value']}\n"
        return output


def get_all_properties(client, output_format: str = 'json'):
    """Get all system properties and format them according to the specified output format."""
    try:
        from openfire_api.system_properties import SystemPropertiesAPI
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
        
        if output_format == 'json':
            return format_properties_as_json(properties_data)
        else:
            return format_properties_as_text(properties_data)
            
    except Exception as e:
        raise Exception(f"Failed to retrieve system properties: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Retrieve OpenFire system properties (read-only monitoring).')
    parser.add_argument('--api-url', default='http://localhost:9090/plugins/restapi/v1', 
                        help='OpenFire REST API URL')
    parser.add_argument('--username', help='Username for basic authentication')
    parser.add_argument('--password', help='Password for basic authentication')
    parser.add_argument('--auth-header', help='Authorization header value')
    parser.add_argument('--insecure', action='store_true', 
                        help='Skip SSL certificate validation')
    parser.add_argument('--output-format', choices=['json', 'text'], default='json',
                        help='Output format (json or text)')
    
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
        # Get and print all properties by default
        result = get_all_properties(client, args.output_format)
        print(result)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main())
