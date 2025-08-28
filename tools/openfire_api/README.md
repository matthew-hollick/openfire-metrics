# OpenFire API Modules

This directory contains Python modules for interacting with the OpenFire REST API.

## Licensing

These modules are part of the OpenFire project and are licensed under the Apache License, Version 2.0.

# Copyright 2025 Ignite Realtime Community

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Modules

### API Modules
- `client.py` - OpenFire API client with HTTP request methods
- `users.py` - Users API module
- `sessions.py` - Sessions API module
- `chatrooms.py` - Chatrooms API module
- `groups.py` - Groups API module
- `system_properties.py` - System Properties API module
- `security_audit_log.py` - Security Audit Log API module
- `message_archive.py` - Message Archive API module

### Utility Modules
- `base_tool.py` - Base tool class for CLI tools
- `http_utils.py` - HTTP utilities with connection pooling and SSL verification
- `auth_utils.py` - Authentication utilities for consistent auth handling
- `error_utils.py` - Error handling utilities with custom exceptions
- `cli_utils.py` - CLI utilities for output options
- `cli_args.py` - Consolidated CLI argument handling
- `format_utils.py` - Formatting utilities for JSON and text output

