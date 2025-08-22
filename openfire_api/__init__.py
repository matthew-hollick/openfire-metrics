"""
OpenFire API Package

This package provides modules for interacting with the OpenFire REST API.
"""

from .client import OpenFireAPIClient, create_client
from .users import UsersAPI
from .sessions import SessionsAPI, SessionEntity, SessionEntities
from .chatrooms import ChatroomsAPI
from .message_archive import MessageArchiveAPI
from .groups import GroupsAPI, GroupEntity, GroupEntities
from .security_audit_log import SecurityAuditLogAPI, SecurityAuditLog, SecurityAuditLogs

__all__ = [
    'OpenFireAPIClient',
    'create_client',
    'UsersAPI',
    'SessionsAPI',
    'SessionEntity',
    'SessionEntities',
    'ChatroomsAPI',
    'MessageArchiveAPI',
    'GroupsAPI',
    'GroupEntity',
    'GroupEntities',
    'SecurityAuditLogAPI',
    'SecurityAuditLog',
    'SecurityAuditLogs'
]
