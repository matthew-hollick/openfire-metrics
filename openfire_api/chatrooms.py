"""
OpenFire API Chatrooms Module

This module provides functionality for interacting with the OpenFire chatrooms endpoint.
"""

from typing import Optional, List
from .client import OpenFireAPIClient


class MUCRoomEntity:
    """Represents a multi-user chat room entity."""
    
    def __init__(self, room_name: str, description: Optional[str] = None,
                 password: Optional[str] = None, subject: Optional[str] = None,
                 natural_name: Optional[str] = None, max_users: Optional[int] = None,
                 creation_date: Optional[str] = None, modification_date: Optional[str] = None,
                 persistent: Optional[bool] = None, public_room: Optional[bool] = None,
                 registration_enabled: Optional[bool] = None, can_anyone_discover_jid: Optional[bool] = None,
                 can_occupants_change_subject: Optional[bool] = None, can_occupants_invite: Optional[bool] = None,
                 can_change_nickname: Optional[bool] = None, log_enabled: Optional[bool] = None,
                 login_restricted_to_nickname: Optional[bool] = None, members_only: Optional[bool] = None,
                 moderated: Optional[bool] = None, allow_pm: Optional[str] = None,
                 owners: Optional[List[str]] = None, admins: Optional[List[str]] = None,
                 members: Optional[List[str]] = None):
        self.room_name = room_name
        self.description = description
        self.password = password
        self.subject = subject
        self.natural_name = natural_name
        self.max_users = max_users
        self.creation_date = creation_date
        self.modification_date = modification_date
        self.persistent = persistent
        self.public_room = public_room
        self.registration_enabled = registration_enabled
        self.can_anyone_discover_jid = can_anyone_discover_jid
        self.can_occupants_change_subject = can_occupants_change_subject
        self.can_occupants_invite = can_occupants_invite
        self.can_change_nickname = can_change_nickname
        self.log_enabled = log_enabled
        self.login_restricted_to_nickname = login_restricted_to_nickname
        self.members_only = members_only
        self.moderated = moderated
        self.allow_pm = allow_pm
        self.owners = owners or []
        self.admins = admins or []
        self.members = members or []


class MUCRoomEntities:
    """Represents a collection of multi-user chat room entities."""
    
    def __init__(self, chat_rooms: List[MUCRoomEntity]):
        self.chat_rooms = chat_rooms


class OccupantEntity:
    """Represents an occupant in a chat room."""
    
    def __init__(self, jid: str, user_address: Optional[str] = None,
                 role: Optional[str] = None, affiliation: Optional[str] = None):
        self.jid = jid
        self.user_address = user_address
        self.role = role
        self.affiliation = affiliation


class OccupantEntities:
    """Represents a collection of occupant entities."""
    
    def __init__(self, occupants: List[OccupantEntity]):
        self.occupants = occupants


class MUCServiceEntity:
    """Represents a multi-user chat service entity."""
    
    def __init__(self, service_name: str, description: Optional[str] = None,
                 hidden: Optional[bool] = None):
        self.service_name = service_name
        self.description = description
        self.hidden = hidden


class MUCServiceEntities:
    """Represents a collection of multi-user chat service entities."""
    
    def __init__(self, services: List[MUCServiceEntity]):
        self.services = services


class ChatroomsAPI:
    """API for interacting with OpenFire chatrooms."""
    
    def __init__(self, client: OpenFireAPIClient):
        self.client = client
    
    def get_chat_services(self) -> MUCServiceEntities:
        """
        Get a list of all multi-user chat services.
        
        Returns:
            MUCServiceEntities: A collection of chat service entities
        """
        response = self.client.get('chatservices')
        response.raise_for_status()
        
        data = response.json()
        services = []
        
        for service_data in data.get('chatService', []):
            service = MUCServiceEntity(
                service_name=service_data['serviceName'],
                description=service_data.get('description'),
                hidden=service_data.get('hidden')
            )
            services.append(service)
        
        return MUCServiceEntities(services)
    
    def get_chatrooms(self, service_name: Optional[str] = None, 
                      room_type: Optional[str] = None,
                      search: Optional[str] = None) -> MUCRoomEntities:
        """
        Get a list of all multi-user chat rooms of a particular chat room service.
        
        Args:
            service_name: The name of the MUC service for which to return all chat rooms
            room_type: Room type-based filter: 'all' or 'public'
            search: Search/Filter by room name
            
        Returns:
            MUCRoomEntities: A collection of chat room entities
        """
        params = {}
        if service_name:
            params['servicename'] = service_name
        if room_type:
            params['type'] = room_type
        if search:
            params['search'] = search
        
        response = self.client.get('chatrooms', params=params)
        response.raise_for_status()
        
        data = response.json()
        chat_rooms = []
        
        for room_data in data.get('chatRooms', []):
            room = MUCRoomEntity(
                room_name=room_data['roomName'],
                description=room_data.get('description'),
                password=room_data.get('password'),
                subject=room_data.get('subject'),
                natural_name=room_data.get('naturalName'),
                max_users=room_data.get('maxUsers'),
                creation_date=room_data.get('creationDate'),
                modification_date=room_data.get('modificationDate'),
                persistent=room_data.get('persistent'),
                public_room=room_data.get('publicRoom'),
                registration_enabled=room_data.get('registrationEnabled'),
                can_anyone_discover_jid=room_data.get('canAnyoneDiscoverJID'),
                can_occupants_change_subject=room_data.get('canOccupantsChangeSubject'),
                can_occupants_invite=room_data.get('canOccupantsInvite'),
                can_change_nickname=room_data.get('canChangeNickname'),
                log_enabled=room_data.get('logEnabled'),
                login_restricted_to_nickname=room_data.get('loginRestrictedToNickname'),
                members_only=room_data.get('membersOnly'),
                moderated=room_data.get('moderated'),
                allow_pm=room_data.get('allowPM'),
                owners=room_data.get('owners', []),
                admins=room_data.get('admins', []),
                members=room_data.get('members', [])
            )
            chat_rooms.append(room)
        
        return MUCRoomEntities(chat_rooms)
    
    def get_room_occupants(self, room_name: str) -> OccupantEntities:
        """
        Get all occupants of a specific multi-user chat room.
        
        Args:
            room_name: The name of the chat room for which to return occupants
            
        Returns:
            OccupantEntities: A collection of occupant entities
        """
        response = self.client.get(f'chatrooms/{room_name}/occupants')
        response.raise_for_status()
        
        data = response.json()
        occupants = []
        
        for occupant_data in data.get('occupants', []):
            occupant = OccupantEntity(
                jid=occupant_data['jid'],
                user_address=occupant_data.get('userAddress'),
                role=occupant_data.get('role'),
                affiliation=occupant_data.get('affiliation')
            )
            occupants.append(occupant)
        
        return OccupantEntities(occupants)
