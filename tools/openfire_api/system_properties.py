"""
OpenFire API System Properties Module

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0

This module provides functionality for interacting with the OpenFire system properties endpoint.
"""

from typing import List
from .client import OpenFireAPIClient


class SystemProperty:
    """Represents a system property entity."""
    
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value


class SystemProperties:
    """Represents a collection of system property entities."""
    
    def __init__(self, properties: List[SystemProperty]):
        self.properties = properties


class SystemPropertiesAPI:
    """API for interacting with OpenFire system properties (read-only)."""
    
    def __init__(self, client: OpenFireAPIClient):
        self.client = client
    
    def get_system_properties(self) -> SystemProperties:
        """
        Retrieve all system properties.
        
        Returns:
            SystemProperties: A collection of system property entities
        """
        response = self.client.get('system/properties')
        response.raise_for_status()
        
        data = response.json()
        properties = []
        
        for prop_data in data.get('property', []):
            prop = SystemProperty(
                key=prop_data['key'],
                value=prop_data.get('value', '')
            )
            properties.append(prop)
        
        return SystemProperties(properties)
    
    def get_system_property(self, property_key: str) -> SystemProperty:
        """
        Retrieve a specific system property.
        
        Args:
            property_key: The key of the system property to retrieve
            
        Returns:
            SystemProperty: The system property entity
        """
        response = self.client.get(f'system/properties/{property_key}')
        response.raise_for_status()
        
        data = response.json()
        return SystemProperty(
            key=data['key'],
            value=data.get('value', '')
        )
