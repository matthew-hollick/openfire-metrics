"""
OpenFire API modules package

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0

This package provides modules for interacting with the OpenFire REST API.
"""

# Client and API modules
from .client import OpenFireAPIClient, create_client
from .users import UsersAPI
from .sessions import SessionsAPI, SessionEntity, SessionEntities
from .chatrooms import ChatroomsAPI
from .message_archive import MessageArchiveAPI
from .groups import GroupsAPI, GroupEntity, GroupEntities
from .security_audit_log import SecurityAuditLogAPI, SecurityAuditLog, SecurityAuditLogs
from .system_properties import SystemPropertiesAPI, SystemProperty, SystemProperties

# Utility modules
from .http_utils import make_request, get_verify_option, get_default_headers, send_to_http_endpoint
from .auth_utils import AuthManager, create_auth_manager, get_auth_tuple, get_auth_headers
from .cli_utils import add_standard_output_options, validate_http_options, parse_http_headers
from .format_utils import format_as_json, format_as_text
from .error_utils import (OpenFireAPIError, AuthenticationError, ConnectionError, 
                         ResourceNotFoundError, ValidationError, ServerError,
                         handle_request_error, raise_for_status)

__all__ = [
    # Client and API classes
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
    'SecurityAuditLogs',
    'SystemPropertiesAPI',
    'SystemProperty',
    'SystemProperties',
    
    # HTTP utilities
    'make_request',
    'get_verify_option',
    'get_default_headers',
    'send_to_http_endpoint',
    
    # Authentication utilities
    'AuthManager',
    'create_auth_manager',
    'get_auth_tuple',
    'get_auth_headers',
    
    # CLI utilities
    'add_standard_output_options',
    'validate_http_options',
    'parse_http_headers',
    
    # Formatting utilities
    'format_as_json',
    'format_as_text',
    
    # Error handling
    'OpenFireAPIError',
    'AuthenticationError',
    'ConnectionError',
    'ResourceNotFoundError',
    'ValidationError',
    'ServerError',
    'handle_request_error',
    'raise_for_status'
]
