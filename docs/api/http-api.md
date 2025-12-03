# HTTP REST API Reference

**RESTful endpoints for file operations, camera images, and system management.**

## Base URL and Authentication

**Base URL**: `http://<device-ip>:8080` or `https://<device-ip>:8081`  
**Authentication**: Bearer token or HTTP Basic Auth

```bash
# Bearer token authentication
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" http://192.168.1.100:8080/api/info

# Basic authentication
curl -u "admin:password" http://192.168.1.100:8080/api/info

# Query parameter authentication
curl "http://192.168.1.100:8080/image?token=1a2B3c4D5e6f7G8h"
```

## Camera Endpoints

### Get Current Image
```http
GET /camera.jpeg
GET /image
```

Returns the current camera frame as JPEG image.

**Parameters**:
- `token` (string): API authentication token
- `quality` (int, optional): JPEG quality 1-100, default 85

**Response**: Binary JPEG data  
**Content-Type**: `image/jpeg`

```bash
# Capture current frame
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/camera.jpeg \
     --output current_frame.jpg

# Capture with custom quality
curl "http://192.168.1.100:8080/camera.jpeg?token=1a2B3c4D5e6f7G8h&quality=95" \
     --output high_quality.jpg
```

### Take Snapshot
```http
POST /snapshot
```

Trigger a high-resolution snapshot capture.

**Request Body**:
```json
{
  "filename": "snapshot_001.jpg",
  "quality": 95,
  "addTimestamp": true
}
```

**Response**:
```json
{
  "success": true,
  "filename": "snapshot_001.jpg",
  "path": "/media/data/snapshots/snapshot_001.jpg",
  "size": 2048576,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### Camera Status
```http
GET /api/camera/status
```

Get current camera hardware status.

**Response**:
```json
{
  "cameras": [
    {
      "id": 0,
      "connected": true,
      "device": "/dev/video0",
      "resolution": "1920x1080",
      "framerate": 30,
      "format": "YUYV"
    },
    {
      "id": 1,
      "connected": false,
      "device": "/dev/video1"
    }
  ],
  "active_camera": 0,
  "streaming": true
}
```

## System Information

### Get System Info
```http
GET /api/info
GET /api/status
```

Returns comprehensive system status and configuration.

**Response**:
```json
{
  "version": "1.0.0",
  "build": "2025-01-15T09:00:00Z",
  "uptime": 3600,
  "system": {
    "temperature": 45.2,
    "cpu_usage": 12.5,
    "memory": {
      "total": 4096,
      "available": 2048,
      "used": 2048
    },
    "disk": {
      "total": 32768,
      "available": 16384,
      "used": 16384
    }
  },
  "camera": {
    "connected": true,
    "resolution": "1920x1080",
    "framerate": 30,
    "recording": false
  },
  "network": {
    "ip": "192.168.1.100",
    "hostname": "rotoclear-cam",
    "connected": true
  }
}
```

### Health Check
```http
GET /health
GET /api/health
```

Simple health check endpoint for monitoring.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "checks": {
    "camera": "ok",
    "storage": "ok",
    "network": "ok"
  }
}
```

## File Management

### Upload File
```http
POST /upload
Content-Type: multipart/form-data
```

Upload files to the device storage.

**Parameters**:
- `file`: File data (multipart form field)
- `path`: Target directory (optional)
- `overwrite`: Allow overwriting existing files (optional)

```bash
# Upload configuration file
curl -X POST \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -F "file=@config.json" \
     -F "path=/data/configs/" \
     http://192.168.1.100:8080/upload

# Upload with overwrite
curl -X POST \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -F "file=@firmware.bin" \
     -F "path=/data/firmware/" \
     -F "overwrite=true" \
     http://192.168.1.100:8080/upload
```

**Response**:
```json
{
  "success": true,
  "filename": "config.json",
  "path": "/data/configs/config.json",
  "size": 1024
}
```

### Download File
```http
GET /download/{filepath}
GET /files/{filepath}
```

Download files from device storage.

```bash
# Download recording
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/download/recordings/video1.avi \
     --output video1.avi

# Download with custom filename
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/files/logs/system.log \
     --output system_backup.log
```

### List Files
```http
GET /files?path={directory}
GET /api/files?directory={path}
```

List files and directories in specified path.

**Parameters**:
- `path` or `directory`: Directory path to list
- `recursive`: Include subdirectories (optional)
- `filter`: File extension filter (optional)

```bash
# List recordings directory
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     "http://192.168.1.100:8080/files?path=/media/data/recordings"

# List with filter
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     "http://192.168.1.100:8080/files?path=/media/data&filter=.avi"
```

**Response**:
```json
{
  "path": "/media/data/recordings",
  "files": [
    {
      "name": "recording_001.avi",
      "size": 1048576,
      "modified": "2025-01-15T10:30:00Z",
      "type": "file",
      "mime_type": "video/x-msvideo"
    },
    {
      "name": "snapshots",
      "type": "directory",
      "modified": "2025-01-15T09:00:00Z"
    }
  ],
  "total_size": 2097152,
  "file_count": 1,
  "directory_count": 1
}
```

### Delete File
```http
DELETE /files/{filepath}
```

Delete file or directory from device storage.

```bash
# Delete single file
curl -X DELETE \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/files/recordings/old_video.avi

# Delete directory (requires confirmation)
curl -X DELETE \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     "http://192.168.1.100:8080/files/temp?recursive=true"
```

## Recording Control

### Start Recording
```http
POST /api/recording/start
```

Start video recording with specified parameters.

**Request Body**:
```json
{
  "filename": "experiment_001.avi",
  "duration": 300,
  "quality": "high",
  "resolution": "1920x1080",
  "framerate": 30
}
```

**Response**:
```json
{
  "success": true,
  "recording_id": "rec_12345",
  "filename": "experiment_001.avi",
  "estimated_size": 1073741824
}
```

### Stop Recording
```http
POST /api/recording/stop
```

Stop current video recording.

**Response**:
```json
{
  "success": true,
  "recording_id": "rec_12345", 
  "filename": "experiment_001.avi",
  "duration": 180,
  "file_size": 805306368
}
```

### Recording Status
```http
GET /api/recording/status
```

Get current recording status and information.

**Response**:
```json
{
  "recording": true,
  "recording_id": "rec_12345",
  "filename": "experiment_001.avi",
  "duration": 120,
  "estimated_size": 536870912,
  "remaining_space": 10737418240
}
```

## Configuration

### Get Configuration
```http
GET /api/config
GET /api/config/{section}
```

Retrieve system configuration.

```bash
# Get all configuration
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/api/config

# Get specific section
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/api/config/camera
```

### Update Configuration
```http
PUT /api/config/{section}
PATCH /api/config/{section}
```

Update system configuration section.

**Request Body**:
```json
{
  "camera": {
    "default_resolution": "1920x1080",
    "default_framerate": 30,
    "auto_exposure": true
  }
}
```

## ONVIF Integration

### ONVIF Device Discovery
```http
GET /api/onvif/discover
```

Discover ONVIF cameras on the network.

**Response**:
```json
{
  "devices": [
    {
      "uuid": "urn:uuid:12345678-1234-5678-9abc-123456789abc",
      "name": "IP Camera 1",
      "hardware": "AXIS P1375",
      "location": "192.168.1.200",
      "services": [
        "http://192.168.1.200/onvif/device_service",
        "http://192.168.1.200/onvif/media_service"
      ]
    }
  ]
}
```

### ONVIF Proxy
```http
POST /api/onvif/{device_id}/{service}
Content-Type: application/soap+xml
```

Proxy ONVIF SOAP requests to discovered devices.

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "CAMERA_NOT_CONNECTED",
    "message": "Camera device not available",
    "details": "V4L2 device /dev/video0 not found",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

### HTTP Status Codes

| Status | Meaning | Common Causes |
|--------|---------|---------------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid parameters or request format |
| 401 | Unauthorized | Invalid or missing authentication token |
| 403 | Forbidden | Insufficient permissions for operation |
| 404 | Not Found | Resource or endpoint doesn't exist |
| 409 | Conflict | Resource already exists or in use |
| 413 | Payload Too Large | File upload exceeds size limit |
| 422 | Unprocessable Entity | Valid format but invalid content |
| 500 | Internal Server Error | Server-side error or exception |
| 503 | Service Unavailable | Camera offline or system overloaded |

### Error Codes

| Code | Description |
|------|-------------|
| `CAMERA_NOT_CONNECTED` | Camera hardware not available |
| `INVALID_RESOLUTION` | Unsupported resolution format |
| `INSUFFICIENT_STORAGE` | Not enough disk space |
| `RECORDING_IN_PROGRESS` | Cannot modify settings during recording |
| `INVALID_CREDENTIALS` | Authentication failed |
| `PERMISSION_DENIED` | User lacks required permissions |
| `FILE_NOT_FOUND` | Requested file doesn't exist |
| `INVALID_FORMAT` | Unsupported file format |

## Rate Limiting

API endpoints have the following rate limits per client IP:

- **Image Requests**: 10 requests/second
- **File Operations**: 5 requests/second  
- **API Calls**: 100 requests/second
- **File Uploads**: 2 requests/second

Exceeded limits return HTTP 429 with headers:
```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1642247400
```

## Content Types

### Request Content Types
- `application/json` - API requests
- `multipart/form-data` - File uploads
- `application/x-www-form-urlencoded` - Form data

### Response Content Types
- `application/json` - API responses
- `image/jpeg` - Camera images
- `video/x-msvideo` - AVI video files
- `text/plain` - Log files
- `application/octet-stream` - Binary files

## Related Documentation

- [WebSocket API](websocket-api.md) - Real-time bidirectional API
- [Authentication](../security/authentication.md) - Security and permissions
- [File Management](../operations/monitoring.md) - Storage and file operations
- [API Examples](examples/) - Code examples for integration

---

*HTTP API documentation derived from route handlers in `src/servers/routes/` and client examples*
