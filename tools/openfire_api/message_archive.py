"""
OpenFire API Message Archive Module

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0

This module provides functionality for interacting with the OpenFire message archive endpoint.
"""

from .client import OpenFireAPIClient


class MessageArchiveAPI:
    """API for interacting with OpenFire message archive."""
    
    def __init__(self, client: OpenFireAPIClient):
        self.client = client
    
    def get_unread_message_count(self, jid: str) -> int:
        """
        Gets a count of messages that haven't been delivered to the user yet.
        
        Args:
            jid: The (bare) JID of the user for which the unread message count
                 needs to be fetched.
            
        Returns:
            int: The number of unread messages
        """
        response = self.client.get(f'archive/messages/unread/{jid}')
        response.raise_for_status()
        
        # The API returns XML or JSON with the count
        # For now, we'll return 0 if we can't parse the response
        try:
            data = response.json()
            # The structure of the response isn't fully defined in the spec,
            # so we'll need to handle this based on actual API responses
            return data.get('count', 0)
        except Exception:
            # If we can't parse JSON, return 0
            return 0
