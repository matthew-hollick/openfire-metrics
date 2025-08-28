"""
OpenFire API Sessions Module

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0

This module provides functionality for interacting with the OpenFire sessions endpoint.
"""

from typing import Optional, List
from .client import OpenFireAPIClient


class SessionEntity:
    """Represents a session entity."""
    
    def __init__(self, session_id: str, username: str, resource: Optional[str] = None,
                 node: Optional[str] = None, session_status: Optional[str] = None,
                 presence_status: Optional[str] = None, presence_message: Optional[str] = None,
                 priority: Optional[int] = None, host_address: Optional[str] = None,
                 host_name: Optional[str] = None, creation_date: Optional[str] = None,
                 last_action_date: Optional[str] = None, secure: Optional[bool] = None,
                 jid: Optional[str] = None):
        self.session_id = session_id
        self.username = username
        self.resource = resource
        self.node = node
        self.session_status = session_status
        self.presence_status = presence_status
        self.presence_message = presence_message
        self.priority = priority
        self.host_address = host_address
        self.host_name = host_name
        self.creation_date = creation_date
        self.last_action_date = last_action_date
        self.secure = secure
        self.jid = jid


class SessionEntities:
    """Represents a collection of session entities."""
    
    def __init__(self, sessions: List[SessionEntity]):
        self.sessions = sessions


class SessionsAPI:
    """API for interacting with OpenFire sessions."""
    
    def __init__(self, client: OpenFireAPIClient):
        self.client = client
    
    def get_sessions(self) -> SessionEntities:
        """
        Retrieve all live client sessions.
        
        Returns:
            SessionEntities: A collection of session entities
        """
        response = self.client.get('sessions')
        response.raise_for_status()
        
        data = response.json()
        sessions = []
        
        for session_data in data.get('sessions', []):
            session = SessionEntity(
                session_id=session_data['sessionId'],
                username=session_data['username'],
                resource=session_data.get('resource'),
                node=session_data.get('node'),
                session_status=session_data.get('sessionStatus'),
                presence_status=session_data.get('presenceStatus'),
                presence_message=session_data.get('presenceMessage'),
                priority=session_data.get('priority'),
                host_address=session_data.get('hostAddress'),
                host_name=session_data.get('hostName'),
                creation_date=session_data.get('creationDate'),
                last_action_date=session_data.get('lastActionDate'),
                secure=session_data.get('secure'),
                jid=session_data.get('jid')
            )
            sessions.append(session)
        
        return SessionEntities(sessions)
    
    def get_user_sessions(self, username: str) -> SessionEntities:
        """
        Retrieve all live client sessions for a particular user.
        
        Args:
            username: The username for which to return client sessions
            
        Returns:
            SessionEntities: A collection of session entities
        """
        response = self.client.get(f'sessions/{username}')
        response.raise_for_status()
        
        data = response.json()
        sessions = []
        
        for session_data in data.get('sessions', []):
            session = SessionEntity(
                session_id=session_data['sessionId'],
                username=session_data['username'],
                resource=session_data.get('resource'),
                node=session_data.get('node'),
                session_status=session_data.get('sessionStatus'),
                presence_status=session_data.get('presenceStatus'),
                presence_message=session_data.get('presenceMessage'),
                priority=session_data.get('priority'),
                host_address=session_data.get('hostAddress'),
                host_name=session_data.get('hostName'),
                creation_date=session_data.get('creationDate'),
                last_action_date=session_data.get('lastActionDate'),
                secure=session_data.get('secure'),
                jid=session_data.get('jid')
            )
            sessions.append(session)
        
        return SessionEntities(sessions)
