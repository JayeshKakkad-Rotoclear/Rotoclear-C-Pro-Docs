# Testing Strategy

**Comprehensive testing approach for the Rotoclear Camera Server.**

## Testing Overview

The testing strategy covers unit testing, integration testing, and manual verification across multiple components including camera hardware, API endpoints, and system integration.

## Test Structure

### Test Directory Organization
```
tests/
├── test_api.nim           # API endpoint testing
├── test_websocket.nim     # WebSocket communication
├── test_hostname.nim      # Network configuration
├── test_ntp.nim          # Time synchronization
├── test_observer.nim     # Observable pattern
├── test_smb_connection.nim # Network storage
├── testAvi.nim           # Video recording
├── testJpeg.nim          # Image capture
└── onvifC2/              # ONVIF protocol tests
```

## Unit Testing

### Test Execution

**Run All Tests:**
```bash
# Execute test suite
find tests/ -name "test_*.nim" -exec nim c -r {} \;
```

**Run Specific Tests:**
```bash
# API tests
nim c -r tests/test_api.nim

# WebSocket tests  
nim c -r tests/test_websocket.nim

# Camera tests
nim c -r tests/testJpeg.nim
nim c -r tests/testAvi.nim
```

### API Testing (from `tests/test_api.nim`)

**WebSocket API Test:**
```nim
import corun/net/websocket

const
  rotoclearIp = "127.0.0.1" 
  rotoclearApiPort = "3000" 
  apiToken = "1a2B3c4D5e6f7G8h"
  wsUrlWithAuth = fmt("ws://{rotoclearIp}:{rotoclearApiPort}/api?token={apiToken}")

let ws = newWebSocket(wsUrlWithAuth)

ws.onopen += proc() =
  echo("Websocket opened")
  ws.send("""{
    "light0": true,
    "changePostName": "test_recording",
    "record": "start"
  }""")
```

**Test Configuration:**
- **Local Testing**: `127.0.0.1:3000`
- **Remote Testing**: `rotoclear-cam.fritz.box:80`
- **Authentication**: API token `1a2B3c4D5e6f7G8h`

### Observable Pattern Testing (from `tests/test_observer.nim`)

Tests the core state management system:

```nim
# Test observable state changes
# Test notification system
# Test state persistence
# Test concurrent access
```

> TODO: Document specific observable test cases

### Network Testing

**SMB Connection Testing** (`tests/test_smb_connection.nim`):

- Network storage connectivity
- Authentication verification
- File transfer operations

**Hostname Testing** (`tests/test_hostname.nim`):

- Network configuration validation
- DNS resolution testing
- Network interface verification

**NTP Testing** (`tests/test_ntp.nim`):

- Time synchronization verification
- NTP server connectivity
- Clock accuracy testing

## Integration Testing

### Camera Hardware Testing

**JPEG Capture Testing** (`tests/testJpeg.nim`):
```bash
nim c -r tests/testJpeg.nim
```

**Video Recording Testing** (`tests/testAvi.nim`):
```bash
nim c -r tests/testAvi.nim
```

**Test Scenarios:**

- Camera detection and initialization
- Image capture with various settings
- Video recording start/stop
- Quality setting validation
- Error handling for missing hardware

### Protocol Testing

**ONVIF Protocol Testing** (`tests/onvifC2/`):

- ONVIF service discovery
- Camera control via ONVIF
- Standards compliance verification

**WebSocket Protocol Testing** (`tests/test_websocket.nim`):

- Connection establishment
- Message exchange
- Authentication flow
- Error handling
- Connection recovery

## Manual Testing

### API Client Testing

**Python Client Testing:**
```bash
cd apiClients/
python3 example.py
python3 example2.py
```

**JavaScript Client Testing:**
```bash
cd apiClients/
node exampleInfo.js
node nodejsExample.js
```

**C# Client Testing:**
```bash
cd apiClients/csharpExample/
dotnet run
```

### Browser Testing

**WebSocket Browser Testing:**
```javascript
// Browser DevTools Console
const ws = new WebSocket("ws://localhost:3000/api?token=1a2B3c4D5e6f7G8h");
ws.onmessage = (e) => console.log(JSON.parse(e.data));
ws.send(JSON.stringify({"light0": true}));
```

**HTTP Endpoint Testing:**
```bash
# Image capture
curl "http://localhost:3000/camera.jpeg?token=1a2B3c4D5e6f7G8h" -o test.jpg

# System status
curl "http://localhost:3000/status?token=1a2B3c4D5e6f7G8h"
```

## Test Environments

### Local Development Testing

**Configuration:**
```json
{
  "httpOn": true,
  "httpsOn": false,
  "httpPort": 3000,
  "httpsPort": 3001,
  "discRotation": false
}
```

**Test Commands:**
```bash
# Start test server
nim c -r rotordream.nim

# Run API tests
nim c -r tests/test_api.nim

# Test camera functionality (requires hardware)
nim c -r tests/testJpeg.nim
```

### Remote Device Testing

**Remote Test Execution:**
```bash
nim c -r tools/remoteTest.nim
```

**Manual Remote Testing:**
```bash
# SSH to device
ssh root@$C3_BOX_IP

# Check service status
systemctl status rotoclear_server

# View logs
tail -f /media/data/logs/rotoclear.log

# Test API
curl "http://localhost/api/status"
```

## Test Data and Fixtures

### Test Media

**Sample Images:**

- `simulator_data/c-basic-start.jpg` - Test image for camera simulation
- `apiClients/currentImage.jpeg` - Reference image for comparison

**Test Videos:**

- `simulator_data/Video_18_Nov_2021_11-29-04.avi` - Sample recording for playback testing

### Test Configuration

**Test Environment Variables:**
```bash
export ROTOCLEAR_TEST_MODE=true
export ROTOCLEAR_MOCK_CAMERA=true
export ROTOCLEAR_TEST_API_TOKEN="test_token_123"
```

## Performance Testing

### Load Testing

**WebSocket Connection Load:**
```bash
# Multiple concurrent connections
for i in {1..10}; do
  wscat -c "ws://localhost:3000/api?token=1a2B3c4D5e6f7G8h" &
done
```

**HTTP Endpoint Load:**
```bash
# Concurrent image requests
for i in {1..20}; do
  curl "http://localhost:3000/camera.jpeg?token=1a2B3c4D5e6f7G8h" -o "test_$i.jpg" &
done
```

### Memory Testing

**Memory Leak Detection:**
```bash
# Run with memory profiling
nim c -r -d:memProfiler rotordream.nim

# Monitor memory usage
valgrind --tool=memcheck ./rotordream
```

### Stress Testing

**Rapid Command Testing:**
```python
# Rapid WebSocket commands
import websocket
import json
import time

ws = websocket.create_connection("ws://localhost:3000/api?token=1a2B3c4D5e6f7G8h")

for i in range(1000):
    ws.send(json.dumps({"light0": i % 2 == 0}))
    time.sleep(0.01)
```

## Hardware-in-the-Loop Testing

### Camera Testing

**Required Hardware:**

- V4L2 compatible cameras
- Multiple camera heads
- LED lighting systems
- Rotation motors (if applicable)

**Test Scenarios:**

1. **Camera Detection**: Verify all connected cameras are detected
2. **Image Capture**: Test various resolutions and quality settings
3. **Video Recording**: Test different codecs and frame rates
4. **Light Control**: Verify LED control functionality
5. **Sensor Selection**: Test camera head sensor switching

### Environmental Testing

**Network Conditions:**

- Test with various network latencies
- Verify behavior with network interruptions
- Test bandwidth limitations

**Storage Testing:**

- Local storage capacity limits
- Network storage connectivity
- Storage failover scenarios

## Automated Testing

### VS Code Integration

Use VS Code tasks for common test scenarios:

**Test Tasks:**

- `test-api`: Run API test suite
- `test-camera`: Run camera hardware tests
- `test-remote`: Execute remote device tests

## Test Coverage

### Coverage Analysis

```bash
# Generate coverage report
nim c -r --coverage tests/test_all.nim
```

### Coverage Targets

| Component | Target Coverage | Current |
|-----------|----------------|---------|
| API Layer | 90% | > TODO |
| State Management | 85% | > TODO |
| Camera Interface | 70% | > TODO |
| Network Layer | 80% | > TODO |

## Debugging and Diagnostics

### Debug Mode Testing

```bash
# Enable debug logging
nim c -r -d:RuntimeCallDebug=true rotordream.nim

# Verbose compilation
nim c -r --verbosity:3 tests/test_api.nim
```

### Log Analysis

**Test Logs Location:**

- Development: `./logs/`
- Production: `/media/data/logs/`

**Log Levels:**

- `Debug`: Detailed execution flow
- `Info`: General information
- `Warn`: Potential issues
- `Error`: Error conditions

## Best Practices

### Test Development

1. **Isolated Tests**: Each test should be independent
2. **Mock Hardware**: Use mocks for hardware-dependent tests
3. **Clear Assertions**: Use descriptive test assertions
4. **Cleanup**: Ensure tests clean up resources
5. **Documentation**: Document test purpose and expected behavior

### Test Execution

1. **Pre-commit Testing**: Run critical tests before commits
2. **Environment Consistency**: Use consistent test environments
3. **Test Data Management**: Maintain clean test data sets
4. **Error Reporting**: Capture and report test failures clearly

### Hardware Testing

1. **Safety First**: Ensure safe camera operation during tests
2. **Hardware State**: Reset hardware to known state before tests
3. **Error Recovery**: Test error recovery scenarios
4. **Performance Limits**: Test within hardware performance limits

## Troubleshooting Test Issues

### Common Test Failures

**WebSocket Connection Failed:**
```bash
# Check if server is running
netstat -tlnp | grep :3000

# Verify API token
echo "1a2B3c4D5e6f7G8h" | base64
```

**Camera Tests Fail:**
```bash
# Check camera permissions
ls -l /dev/video*
groups $USER

# Verify V4L2 support
v4l2-ctl --list-devices
```

**Network Tests Fail:**
```bash
# Check network connectivity
ping rotoclear-cam.local

# Verify DNS resolution
nslookup rotoclear-cam.local
```

## Related Documentation

- [API Reference](../api/README.md) - API testing details
- [Getting Started](../getting-started.md) - Development setup
- [Build and Deploy](../operations/build-and-deploy.md) - Deployment testing

---

*Testing documentation derived from `tests/` directory analysis and `apiClients/` examples*
