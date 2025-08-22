#!/usr/bin/env python3

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openfire_api.client import create_client

# Create a client
client = create_client(
    url='http://localhost:9090/plugins/restapi/v1',
    auth_header='fred',
    insecure=False
)

try:
    # Get raw session data
    response = client.get('sessions')
    response.raise_for_status()
    
    data = response.json()
    print("Raw session data:")
    print(json.dumps(data, indent=2))
    
finally:
    client.close()
