#!/usr/bin/env python3
"""
OpenFire Security Audit Log Tool

A command-line tool to fetch OpenFire security audit logs.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

from openfire_api.client import create_client
from openfire_api.security_audit_log import SecurityAuditLogAPI


def format_logs_as_json(logs_data: dict) -> str:
    """Format security audit logs as JSON."""
    return json.dumps(logs_data, indent=2)


def format_logs_as_text(logs_data: dict) -> str:
    """Format security audit logs as human-readable text."""
    if not logs_data['logs']:
        return "No security audit logs found."
    
    lines = ["Security Audit Logs:"]
    lines.append("=" * 50)
    
    for log in logs_data['logs']:
        timestamp = datetime.fromtimestamp(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        lines.append(f"ID: {log['logId']}")
        lines.append(f"Timestamp: {timestamp}")
        lines.append(f"Username: {log['username']}")
        lines.append(f"Node: {log['node']}")
        lines.append(f"Summary: {log['summary']}")
        lines.append(f"Details: {log['details']}")
        lines.append("-" * 30)
    
    return "\n".join(lines)


def get_security_audit_logs(client, since_minutes: int, output_format: str = 'json'):
    """
    Fetch security audit logs from OpenFire.
    
    Args:
        client: OpenFire API client
        since_minutes: Number of minutes ago to start fetching logs
        output_format: Output format ('json' or 'text')
    
    Returns:
        str: Formatted logs
    """
    try:
        # Calculate start time based on since_minutes
        end_time = 0  # Now
        start_time = int((datetime.now() - timedelta(minutes=since_minutes)).timestamp())
        
        # Ensure start_time is not negative
        if start_time < 0:
            start_time = 0
        
        # Create API instance and fetch logs
        logs_api = SecurityAuditLogAPI(client)
        logs = logs_api.get_security_audit_logs(start_time=start_time, end_time=end_time)
        
        # Convert to dictionary for serialization
        logs_data = {
            'logs': [
                {
                    'logId': log.log_id,
                    'username': log.username,
                    'timestamp': log.timestamp,
                    'summary': log.summary,
                    'node': log.node,
                    'details': log.details
                }
                for log in logs.logs
            ]
        }
        
        if output_format == 'json':
            return format_logs_as_json(logs_data)
        else:
            return format_logs_as_text(logs_data)
            
    except Exception as e:
        raise Exception(f"Failed to retrieve security audit logs: {e}")


def main():
    """Main function for the security audit log tool."""
    parser = argparse.ArgumentParser(description='Retrieve OpenFire security audit logs (read-only monitoring).')
    parser.add_argument('--api-url', default='http://localhost:9090/plugins/restapi/v1', 
                        help='OpenFire REST API URL')
    parser.add_argument('--username', help='Username for basic authentication')
    parser.add_argument('--password', help='Password for basic authentication')
    parser.add_argument('--auth-header', help='Authorization header value')
    parser.add_argument('--insecure', action='store_true', help='Skip SSL certificate validation')
    parser.add_argument('--output-format', choices=['json', 'text'], default='json', 
                        help='Output format (json or text)')
    parser.add_argument('--since', type=int, default=60,
                        help='Number of minutes ago to start fetching logs (default: 60)')
    
    args = parser.parse_args()
    
    # Validate authentication arguments
    if args.username and not args.password:
        print("Error: Password is required when username is provided.", file=sys.stderr)
        return 1
    
    if not args.username and args.password:
        print("Error: Username is required when password is provided.", file=sys.stderr)
        return 1
    
    # Create API client
    client = create_client(url=args.api_url, username=args.username, password=args.password,
                          auth_header=args.auth_header, insecure=args.insecure)
    
    try:
        result = get_security_audit_logs(client, args.since, args.output_format)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    finally:
        client.close()


if __name__ == '__main__':
    sys.exit(main())
