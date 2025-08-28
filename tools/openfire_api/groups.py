"""
OpenFire API Groups Module

# Copyright 2025 Ignite Realtime Community
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0

This module provides functionality for interacting with the OpenFire groups endpoint.
"""

from typing import Optional, List
from .client import OpenFireAPIClient


class GroupEntity:
    """Represents a group entity."""
    
    def __init__(self, name: str, description: Optional[str] = None, 
                 is_shared: Optional[bool] = None, members: Optional[List[str]] = None,
                 admins: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.is_shared = is_shared
        self.members = members or []
        self.admins = admins or []


class GroupEntities:
    """Represents a collection of group entities."""
    
    def __init__(self, groups: List[GroupEntity]):
        self.groups = groups


class GroupsAPI:
    """API for interacting with OpenFire groups."""
    
    def __init__(self, client: OpenFireAPIClient):
        self.client = client
    
    def get_groups(self) -> GroupEntities:
        """
        Retrieve all groups.
        
        Returns:
            GroupEntities: A collection of group entities
        """
        response = self.client.get('groups')
        response.raise_for_status()
        
        data = response.json()
        groups = []
        
        for group_data in data.get('groups', []):
            # Get detailed information for each group to include members and admins
            try:
                detailed_group = self.get_group(group_data['name'])
                group = detailed_group
            except Exception:
                # If we can't get detailed info, fall back to basic info
                group = GroupEntity(
                    name=group_data['name'],
                    description=group_data.get('description'),
                    is_shared=group_data.get('shared'),
                    members=group_data.get('members', []),
                    admins=group_data.get('admins', [])
                )
            groups.append(group)
        
        return GroupEntities(groups)
    
    def get_group(self, group_name: str) -> GroupEntity:
        """
        Retrieve a specific group.
        
        Args:
            group_name: The name of the group to retrieve
            
        Returns:
            GroupEntity: The group entity
        """
        response = self.client.get(f'groups/{group_name}')
        response.raise_for_status()
        
        data = response.json()
        return GroupEntity(
            name=data['name'],
            description=data.get('description'),
            is_shared=data.get('shared'),
            members=data.get('members', []),
            admins=data.get('admins', [])
        )
    
    def create_group(self, group: GroupEntity) -> None:
        """
        Create a new group.
        
        Args:
            group: The group entity to create
        """
        import xml.etree.ElementTree as ET
        
        # Create XML payload
        root = ET.Element('group')
        name_elem = ET.SubElement(root, 'name')
        name_elem.text = group.name
        
        if group.description is not None:
            desc_elem = ET.SubElement(root, 'description')
            desc_elem.text = group.description
            
        if group.is_shared is not None:
            shared_elem = ET.SubElement(root, 'shared')
            shared_elem.text = str(group.is_shared).lower()
        
        xml_data = ET.tostring(root, encoding='utf-8')
        
        response = self.client.post(
            'groups',
            data=xml_data,
            headers={'Content-Type': 'application/xml'}
        )
        response.raise_for_status()
    
    def delete_group(self, group_name: str) -> None:
        """
        Delete a group.
        
        Args:
            group_name: The name of the group to delete
        """
        response = self.client.delete(f'groups/{group_name}')
        response.raise_for_status()
    
    def update_group(self, group_name: str, group: GroupEntity) -> None:
        """
        Update/overwrite a group.
        
        Args:
            group_name: The name of the group to update
            group: The updated group entity
        """
        import xml.etree.ElementTree as ET
        
        # Create XML payload
        root = ET.Element('group')
        name_elem = ET.SubElement(root, 'name')
        name_elem.text = group.name
        
        if group.description is not None:
            desc_elem = ET.SubElement(root, 'description')
            desc_elem.text = group.description
            
        if group.is_shared is not None:
            shared_elem = ET.SubElement(root, 'shared')
            shared_elem.text = str(group.is_shared).lower()
        
        xml_data = ET.tostring(root, encoding='utf-8')
        
        response = self.client.put(
            f'groups/{group_name}',
            data=xml_data,
            headers={'Content-Type': 'application/xml'}
        )
        response.raise_for_status()
