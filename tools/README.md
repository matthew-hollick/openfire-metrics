# OpenFire Tools

This directory contains standalone command-line tools to read data from the OpenFire REST API. Each tool can output data in JSON format, as human-readable text, or send it to an HTTP endpoint (eg elastic-agent).

## Available Tools

- `users_tool.py` - Retrieve user information from OpenFire
- `chatrooms_tool.py` - Retrieve chatroom information from OpenFire
- `groups_tool.py` - Retrieve group information from OpenFire
- `system_properties_tool.py` - Retrieve system properties from OpenFire
- `sessions_tool.py` - Retrieve session information from OpenFire
- `security_audit_log_tool.py` - Retrieve security audit logs from OpenFire

## Common Options

All tools support these common command-line options:

- `--url` - OpenFire REST API URL (default: http://localhost:9090/plugins/restapi/v1)
- `--auth-header` - Authorization header value (required)
- `--insecure` - Skip SSL certificate validation
- `--output-format` - Output format (json, text, or http) (default: json)
- `--output-destination` - HTTP endpoint URL for output (required when using http output format)
- `--http-username` - Username for HTTP basic auth
- `--http-password` - Password for HTTP basic auth
- `--http-header` - Custom headers for HTTP requests (format: name:value)

## HTTP Output

All tools can send their output to an HTTP endpoint using the `--output-format http` option along with `--output-destination`. This is useful for integrating with other systems or services.

## Test HTTP Endpoint

The `test_http_endpoint.py` utility is provided for testing the HTTP output functionality of the tools. It creates a simple Flask server that receives and logs POST requests.

### Usage

```bash
python test_http_endpoint.py [OPTIONS]
```

### Options

- `--host` - Host to bind the server to (default: localhost)
- `--port` - Port to bind the server to (default: 8081)
- `--username` - Username for basic authentication
- `--password` - Password for basic authentication
- `--require-auth` - Require authentication for all requests
- `--debug` - Enable debug mode to echo full JSON object received

### Testing HTTP Output

1. Start the test HTTP endpoint:
   ```bash
   python test_http_endpoint.py --port 8081
   ```

2. Use any tool with HTTP output format:
   ```bash
   python users_tool.py --auth-header "your-secret" --output-format http --output-destination http://localhost:8081
   ```

Love and thanks to the Openfire community for the 
