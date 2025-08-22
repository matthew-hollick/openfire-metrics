"""
OpenFire API Users Module

This module provides functionality for interacting with the OpenFire users endpoint.
"""

from typing import Optional, List
from .client import OpenFireAPIClient


class UserProperty:
    """Represents a user property."""
    
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value


class UserEntity:
    """Represents a user entity."""
    
    def __init__(self, username: str, name: Optional[str] = None, 
                 email: Optional[str] = None, password: Optional[str] = None,
                 properties: Optional[List[UserProperty]] = None):
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.properties = properties or []


class UserEntities:
    """Represents a collection of user entities."""
    
    def __init__(self, users: List[UserEntity]):
        self.users = users


class UsersAPI:
    """API for interacting with OpenFire users."""
    
    def __init__(self, client: OpenFireAPIClient):
        self.client = client
    
    def get_users(self, search: Optional[str] = None, 
                  property_key: Optional[str] = None,
                  property_value: Optional[str] = None) -> UserEntities:
        """
        Retrieve all users defined in Openfire (with optional filtering).
        
        Args:
            search: Search/Filter by username (wildcard search %String%)
            property_key: Filter by a user property name
            property_value: Filter by user property value (only with property_key)
            
        Returns:
            UserEntities: A collection of user entities
        """
        params = {}
        if search:
            params['search'] = search
        if property_key:
            params['propertyKey'] = property_key
        if property_value and property_key:
            params['propertyValue'] = property_value
        
        response = self.client.get('users', params=params)
        response.raise_for_status()
        
        data = response.json()
        users = []
        
        for user_data in data.get('users', []):
            properties = []
            for prop_data in user_data.get('properties', []):
                properties.append(UserProperty(prop_data['key'], prop_data['value']))
            
            user = UserEntity(
                username=user_data['username'],
                name=user_data.get('name'),
                email=user_data.get('email'),
                properties=properties
            )
            users.append(user)
        
        return UserEntities(users)
    
    def get_user(self, username: str) -> UserEntity:
        """
        Retrieve a specific user by username.
        
        Args:
            username: The username of the user to retrieve
            
        Returns:
            UserEntity: The user entity
        """
        response = self.client.get(f'users/{username}')
        response.raise_for_status()
        
        data = response.json()
        properties = []
        for prop_data in data.get('properties', []):
            properties.append(UserProperty(prop_data['key'], prop_data['value']))
        
        return UserEntity(
            username=data['username'],
            name=data.get('name'),
            email=data.get('email'),
            properties=properties
        )
