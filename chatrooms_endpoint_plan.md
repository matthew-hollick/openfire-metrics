# Chatrooms Endpoint Implementation Plan

## Overview
Implement a monitoring tool for OpenFire chatrooms that can retrieve and display information about chat rooms and their occupants.

## Requirements
1. Retrieve list of all chatrooms with detailed information
2. Retrieve occupants for a specific chatroom
3. Support both JSON and text output formats
4. Command-line interface with authentication options
5. Read-only functionality (no create/update/delete operations)

## Data Models Needed
1. `MUCRoomEntity` - Already exists in `openfire_api/chatrooms.py`
2. `OccupantEntity` - Already exists in `openfire_api/chatrooms.py`

## API Endpoints to Implement
1. `GET /chatrooms` - List all chatrooms
2. `GET /chatrooms/{roomName}/occupants` - List occupants in a specific room

## Tool Features
1. Display chatroom information including:
   - Room name and description
   - Creation and modification dates
   - Room settings (persistent, public, members-only, etc.)
   - Owners, admins, and members lists
2. Display occupant information including:
   - JID
   - User address
   - Role and affiliation
3. Support filtering options:
   - By service name
   - By room type (all/public)
   - By search term
4. Support retrieving occupants for a specific room

## Implementation Steps
1. Create `chatrooms_tool.py` with command-line interface
2. Implement functions to retrieve and format chatrooms data
3. Implement functions to retrieve and format occupants data
4. Add output formatting for both JSON and text
5. Test the tool with actual OpenFire instance

## Output Format Examples

### JSON Format
```json
{
  "chatRooms": [
    {
      "roomName": "example-room",
      "naturalName": "Example Room",
      "description": "An example chat room",
      "creationDate": 1754428361544,
      "persistent": true,
      "publicRoom": true,
      "membersOnly": false,
      "owners": ["admin@example.com"],
      "admins": [],
      "members": [],
      "occupants": [
        {
          "jid": "example-room@conference.example.com/user1",
          "userAddress": "user1@example.com/Spark",
          "role": "participant",
          "affiliation": "none"
        }
      ]
    }
  ]
}
```

### Text Format
```
Found 1 chatrooms:
  example-room (Example Room)
    Description: An example chat room
    Persistent: True
    Public: True
    Members-only: False
    Creation Date: 2025-08-22 12:00:00
    
    Owners (1):
      admin@example.com
    Admins: None
    Members: None
    
    Occupants (1):
      jid: example-room@conference.example.com/user1
      user: user1@example.com/Spark
      role: participant
      affiliation: none
```

## Testing
1. Test with actual OpenFire instance
2. Verify both JSON and text output formats
3. Test error handling for invalid room names
4. Test filtering options
