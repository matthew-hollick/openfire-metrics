#!/usr/bin/env python3
"""
Simple HTTP endpoint for testing the OpenFire tools' HTTP output functionality.
"""

import json
import base64
import click
from flask import Flask, request, jsonify


def create_test_endpoint(username=None, password=None, require_auth=False, debug=False):
    """Create a simple Flask app for testing HTTP output."""
    app = Flask(__name__)
    
    def check_auth(headers):
        """Check if the request has valid authentication."""
        if not require_auth:
            return True
            
        auth_header = headers.get('Authorization')
        if not auth_header:
            return False
            
        if auth_header.startswith('Basic '):
            try:
                encoded_credentials = auth_header.split(' ')[1]
                decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
                req_username, req_password = decoded_credentials.split(':', 1)
                return req_username == username and req_password == password
            except Exception:
                return False
        
        return False
    
    @app.route('/', methods=['POST'])
    def receive_data():
        """Receive and log POST data."""
        # Check authentication if required
        if require_auth and not check_auth(request.headers):
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
        print("Received POST request")
        print(f"Content-Type: {request.content_type}")
        
        # Get headers
        print("Headers:")
        for header, value in request.headers:
            print(f"  {header}: {value}")
        
        # Get data
        if request.is_json:
            data = request.get_json()
            print("Data:")
            print(json.dumps(data, indent=2))
            
            # Debug option: echo full JSON object
            if debug:
                print("DEBUG: Full JSON object received:")
                print(json.dumps(data, indent=2, sort_keys=True))
        else:
            data = request.get_data(as_text=True)
            print("Data:")
            print(data)
            
            # Debug option: echo full data
            if debug:
                print("DEBUG: Full data received:")
                print(data)
        
        print("---")
        
        return jsonify({"status": "success", "message": "Data received"}), 200
    
    @app.route('/', methods=['GET'])
    def health_check():
        """Simple health check endpoint."""
        # Check authentication if required
        if require_auth and not check_auth(request.headers):
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
            
        return jsonify({"status": "ok", "message": "Test HTTP endpoint is running"}), 200
    
    return app


@click.command()
@click.option('--host', default='localhost', help='Host to bind the server to')
@click.option('--port', default=8081, help='Port to bind the server to')
@click.option('--username', default=None, help='Username for basic authentication')
@click.option('--password', default=None, help='Password for basic authentication')
@click.option('--require-auth', is_flag=True, help='Require authentication for all requests')
@click.option('--debug', is_flag=True, help='Enable debug mode to echo full JSON object received')
def main(host, port, username, password, require_auth, debug):
    """Run the test HTTP endpoint."""
    app = create_test_endpoint(username, password, require_auth, debug)
    print(f"Starting test HTTP endpoint on http://{host}:{port}")
    if require_auth:
        print(f"Authentication required: username='{username}', password='{password}'")
    if debug:
        print("Debug mode enabled: Full JSON objects will be echoed")
    print("Press Ctrl+C to stop")
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    main()
