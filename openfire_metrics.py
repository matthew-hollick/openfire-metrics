#!/usr/bin/env python3
"""
Openfire Metrics CLI Tool

Connects to Openfire REST API and exports data in NDJSON format for Elasticsearch ingestion.
"""

import click
import requests
import json
import os
import logging
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Constants
OPENFIRE_API_BASE_URL = 'http://localhost:9090/plugins/restapi/v1'


def get_auth(username, password, auth_header):
    """Get authentication tuple or header."""
    if username and password:
        return (username, password)
    return None

def get_last_timestamp_from_log(log_file_path):
    """Extract the last timestamp from the security logs in the existing log file."""
    if not os.path.exists(log_file_path):
        return None
    
    last_timestamp = None
    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                # Skip log lines that are not JSON (like the INFO line)
                if line.startswith('{'):
                    try:
                        data = json.loads(line)
                        # Extract logs array from the JSON
                        if 'logs' in data and isinstance(data['logs'], list):
                            # Find the highest timestamp in this batch of logs
                            for log_entry in data['logs']:
                                if 'timestamp' in log_entry:
                                    timestamp = log_entry['timestamp']
                                    if last_timestamp is None or timestamp > last_timestamp:
                                        last_timestamp = timestamp
                    except json.JSONDecodeError:
                        # Skip lines that aren't valid JSON
                        continue
    except Exception as e:
        # If there's any error reading the file, we'll just return None
        # which will cause the tool to fetch all logs
        pass
    
    return last_timestamp


def get_headers(auth_header):
    """Get headers including authorization and accept headers."""
    headers = {'Accept': 'application/json'}
    if auth_header:
        headers['Authorization'] = auth_header
    return headers


def output_ndjson(data, index_prefix="openfire"):
    """Output data in NDJSON format (one document per line)."""
    if isinstance(data, list):
        # Handle list of items
        for item in data:
            click.echo(json.dumps(item, separators=(',', ':')))
    elif isinstance(data, dict):
        # Handle single object
        click.echo(json.dumps(data, separators=(',', ':')))
    else:
        # Handle primitive types
        click.echo(json.dumps(data, separators=(',', ':')))


def get_24h_ago_timestamp():
    """Get Unix timestamp for 24 hours ago."""
    from datetime import datetime, timedelta
    return int((datetime.now() - timedelta(hours=24)).timestamp())



@click.command()
@click.option('--url', '-u',
              default=lambda: os.environ.get('OPENFIRE_URL', f'{OPENFIRE_API_BASE_URL}/users'),
              help='REST API endpoint URL')
@click.option('--endpoint', '-e',
              type=click.Choice([
                  'users', 'groups', 'sessions', 'system', 'chatrooms', 'user-roster',
                  'system-properties', 'security-logs'
              ]),
              default='users',
              help='Predefined REST API endpoints')
@click.option('--username',
              default=lambda: os.environ.get('OPENFIRE_USERNAME', ''),
              help='Username for basic authentication')
@click.option('--password',
              default=lambda: os.environ.get('OPENFIRE_PASSWORD', ''),
              help='Password for basic authentication')
@click.option('--auth-header',
              default=lambda: os.environ.get('OPENFIRE_AUTH_HEADER', ''),
              help='Authorization header value')
@click.option('--output-format', '-f',
              type=click.Choice(['json', 'ndjson']),
              default='json',
              help='Output format')
@click.option('--index-prefix', '-p',
              default='openfire',
              help='Index prefix for NDJSON output')
@click.option('--iterate', '-i',
              is_flag=True,
              help='Iterate through list endpoints and fetch individual items')
@click.option('--incremental',
              is_flag=True,
              help='For security-logs: pull logs since last timestamp in existing log file (requires --enable-logging)')
@click.option('--start-time',
              type=int,
              help='Start time for security-logs endpoint (Unix timestamp)')
@click.option('--end-time',
              type=int,
              help='End time for security-logs endpoint (Unix timestamp)')
@click.option('--log-path',
              default='/var/log/openfire-metrics',
              help='Log path for output files (default: /var/log/openfire-metrics)')
@click.option('--enable-logging', '-l',
              is_flag=True,
              help='Enable logging to file (default: no)')
@click.option('--insecure',
              is_flag=True,
              help='Skip SSL certificate validation')
def main(url, endpoint, username, password, auth_header, output_format, index_prefix, iterate, incremental, start_time, end_time, log_path, enable_logging, insecure):
    """Connect to Openfire REST API and output data."""
    # Set up logging
    if enable_logging:
        # Create log directory if it doesn't exist
        os.makedirs(log_path, exist_ok=True)
        
        # Create log filename with opinionated format
        current_date = datetime.now().strftime('%Y-%m-%d')
        log_filename = f"{endpoint}-{current_date}.{output_format}"
        log_file = os.path.join(log_path, log_filename)
        
        # Set up logging
        if output_format == 'ndjson':
            # For NDJSON, we don't want any non-JSON lines in the file
            # We'll just open the file for appending without setting up logging
            pass
        else:
            # For JSON format, we can use standard logging
            logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', filemode='a')
            logging.info(f'Started logging for endpoint {endpoint}')

    # If endpoint is specified, override URL
    if endpoint and url == f'{OPENFIRE_API_BASE_URL}/users':
        if endpoint == 'security-logs':
            # Special handling for security-logs endpoint
            url = f"{OPENFIRE_API_BASE_URL}/logs/security"
            # Add query parameters if provided
            params = []
            
            # Handle incremental feature with pragmatic approach
            if incremental and enable_logging and not start_time and not end_time:
                # Check for log files with today's and yesterday's dates
                from datetime import datetime as dt, timedelta
                today = dt.now()
                yesterday = today - timedelta(days=1)
                
                # Try to find existing log files
                log_files_to_check = [
                    os.path.join(log_path, f"{endpoint}-{today.strftime('%Y-%m-%d')}.{output_format}"),
                    os.path.join(log_path, f"{endpoint}-{yesterday.strftime('%Y-%m-%d')}.{output_format}")
                ]
                
                found_log_file = None
                for log_file_path in log_files_to_check:
                    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > 0:
                        found_log_file = log_file_path
                        break
                
                if found_log_file:
                    # Get the last timestamp from the existing log file
                    last_timestamp = get_last_timestamp_from_log(found_log_file)
                    if last_timestamp:
                        # Add one second to avoid duplicates
                        start_time = last_timestamp + 1
                else:
                    # No log file found, pull the last 24 hours of logs
                    start_time = get_24h_ago_timestamp()
            
            if start_time:
                params.append(f"startTime={start_time}")
            if end_time:
                params.append(f"endTime={end_time}")
            if params:
                url += "?" + "&".join(params)
        elif endpoint == 'system-properties':
            # Alias for system
            url = f"{OPENFIRE_API_BASE_URL}/system/properties"
        else:
            url = f"{OPENFIRE_API_BASE_URL}/{endpoint}"
    elif not endpoint:
        # If no endpoint specified, try to infer from URL
        if '/users' in url:
            endpoint = 'users'
        elif '/groups' in url:
            endpoint = 'groups'
        elif '/sessions' in url:
            endpoint = 'sessions'
        elif '/system' in url:
            endpoint = 'system'
        elif '/chatrooms' in url:
            endpoint = 'chatrooms'
        elif '/logs/security' in url:
            endpoint = 'security-logs'

    # Set up authentication
    auth = get_auth(username, password, auth_header)
    headers = get_headers(auth_header)

    # If iterate flag is set and we have a list endpoint, fetch individual items
    if iterate and endpoint in ['users', 'groups', 'chatrooms']:
        try:
            response = requests.get(url, auth=auth, headers=headers, verify=not insecure)
            response.raise_for_status()
            data = response.json()
            
            # Determine the list key based on endpoint
            list_key = None
            if endpoint == 'users':
                list_key = 'users'
            elif endpoint == 'groups':
                list_key = 'groups'
            elif endpoint == 'chatrooms':
                list_key = 'chatRooms'
            
            # Process list items
            if list_key and list_key in data:
                for item in data[list_key]:
                    # Get the ID for the item
                    item_id = None
                    if endpoint == 'users' and 'username' in item:
                        item_id = item['username']
                    elif endpoint == 'groups' and 'name' in item:
                        item_id = item['name']
                    elif endpoint == 'chatrooms' and 'roomName' in item:
                        item_id = item['roomName']
                    
                    # Fetch individual item if we have an ID
                    if item_id:
                        item_url = f"{base_url}/{endpoint}/{item_id}"
                        try:
                            item_response = requests.get(item_url, auth=auth, headers=headers, verify=not insecure)
                            item_response.raise_for_status()
                            item_data = item_response.json()
                            
                            # For chatrooms, also get user count
                            if endpoint == 'chatrooms' and item_id:
                                # Try to get occupants count
                                occupants_url = f"{base_url}/{endpoint}/{item_id}/occupants"
                                try:
                                    occupants_response = requests.get(occupants_url, auth=auth, headers=headers, verify=not insecure)
                                    occupants_response.raise_for_status()
                                    occupants_data = occupants_response.json()
                                    
                                    # Add user count to chatroom data
                                    if 'occupants' in occupants_data:
                                        item_data['userCount'] = len(occupants_data['occupants'])
                                        item_data['occupants'] = occupants_data['occupants']
                                except requests.exceptions.RequestException:
                                    # If occupants endpoint fails, try participants
                                    try:
                                        participants_url = f"{base_url}/{endpoint}/{item_id}/participants"
                                        participants_response = requests.get(participants_url, auth=auth, headers=headers, verify=not insecure)
                                        participants_response.raise_for_status()
                                        participants_data = participants_response.json()
                                        
                                        # Add user count to chatroom data
                                        if 'participants' in participants_data:
                                            item_data['userCount'] = len(participants_data['participants'])
                                            item_data['participants'] = participants_data['participants']
                                    except requests.exceptions.RequestException:
                                        # If both fail, just leave the data as is
                                        pass
                            
                            # Output to file if logging is enabled
                            if enable_logging:
                                with open(log_file, 'a') as f:
                                    if output_format == 'ndjson':
                                        # Output in NDJSON format (one document per line)
                                        if isinstance(item_data, list):
                                            for item in item_data:
                                                f.write(json.dumps(item, separators=(',', ':')) + '\n')
                                        elif isinstance(item_data, dict):
                                            f.write(json.dumps(item_data, separators=(',', ':')) + '\n')
                                        else:
                                            f.write(json.dumps(item_data, separators=(',', ':')) + '\n')
                                    else:
                                        f.write(f"Item: {item_id}\n")
                                        f.write(json.dumps(item_data, indent=2) + '\n')
                                
                                # Also output to console
                                if output_format == 'ndjson':
                                    output_ndjson(item_data, index_prefix)
                                else:
                                    click.echo(f"Item: {item_id}")
                                    click.echo(json.dumps(item_data, indent=2))
                            else:
                                # Output to console only
                                if output_format == 'ndjson':
                                    output_ndjson(item_data, index_prefix)
                                else:
                                    click.echo(f"Item: {item_id}")
                                    click.echo(json.dumps(item_data, indent=2))
                        except requests.exceptions.RequestException as e:
                            error_msg = f"Error fetching item {item_id}: {e}"
                            if enable_logging:
                                logging.error(error_msg)
                            click.echo(error_msg, err=True)
                    else:
                        # Output the item as is
                        if enable_logging:
                            with open(log_file, 'a') as f:
                                if output_format == 'ndjson':
                                    # Handle NDJSON output (one document per line)
                                    if isinstance(item, list):
                                        for item_entry in item:
                                            f.write(json.dumps(item_entry, separators=(',', ':')) + '\n')
                                    elif isinstance(item, dict):
                                        f.write(json.dumps(item, separators=(',', ':')) + '\n')
                                    else:
                                        f.write(json.dumps(item, separators=(',', ':')) + '\n')
                                else:
                                    f.write(json.dumps(item, indent=2) + '\n')
                            
                            # Also output to console
                            if output_format == 'ndjson':
                                output_ndjson(item, index_prefix)
                            else:
                                click.echo(json.dumps(item, indent=2))
                        else:
                            # Output to console only
                            if output_format == 'ndjson':
                                output_ndjson(item, index_prefix)
                            else:
                                click.echo(json.dumps(item, indent=2))
            else:
                error_msg = "No list data found in response"
                if enable_logging:
                    logging.error(error_msg)
                click.echo(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Error connecting to API: {e}"
            if enable_logging:
                logging.error(error_msg)
            click.echo(error_msg, err=True)
            raise click.Abort()
    else:
        # Standard mode - make request
        try:
            response = requests.get(url, auth=auth, headers=headers, verify=not insecure)
            
            # Output status code if in JSON mode
            if output_format == 'json' and not enable_logging:
                click.echo(f"Status Code: {response.status_code}")
            elif output_format == 'json' and enable_logging:
                with open(log_file, 'a') as f:
                    f.write(f"Status Code: {response.status_code}\n")
                click.echo(f"Status Code: {response.status_code}")
            
            # Try to parse and output JSON
            try:
                json_data = response.json()
                if output_format == 'json':
                    if enable_logging:
                        with open(log_file, 'a') as f:
                            f.write("Response JSON:\n")
                            f.write(json.dumps(json_data, indent=2) + '\n')
                        click.echo("Response JSON:")
                        click.echo(json.dumps(json_data, indent=2))
                    else:
                        click.echo("Response JSON:")
                        click.echo(json.dumps(json_data, indent=2))
                else:
                    # Output in NDJSON format for Elasticsearch
                    if enable_logging:
                        with open(log_file, 'a') as f:
                            # Write NDJSON to file (one document per line)
                            if isinstance(json_data, list):
                                for item in json_data:
                                    f.write(json.dumps(item, separators=(',', ':')) + '\n')
                            elif isinstance(json_data, dict):
                                f.write(json.dumps(json_data, separators=(',', ':')) + '\n')
                            else:
                                f.write(json.dumps(json_data, separators=(',', ':')) + '\n')
                        
                        # Also output to console
                        output_ndjson(json_data, index_prefix)
                    else:
                        # Output to console only
                        output_ndjson(json_data, index_prefix)
            except json.JSONDecodeError:
                if output_format == 'json':
                    if enable_logging:
                        with open(log_file, 'a') as f:
                            f.write("Response (non-JSON):\n")
                            f.write(response.text + '\n')
                        click.echo("Response (non-JSON):")
                        click.echo(response.text)
                    else:
                        click.echo("Response (non-JSON):")
                        click.echo(response.text)
                else:
                    # For NDJSON, try to output as is
                    if enable_logging:
                        with open(log_file, 'a') as f:
                            f.write(response.text + '\n')
                        click.echo(response.text)
                    else:
                        click.echo(response.text)
                    
        except requests.exceptions.RequestException as e:
            error_msg = f"Error connecting to API: {e}"
            if enable_logging:
                logging.error(error_msg)
            click.echo(error_msg, err=True)
            raise click.Abort()


if __name__ == '__main__':
    main()
