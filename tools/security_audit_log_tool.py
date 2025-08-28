#!/usr/bin/env python3
"""
OpenFire Security Audit Log Tool

A command-line tool to fetch OpenFire security audit logs.
"""

import sys
from datetime import datetime, timedelta

from openfire_api.client import create_client
from openfire_api.security_audit_log import SecurityAuditLogAPI

# Import base tool class
from openfire_api.base_tool import BaseTool


class SecurityAuditLogTool(BaseTool):
    """Security audit log tool implementation."""
    
    def __init__(self):
        """Initialize the security audit log tool."""
        super().__init__('Retrieve OpenFire security audit logs (read-only monitoring)')
        self._add_security_audit_log_arguments()
    
    def _add_security_audit_log_arguments(self):
        """Add security audit log-specific command-line arguments."""
        self.parser.add_argument('--since', type=int, default=60,
                                help='Number of minutes ago to start fetching logs (default: 60)')
    
    def run(self):
        """Run the security audit log tool."""
        args = self.parse_args()
        
        # Create API client with auth from auth_utils
        client = create_client(url=args.url, auth_header=args.auth_header, insecure=args.insecure)
        
        try:
            # Calculate start time based on since_minutes
            end_time = 0  # Now
            start_time = int((datetime.now() - timedelta(minutes=args.since)).timestamp())
            
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
            
            self.output_data(logs_data)
        
        finally:
            client.close()
    
    def _output_as_text(self, data):
        """Output data as text."""
        if not data['logs']:
            print("No security audit logs found.")
            return
        
        print("Security Audit Logs:")
        print("=" * 50)
        
        for log in data['logs']:
            timestamp = datetime.fromtimestamp(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            print(f"ID: {log['logId']}")
            print(f"Timestamp: {timestamp}")
            print(f"Username: {log['username']}")
            print(f"Node: {log['node']}")
            print(f"Summary: {log['summary']}")
            print(f"Details: {log['details']}")
            print("-" * 30)

def main():
    """Main function for the security audit log tool."""
    tool = SecurityAuditLogTool()
    tool.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
