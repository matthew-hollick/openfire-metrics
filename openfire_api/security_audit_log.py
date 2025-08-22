"""
OpenFire API Security Audit Log Module

This module provides functionality for interacting with the OpenFire security audit log endpoint.
"""

from typing import List, Optional
from .client import OpenFireAPIClient


class SecurityAuditLog:
    """Represents a security audit log entry."""
    
    def __init__(self, log_id: int, username: str, timestamp: int, summary: str, 
                 node: str, details: str):
        self.log_id = log_id
        self.username = username
        self.timestamp = timestamp
        self.summary = summary
        self.node = node
        self.details = details


class SecurityAuditLogs:
    """Represents a collection of security audit log entries."""
    
    def __init__(self, logs: List[SecurityAuditLog]):
        self.logs = logs


class SecurityAuditLogAPI:
    """API for interacting with OpenFire security audit logs (read-only)."""
    
    def __init__(self, client: OpenFireAPIClient):
        self.client = client
    
    def get_security_audit_logs(self, username: Optional[str] = None, 
                               offset: int = 0, limit: int = 100,
                               start_time: Optional[int] = None, 
                               end_time: Optional[int] = None) -> SecurityAuditLogs:
        """
        Retrieve security audit log entries.
        
        Args:
            username: The name of a user for which to filter events
            offset: Number of log entries to skip
            limit: Number of log entries to retrieve
            start_time: Oldest timestamp of range of logs to retrieve. 0 for 'forever'
            end_time: Most recent timestamp of range of logs to retrieve. 0 for 'now'
            
        Returns:
            SecurityAuditLogs: A collection of security audit log entries
        """
        params = {
            'offset': offset,
            'limit': limit
        }
        
        if username:
            params['username'] = username
        
        if start_time is not None:
            params['startTime'] = start_time
            
        if end_time is not None:
            params['endTime'] = end_time
        
        response = self.client.get('logs/security', params=params)
        response.raise_for_status()
        
        data = response.json()
        logs = []
        
        for log_data in data.get('logs', []):
            log = SecurityAuditLog(
                log_id=log_data['logId'],
                username=log_data['username'],
                timestamp=log_data['timestamp'],
                summary=log_data['summary'],
                node=log_data['node'],
                details=log_data.get('details', '')
            )
            logs.append(log)
        
        return SecurityAuditLogs(logs)
