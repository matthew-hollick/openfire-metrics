# Openfire Metrics Exporter

A Python CLI tool that connects to the Openfire REST API and exports data in NDJSON format for Elasticsearch ingestion.

## Features

- Connects to Openfire REST API endpoints
- Supports both basic authentication (username/password) and Authorization header
- Outputs data in JSON or NDJSON format
- Environment variable support for all configuration options
- Predefined endpoints for common Openfire resources

## Installation

This project uses `uv` for dependency management:

```bash
# Install dependencies
uv pip install -r requirements.txt
```

## Usage

```bash
# Basic usage with default users endpoint
python openfire_metrics.py

# Specify a different endpoint
python openfire_metrics.py --endpoint groups

# Use basic authentication
python openfire_metrics.py --username admin --password secret

# Use authorization header
python openfire_metrics.py --auth-header "Bearer your-token-here"

# Output in NDJSON format for Elasticsearch
python openfire_metrics.py --output-format ndjson

# Specify a custom URL
python openfire_metrics.py --url http://localhost:9090/plugins/restapi/v1/sessions

# Iterate through list endpoints and fetch individual items
python openfire_metrics.py --endpoint users --iterate

# Combine iteration with NDJSON output
python openfire_metrics.py --endpoint users --iterate --output-format ndjson

# Enable logging to file with custom path
python openfire_metrics.py --endpoint users --enable-logging --log-path /var/log/openfire

# Combine logging with iteration and NDJSON output
python openfire_metrics.py --endpoint users --iterate --output-format ndjson --enable-logging

# Use security-logs endpoint with time range
python openfire_metrics.py --endpoint security-logs --start-time 1754425310 --end-time 1754428324

# Use security-logs with NDJSON output and logging
python openfire_metrics.py --endpoint security-logs --start-time 1754425310 --output-format ndjson --enable-logging

# Use security-logs with incremental pulling (fetches logs since last timestamp in log file)
python openfire_metrics.py --endpoint security-logs --incremental --enable-logging --output-format ndjson

# Skip SSL certificate validation (useful for self-signed certificates)
python openfire_metrics.py --endpoint users --insecure

# Connect to HTTPS endpoint with self-signed certificate
python openfire_metrics.py --url https://localhost:9091/plugins/restapi/v1/users --auth-header fred --insecure
```

## Environment Variables

All CLI options can be set using environment variables:

- `OPENFIRE_URL` - REST API endpoint URL
- `OPENFIRE_USERNAME` - Username for basic authentication
- `OPENFIRE_PASSWORD` - Password for basic authentication
- `OPENFIRE_AUTH_HEADER` - Authorization header value

Note: The `--insecure` option does not have an environment variable equivalent as it's a security-sensitive flag that should be explicitly set.

## Available Endpoints

- `users` - User information (list)
- `groups` - Group information (list)
- `sessions` - Session information (list)
- `system` - System properties (list)
- `chatrooms` - Chat room information (includes user count when using iteration)
- `user-roster` - User roster information
- `system-properties` - System properties (alias for `system`)
- `security-logs` - Security audit logs (supports `--start-time` and `--end-time` parameters, and incremental pulling with `--incremental`). When using incremental pulling, the tool checks for log files from today and yesterday; if none are found, it pulls the last 24 hours of logs.

## Output Formats

- `json` - Standard JSON output (default)
- `ndjson` - Newline Delimited JSON for Elasticsearch bulk import

## Log Files

When logging is enabled, output files are created with the following naming convention:
`<ENDPOINT_NAME>-<YYYY-MM-DD>.<OUTPUT_FORMAT>`

For example:
- `users-2025-08-05.json`
- `groups-2025-08-05.ndjson`

Log files are created in the specified log path directory (default: `/var/log/openfire-metrics`).

## Example NDJSON Output

When using NDJSON format, the output follows the Elasticsearch bulk import format:

```json
{"index":{"_index":"openfire-metrics"}}
{"username":"alice","email":"alice@example.com","status":"active"}
{"index":{"_index":"openfire-metrics"}}
{"username":"bob","email":"bob@example.com","status":"inactive"}
```

## API Documentation

Swagger API documentation is available at: http://localhost:9090/plugins/restapi/docs/index.html
