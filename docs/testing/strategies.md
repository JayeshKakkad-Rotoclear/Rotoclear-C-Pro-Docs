# Testing Strategies

**Comprehensive testing methodologies and frameworks for C Pro system validation, quality assurance, and continuous integration.**

## Overview

The C Pro testing strategy ensures system reliability, performance, and quality through multiple testing layers including unit tests, integration tests, system tests, and continuous validation.

```mermaid
graph TB
    A[Testing Strategy] --> B{Testing Levels}
    
    B -->|Code| C[Unit Testing]
    B -->|Component| D[Integration Testing]
    B -->|System| E[System Testing]
    B -->|User| F[Acceptance Testing]
    
    C --> C1[Function Tests]
    C --> C2[Module Tests]
    C --> C3[Class Tests]
    C --> C4[API Tests]
    
    D --> D1[Component Integration]
    D --> D2[Service Integration]
    D --> D3[Database Integration]
    D --> D4[External Integration]
    
    E --> E1[Performance Tests]
    E --> E2[Security Tests]
    E --> E3[Compatibility Tests]
    E --> E4[Reliability Tests]
    
    F --> F1[User Acceptance]
    F --> F2[Business Acceptance]
    F --> F3[Operational Acceptance]
    F --> F4[Contract Acceptance]
    
    style A fill:#e1f5ff,stroke:#333,stroke-width:3px
    style B fill:#ffe6e6,stroke:#333,stroke-width:2px
    style C fill:#ccffcc,stroke:#333,stroke-width:2px
    style D fill:#ffffcc,stroke:#333,stroke-width:2px
    style E fill:#ffccff,stroke:#333,stroke-width:2px
    style F fill:#ccffff,stroke:#333,stroke-width:2px
```

## Testing Framework Architecture

### Test Environment Setup

**Docker Test Environment**:
```dockerfile
# Dockerfile.test
FROM nim:1.6.14-alpine

# Install test dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    gstreamer-dev \
    gstreamer-plugins-base-dev \
    v4l-utils-dev \
    ffmpeg-dev \
    sqlite-dev \
    postgresql-dev

# Install Nim testing framework
RUN nimble install -y unittest2 times asynctest mock

# Copy source code
COPY . /app
WORKDIR /app

# Install project dependencies
RUN nimble install -d

# Run tests
CMD ["nimble", "test"]
```

**Test Configuration**:
```nim
# tests/config.nim
import unittest2, os, strutils

const
  TEST_DATA_DIR = "tests/data"
  TEST_OUTPUT_DIR = "tests/output"
  TEST_DATABASE = "tests/test.db"
  TEST_CONFIG_FILE = "tests/test_config.json"

type
  TestEnvironment* = object
    dataDir*: string
    outputDir*: string
    database*: string
    configFile*: string
    cleanup*: bool

proc setupTestEnvironment*(): TestEnvironment =
  ## Setup test environment
  result = TestEnvironment(
    dataDir: TEST_DATA_DIR,
    outputDir: TEST_OUTPUT_DIR,
    database: TEST_DATABASE,
    configFile: TEST_CONFIG_FILE,
    cleanup: true
  )
  
  # Create test directories
  if not dirExists(result.dataDir):
    createDir(result.dataDir)
  if not dirExists(result.outputDir):
    createDir(result.outputDir)

proc cleanupTestEnvironment*(env: TestEnvironment) =
  ## Cleanup test environment
  if env.cleanup:
    if fileExists(env.database):
      removeFile(env.database)
    if dirExists(env.outputDir):
      removeDir(env.outputDir)
```

### Test Suite Organization

**Test Directory Structure**:
```
tests/
├── unit/                    # Unit tests
│   ├── test_camera.nim
│   ├── test_settings.nim
│   ├── test_helpers.nim
│   └── test_state/
├── integration/             # Integration tests
│   ├── test_api.nim
│   ├── test_websocket.nim
│   ├── test_onvif.nim
│   └── test_database.nim
├── system/                  # System tests
│   ├── test_streaming.nim
│   ├── test_recording.nim
│   └── test_performance.nim
├── acceptance/              # Acceptance tests
│   ├── test_user_scenarios.nim
│   └── test_business_rules.nim
├── data/                    # Test data
│   ├── test_images/
│   ├── test_videos/
│   └── test_configs/
├── fixtures/                # Test fixtures
├── mocks/                   # Mock objects
└── utils/                   # Test utilities
```

## Unit Testing

### Camera Module Testing

**Camera Unit Tests**:
```nim
# tests/unit/test_camera.nim
import unittest2, asynctest
import ../../src/camserver/cam
import ../config

suite "Camera Module Tests":
  var env: TestEnvironment
  
  setup:
    env = setupTestEnvironment()
  
  teardown:
    cleanupTestEnvironment(env)
  
  test "Camera initialization":
    let camera = newCamera()
    check camera != nil
    check camera.status == CameraStatus.Disconnected
  
  test "Camera configuration":
    let camera = newCamera()
    let config = CameraConfig(
      devicePath: "/dev/video0",
      resolution: Resolution(width: 1920, height: 1080),
      framerate: 30,
      format: VideoFormat.H264
    )
    
    camera.configure(config)
    check camera.config.resolution.width == 1920
    check camera.config.framerate == 30
  
  asyncTest "Camera streaming":
    let camera = newCamera()
    let config = CameraConfig(
      devicePath: "/dev/video0",
      resolution: Resolution(width: 1280, height: 720),
      framerate: 25
    )
    
    camera.configure(config)
    await camera.start()
    
    check camera.status == CameraStatus.Streaming
    
    # Test frame capture
    let frame = await camera.captureFrame()
    check frame != nil
    check frame.data.len > 0
    
    await camera.stop()
    check camera.status == CameraStatus.Stopped
  
  test "Camera error handling":
    let camera = newCamera()
    
    expect(CameraError):
      camera.configure(CameraConfig(devicePath: "/invalid/path"))
    
    expect(CameraError):
      discard waitFor camera.start()  # Should fail without config
```

### Settings Module Testing

**Settings Unit Tests**:
```nim
# tests/unit/test_settings.nim
import unittest2, json, os
import ../../src/settings
import ../config

suite "Settings Module Tests":
  var env: TestEnvironment
  
  setup:
    env = setupTestEnvironment()
  
  teardown:
    cleanupTestEnvironment(env)
  
  test "Default settings loading":
    let settings = loadDefaultSettings()
    check settings != nil
    check settings.camera.resolution.width > 0
    check settings.network.httpPort > 0
  
  test "Settings file loading":
    # Create test settings file
    let testSettings = %*{
      "camera": {
        "resolution": {"width": 1920, "height": 1080},
        "framerate": 30
      },
      "network": {
        "httpPort": 8080,
        "rtspPort": 554
      }
    }
    
    writeFile(env.configFile, $testSettings)
    
    let settings = loadSettingsFromFile(env.configFile)
    check settings.camera.resolution.width == 1920
    check settings.network.httpPort == 8080
  
  test "Settings validation":
    var settings = Settings()
    settings.camera.resolution.width = -1  # Invalid
    
    let validation = validateSettings(settings)
    check not validation.valid
    check validation.errors.len > 0
  
  test "Settings persistence":
    let originalSettings = loadDefaultSettings()
    originalSettings.camera.resolution.width = 1920
    originalSettings.network.httpPort = 9090
    
    saveSettingsToFile(originalSettings, env.configFile)
    
    let loadedSettings = loadSettingsFromFile(env.configFile)
    check loadedSettings.camera.resolution.width == 1920
    check loadedSettings.network.httpPort == 9090
```

### State Management Testing

**Observable State Tests**:
```nim
# tests/unit/test_state/test_observable.nim
import unittest2, asynctest, json
import ../../../src/state/observable
import ../../config

suite "Observable State Tests":
  var env: TestEnvironment
  
  setup:
    env = setupTestEnvironment()
  
  teardown:
    cleanupTestEnvironment(env)
  
  test "State creation and initialization":
    let state = newObservableState[CameraState]()
    check state != nil
    check state.observers.len == 0
  
  test "Observer registration":
    let state = newObservableState[CameraState]()
    var notificationReceived = false
    
    proc observer(oldState, newState: CameraState) =
      notificationReceived = true
    
    state.addObserver(observer)
    check state.observers.len == 1
  
  asyncTest "State update notification":
    let state = newObservableState[CameraState]()
    var notifications = 0
    var lastState: CameraState
    
    proc observer(oldState, newState: CameraState) =
      notifications.inc
      lastState = newState
    
    state.addObserver(observer)
    
    let newState = CameraState(
      status: CameraStatus.Streaming,
      resolution: Resolution(width: 1920, height: 1080),
      framerate: 30
    )
    
    await state.update(newState)
    
    check notifications == 1
    check lastState.status == CameraStatus.Streaming
  
  test "Multiple observers":
    let state = newObservableState[CameraState]()
    var observer1Called = false
    var observer2Called = false
    
    proc observer1(oldState, newState: CameraState) =
      observer1Called = true
    
    proc observer2(oldState, newState: CameraState) =
      observer2Called = true
    
    state.addObserver(observer1)
    state.addObserver(observer2)
    
    let newState = CameraState(status: CameraStatus.Recording)
    waitFor state.update(newState)
    
    check observer1Called
    check observer2Called
  
  test "Observer removal":
    let state = newObservableState[CameraState]()
    var notificationCount = 0
    
    proc observer(oldState, newState: CameraState) =
      notificationCount.inc
    
    state.addObserver(observer)
    state.removeObserver(observer)
    
    check state.observers.len == 0
    
    let newState = CameraState(status: CameraStatus.Streaming)
    waitFor state.update(newState)
    
    check notificationCount == 0
```

## Integration Testing

### API Integration Tests

**HTTP API Tests**:
```nim
# tests/integration/test_api.nim
import unittest2, asynctest, httpclient, json
import ../../src/servers/httpapi
import ../config

suite "HTTP API Integration Tests":
  var
    env: TestEnvironment
    server: HttpServer
    client: AsyncHttpClient
  
  setup:
    env = setupTestEnvironment()
    server = newHttpServer()
    client = newAsyncHttpClient()
    
    # Start test server
    asyncSpawn server.start("127.0.0.1", 8081)
    await sleepAsync(100)  # Wait for server to start
  
  teardown:
    cleanupTestEnvironment(env)
    server.stop()
    client.close()
  
  asyncTest "GET /api/status":
    let response = await client.get("http://127.0.0.1:8081/api/status")
    check response.code == Http200
    
    let responseData = parseJson(await response.body)
    check responseData.hasKey("status")
    check responseData.hasKey("timestamp")
  
  asyncTest "GET /api/camera/info":
    let response = await client.get("http://127.0.0.1:8081/api/camera/info")
    check response.code == Http200
    
    let cameraInfo = parseJson(await response.body)
    check cameraInfo.hasKey("device")
    check cameraInfo.hasKey("capabilities")
    check cameraInfo.hasKey("current_settings")
  
  asyncTest "PUT /api/camera/settings":
    let settings = %*{
      "resolution": {"width": 1280, "height": 720},
      "framerate": 25,
      "quality": 80
    }
    
    let response = await client.put(
      "http://127.0.0.1:8081/api/camera/settings",
      body = $settings
    )
    check response.code == Http200
    
    # Verify settings were applied
    let getResponse = await client.get("http://127.0.0.1:8081/api/camera/settings")
    let appliedSettings = parseJson(await getResponse.body)
    check appliedSettings["resolution"]["width"].getInt == 1280
  
  asyncTest "POST /api/camera/snapshot":
    let response = await client.post("http://127.0.0.1:8081/api/camera/snapshot")
    check response.code == Http200
    
    let contentType = response.headers.getOrDefault("content-type")
    check contentType.startsWith("image/")
    
    let imageData = await response.body
    check imageData.len > 0
  
  asyncTest "API authentication":
    # Test without auth token
    let unauthedResponse = await client.get("http://127.0.0.1:8081/api/admin/users")
    check unauthedResponse.code == Http401
    
    # Test with invalid token
    client.headers = newHttpHeaders({"Authorization": "Bearer invalid_token"})
    let invalidResponse = await client.get("http://127.0.0.1:8081/api/admin/users")
    check invalidResponse.code == Http401
    
    # Test with valid token
    client.headers = newHttpHeaders({"Authorization": "Bearer valid_test_token"})
    let validResponse = await client.get("http://127.0.0.1:8081/api/admin/users")
    check validResponse.code == Http200
```

### WebSocket Integration Tests

**WebSocket API Tests**:
```nim
# tests/integration/test_websocket.nim
import unittest2, asynctest, ws, json
import ../../src/servers/websocketApiV1Handler
import ../config

suite "WebSocket Integration Tests":
  var
    env: TestEnvironment
    client: WebSocket
  
  setup:
    env = setupTestEnvironment()
    client = waitFor newWebSocket("ws://127.0.0.1:8080/api/v1/ws")
  
  teardown:
    cleanupTestEnvironment(env)
    if client != nil:
      client.close()
  
  asyncTest "WebSocket connection":
    check client.readyState == Open
  
  asyncTest "Status subscription":
    # Subscribe to status updates
    let subscribeMsg = %*{
      "type": "subscribe",
      "channel": "status",
      "id": "test_subscription"
    }
    
    await client.send($subscribeMsg)
    
    # Wait for subscription confirmation
    let response = await client.receiveStrPacket()
    let responseData = parseJson(response)
    
    check responseData["type"].getStr == "subscription_confirmed"
    check responseData["channel"].getStr == "status"
  
  asyncTest "Camera control via WebSocket":
    # Send camera start command
    let startCmd = %*{
      "type": "command",
      "command": "camera_start",
      "parameters": {
        "resolution": {"width": 1280, "height": 720},
        "framerate": 25
      },
      "id": "start_command"
    }
    
    await client.send($startCmd)
    
    # Wait for command response
    let response = await client.receiveStrPacket()
    let responseData = parseJson(response)
    
    check responseData["type"].getStr == "command_response"
    check responseData["id"].getStr == "start_command"
    check responseData["success"].getBool == true
  
  asyncTest "Real-time status updates":
    # Subscribe to status updates
    let subscribeMsg = %*{
      "type": "subscribe",
      "channel": "status"
    }
    await client.send($subscribeMsg)
    
    # Skip subscription confirmation
    discard await client.receiveStrPacket()
    
    # Trigger status change (mock)
    # In real test, this would be triggered by actual camera state change
    
    # Wait for status update
    let statusUpdate = await client.receiveStrPacket()
    let updateData = parseJson(statusUpdate)
    
    check updateData["type"].getStr == "status_update"
    check updateData.hasKey("data")
```

### Database Integration Tests

**Database Tests**:
```nim
# tests/integration/test_database.nim
import unittest2, asynctest, db_sqlite
import ../../src/database
import ../config

suite "Database Integration Tests":
  var
    env: TestEnvironment
    db: DbConn
  
  setup:
    env = setupTestEnvironment()
    db = open(env.database, "", "", "")
    initializeDatabase(db)
  
  teardown:
    db.close()
    cleanupTestEnvironment(env)
  
  test "Database schema creation":
    # Check if tables exist
    let tables = db.getAllRows(sql"SELECT name FROM sqlite_master WHERE type='table'")
    
    var tableNames: seq[string]
    for row in tables:
      tableNames.add(row[0])
    
    check "users" in tableNames
    check "camera_settings" in tableNames
    check "recordings" in tableNames
    check "events" in tableNames
  
  test "User CRUD operations":
    # Create user
    let userId = db.insertID(sql"""
      INSERT INTO users (username, email, password_hash, role, created_at)
      VALUES (?, ?, ?, ?, datetime('now'))
    """, "testuser", "test@example.com", "hashed_password", "operator")
    
    check userId > 0
    
    # Read user
    let user = db.getRow(sql"SELECT * FROM users WHERE id = ?", userId)
    check user[1] == "testuser"
    check user[2] == "test@example.com"
    
    # Update user
    db.exec(sql"UPDATE users SET email = ? WHERE id = ?", "updated@example.com", userId)
    
    let updatedUser = db.getRow(sql"SELECT email FROM users WHERE id = ?", userId)
    check updatedUser[0] == "updated@example.com"
    
    # Delete user
    db.exec(sql"DELETE FROM users WHERE id = ?", userId)
    
    let deletedUser = db.getRow(sql"SELECT * FROM users WHERE id = ?", userId)
    check deletedUser[0] == ""  # No result
  
  test "Recording storage and retrieval":
    # Insert recording
    let recordingId = db.insertID(sql"""
      INSERT INTO recordings (filename, start_time, end_time, file_size, duration, format)
      VALUES (?, datetime('now'), datetime('now', '+1 hour'), ?, ?, ?)
    """, "test_recording.mp4", 1024000, 3600, "mp4")
    
    # Retrieve recording
    let recording = db.getRow(sql"SELECT * FROM recordings WHERE id = ?", recordingId)
    check recording[1] == "test_recording.mp4"
    check recording[4].parseInt == 1024000
  
  asyncTest "Event logging":
    # Log multiple events
    for i in 1..10:
      db.exec(sql"""
        INSERT INTO events (event_type, description, severity, timestamp)
        VALUES (?, ?, ?, datetime('now'))
      """, "motion_detected", f"Motion detected in zone {i}", "medium")
    
    # Query events
    let events = db.getAllRows(sql"SELECT * FROM events ORDER BY timestamp DESC LIMIT 5")
    check events.len == 5
    
    # Test event filtering
    let motionEvents = db.getAllRows(sql"""
      SELECT * FROM events WHERE event_type = ? AND severity = ?
    """, "motion_detected", "medium")
    check motionEvents.len == 10
```

## System Testing

### Performance Testing

**Performance Test Suite**:
```nim
# tests/system/test_performance.nim
import unittest2, asynctest, times, statistics
import ../../src/camserver/cam
import ../config

suite "Performance Tests":
  var env: TestEnvironment
  
  setup:
    env = setupTestEnvironment()
  
  teardown:
    cleanupTestEnvironment(env)
  
  asyncTest "Frame rate consistency":
    let camera = newCamera()
    let config = CameraConfig(
      devicePath: "/dev/video0",
      resolution: Resolution(width: 1920, height: 1080),
      framerate: 30
    )
    
    camera.configure(config)
    await camera.start()
    
    var frameTimes: seq[float]
    let testDuration = 10.0  # seconds
    let startTime = epochTime()
    
    while epochTime() - startTime < testDuration:
      let frameStart = epochTime()
      let frame = await camera.captureFrame()
      check frame != nil
      
      let frameTime = epochTime() - frameStart
      frameTimes.add(frameTime)
    
    await camera.stop()
    
    # Analyze frame rate consistency
    let avgFrameTime = mean(frameTimes)
    let expectedFrameTime = 1.0 / 30.0  # 30 FPS
    let variance = variance(frameTimes)
    
    echo f"Average frame time: {avgFrameTime:.4f}s"
    echo f"Expected frame time: {expectedFrameTime:.4f}s"
    echo f"Frame time variance: {variance:.6f}"
    
    # Check if frame rate is within acceptable range
    check abs(avgFrameTime - expectedFrameTime) < 0.01
    check variance < 0.001  # Low variance indicates consistent timing
  
  asyncTest "Memory usage stability":
    let camera = newCamera()
    await camera.start()
    
    let initialMemory = getMemoryUsage()
    
    # Capture frames for extended period
    for i in 1..1000:
      let frame = await camera.captureFrame()
      check frame != nil
      
      # Periodic memory check
      if i mod 100 == 0:
        let currentMemory = getMemoryUsage()
        let memoryIncrease = currentMemory - initialMemory
        
        echo f"Memory usage after {i} frames: {currentMemory} bytes"
        echo f"Memory increase: {memoryIncrease} bytes"
        
        # Check for memory leaks
        check memoryIncrease < 10_000_000  # Max 10MB increase
    
    await camera.stop()
  
  asyncTest "Concurrent streaming performance":
    let numStreams = 4
    var cameras: seq[Camera]
    var tasks: seq[Future[void]]
    
    # Setup multiple camera streams
    for i in 1..numStreams:
      let camera = newCamera()
      let config = CameraConfig(
        devicePath: f"/dev/video{i-1}",
        resolution: Resolution(width: 1280, height: 720),
        framerate: 25
      )
      
      camera.configure(config)
      cameras.add(camera)
    
    # Start all cameras concurrently
    let startTime = epochTime()
    for camera in cameras:
      tasks.add(camera.start())
    
    await all(tasks)
    let setupTime = epochTime() - startTime
    
    echo f"Setup time for {numStreams} streams: {setupTime:.2f}s"
    check setupTime < 5.0  # Should setup within 5 seconds
    
    # Test concurrent frame capture
    let captureStartTime = epochTime()
    var captureTasks: seq[Future[Frame]]
    
    for camera in cameras:
      captureTasks.add(camera.captureFrame())
    
    let frames = await all(captureTasks)
    let captureTime = epochTime() - captureStartTime
    
    echo f"Concurrent capture time: {captureTime:.4f}s"
    check captureTime < 1.0  # Should capture all frames within 1 second
    
    # Verify all frames captured successfully
    for frame in frames:
      check frame != nil
      check frame.data.len > 0
    
    # Cleanup
    for camera in cameras:
      await camera.stop()
```

### Streaming Performance Tests

**RTSP Streaming Tests**:
```nim
# tests/system/test_streaming.nim
import unittest2, asynctest, net, strutils
import ../../src/servers/streamer
import ../config

suite "Streaming Performance Tests":
  var env: TestEnvironment
  
  setup:
    env = setupTestEnvironment()
  
  teardown:
    cleanupTestEnvironment(env)
  
  asyncTest "RTSP connection handling":
    let streamer = newRTSPStreamer()
    await streamer.start("0.0.0.0", 554)
    
    # Test multiple concurrent connections
    let numClients = 10
    var clients: seq[Socket]
    
    for i in 1..numClients:
      let client = newSocket()
      client.connect("127.0.0.1", Port(554))
      clients.add(client)
    
    # Send RTSP DESCRIBE requests
    for i, client in clients:
      client.send("DESCRIBE rtsp://127.0.0.1:554/live RTSP/1.0\r\n")
      client.send(f"CSeq: {i}\r\n")
      client.send("User-Agent: Test-Client\r\n\r\n")
    
    # Check responses
    for i, client in clients:
      let response = client.recvLine()
      check response.startsWith("RTSP/1.0 200 OK")
    
    # Cleanup
    for client in clients:
      client.close()
    
    await streamer.stop()
  
  asyncTest "Stream quality under load":
    let streamer = newRTSPStreamer()
    await streamer.start("0.0.0.0", 554)
    
    # Simulate high load
    let numConnections = 50
    var connections: seq[Future[void]]
    
    proc simulateClient(clientId: int): Future[void] {.async.} =
      let client = newSocket()
      try:
        client.connect("127.0.0.1", Port(554))
        
        # RTSP handshake
        client.send("DESCRIBE rtsp://127.0.0.1:554/live RTSP/1.0\r\n")
        client.send(f"CSeq: {clientId}\r\n\r\n")
        
        let response = client.recvLine()
        check response.startsWith("RTSP/1.0")
        
        # Simulate streaming for a short period
        await sleepAsync(1000)
        
      finally:
        client.close()
    
    # Start all client simulations
    for i in 1..numConnections:
      connections.add(simulateClient(i))
    
    # Wait for all clients to complete
    await all(connections)
    
    # Check server is still responsive
    let testClient = newSocket()
    testClient.connect("127.0.0.1", Port(554))
    testClient.send("DESCRIBE rtsp://127.0.0.1:554/live RTSP/1.0\r\n")
    testClient.send("CSeq: 999\r\n\r\n")
    
    let response = testClient.recvLine()
    check response.startsWith("RTSP/1.0 200 OK")
    
    testClient.close()
    await streamer.stop()
```

## Security Testing

### Security Test Suite

**Security Tests**:
```nim
# tests/system/test_security.nim
import unittest2, asynctest, httpclient, json, base64
import ../../src/servers/httpapi
import ../config

suite "Security Tests":
  var
    env: TestEnvironment
    client: AsyncHttpClient
  
  setup:
    env = setupTestEnvironment()
    client = newAsyncHttpClient()
  
  teardown:
    cleanupTestEnvironment(env)
    client.close()
  
  asyncTest "Authentication bypass attempts":
    # Test access without authentication
    let response = await client.get("http://127.0.0.1:8080/api/admin/users")
    check response.code == Http401
    
    # Test with malformed token
    client.headers = newHttpHeaders({"Authorization": "Bearer malformed.token.here"})
    let malformedResponse = await client.get("http://127.0.0.1:8080/api/admin/users")
    check malformedResponse.code == Http401
    
    # Test with expired token
    let expiredToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9"
    client.headers = newHttpHeaders({"Authorization": f"Bearer {expiredToken}"})
    let expiredResponse = await client.get("http://127.0.0.1:8080/api/admin/users")
    check expiredResponse.code == Http401
  
  asyncTest "SQL injection prevention":
    # Test SQL injection in login
    let sqlInjectionPayload = %*{
      "username": "admin'; DROP TABLE users; --",
      "password": "password"
    }
    
    let response = await client.post(
      "http://127.0.0.1:8080/api/auth/login",
      body = $sqlInjectionPayload
    )
    
    # Should not return success or cause server error
    check response.code in [Http400, Http401]
    
    # Verify users table still exists
    let usersResponse = await client.get("http://127.0.0.1:8080/api/admin/users")
    # Should return 401 (unauthorized) not 500 (server error)
    check usersResponse.code == Http401
  
  asyncTest "XSS prevention":
    # Test XSS in user input
    let xssPayload = %*{
      "description": "<script>alert('XSS')</script>",
      "title": "Normal Title"
    }
    
    let response = await client.post(
      "http://127.0.0.1:8080/api/events",
      body = $xssPayload
    )
    
    # Should sanitize input
    if response.code == Http200:
      let responseData = parseJson(await response.body)
      let description = responseData["description"].getStr
      check not description.contains("<script>")
  
  asyncTest "Rate limiting":
    # Test rate limiting on authentication endpoint
    let loginPayload = %*{
      "username": "testuser",
      "password": "wrongpassword"
    }
    
    var responses: seq[AsyncResponse]
    
    # Send many requests quickly
    for i in 1..20:
      let response = await client.post(
        "http://127.0.0.1:8080/api/auth/login",
        body = $loginPayload
      )
      responses.add(response)
    
    # Check if rate limiting kicks in
    var rateLimitedCount = 0
    for response in responses:
      if response.code == Http429:
        rateLimitedCount.inc
    
    check rateLimitedCount > 0  # Some requests should be rate limited
  
  asyncTest "HTTPS redirect":
    # Test HTTP to HTTPS redirect (if configured)
    let httpResponse = await client.get("http://127.0.0.1:8080/api/status")
    
    if httpResponse.code == Http301 or httpResponse.code == Http302:
      let location = httpResponse.headers.getOrDefault("Location")
      check location.startsWith("https://")
```

## Acceptance Testing

### User Acceptance Tests

**User Scenario Tests**:
```nim
# tests/acceptance/test_user_scenarios.nim
import unittest2, asynctest, httpclient, json, ws
import ../config

suite "User Acceptance Tests":
  var
    env: TestEnvironment
    httpClient: AsyncHttpClient
    wsClient: WebSocket
    authToken: string
  
  setup:
    env = setupTestEnvironment()
    httpClient = newAsyncHttpClient()
    
    # Authenticate test user
    let loginResponse = await httpClient.post(
      "http://127.0.0.1:8080/api/auth/login",
      body = $(%*{"username": "testuser", "password": "testpass"})
    )
    
    let loginData = parseJson(await loginResponse.body)
    authToken = loginData["token"].getStr
    
    httpClient.headers = newHttpHeaders({"Authorization": f"Bearer {authToken}"})
    wsClient = waitFor newWebSocket("ws://127.0.0.1:8080/api/v1/ws", headers = httpClient.headers)
  
  teardown:
    cleanupTestEnvironment(env)
    httpClient.close()
    if wsClient != nil:
      wsClient.close()
  
  asyncTest "Complete camera setup workflow":
    # 1. User views current camera status
    let statusResponse = await httpClient.get("http://127.0.0.1:8080/api/camera/status")
    check statusResponse.code == Http200
    
    # 2. User configures camera settings
    let settingsPayload = %*{
      "resolution": {"width": 1920, "height": 1080},
      "framerate": 30,
      "quality": 85,
      "format": "h264"
    }
    
    let configResponse = await httpClient.put(
      "http://127.0.0.1:8080/api/camera/settings",
      body = $settingsPayload
    )
    check configResponse.code == Http200
    
    # 3. User starts streaming
    let startResponse = await httpClient.post("http://127.0.0.1:8080/api/camera/start")
    check startResponse.code == Http200
    
    # 4. User verifies streaming status
    let streamingStatus = await httpClient.get("http://127.0.0.1:8080/api/camera/status")
    let statusData = parseJson(await streamingStatus.body)
    check statusData["status"].getStr == "streaming"
    
    # 5. User captures snapshot
    let snapshotResponse = await httpClient.post("http://127.0.0.1:8080/api/camera/snapshot")
    check snapshotResponse.code == Http200
    check snapshotResponse.headers.getOrDefault("content-type").startsWith("image/")
  
  asyncTest "Live monitoring workflow":
    # 1. User subscribes to live status updates
    let subscribeMsg = %*{
      "type": "subscribe",
      "channel": "status",
      "id": "status_subscription"
    }
    await wsClient.send($subscribeMsg)
    
    # Wait for subscription confirmation
    let confirmMsg = await wsClient.receiveStrPacket()
    let confirmData = parseJson(confirmMsg)
    check confirmData["type"].getStr == "subscription_confirmed"
    
    # 2. User subscribes to event notifications
    let eventSubscribeMsg = %*{
      "type": "subscribe",
      "channel": "events",
      "id": "event_subscription"
    }
    await wsClient.send($eventSubscribeMsg)
    
    # 3. User triggers recording via API
    let recordResponse = await httpClient.post("http://127.0.0.1:8080/api/recording/start")
    check recordResponse.code == Http200
    
    # 4. User should receive real-time status update
    let statusUpdate = await wsClient.receiveStrPacket()
    let updateData = parseJson(statusUpdate)
    check updateData["type"].getStr == "status_update"
    check updateData["data"]["recording"].getBool == true
    
    # 5. User stops recording
    let stopResponse = await httpClient.post("http://127.0.0.1:8080/api/recording/stop")
    check stopResponse.code == Http200
    
    # 6. User should receive recording stopped notification
    let stopUpdate = await wsClient.receiveStrPacket()
    let stopData = parseJson(stopUpdate)
    check stopData["data"]["recording"].getBool == false
  
  asyncTest "User management workflow":
    # Admin user manages other users
    
    # 1. Admin views current users
    let usersResponse = await httpClient.get("http://127.0.0.1:8080/api/admin/users")
    check usersResponse.code == Http200
    
    # 2. Admin creates new user
    let newUserPayload = %*{
      "username": "newoperator",
      "email": "operator@example.com",
      "role": "operator",
      "password": "newuserpass"
    }
    
    let createResponse = await httpClient.post(
      "http://127.0.0.1:8080/api/admin/users",
      body = $newUserPayload
    )
    check createResponse.code == Http201
    
    let createdUser = parseJson(await createResponse.body)
    let userId = createdUser["id"].getInt
    
    # 3. Admin updates user role
    let updatePayload = %*{"role": "viewer"}
    let updateResponse = await httpClient.put(
      f"http://127.0.0.1:8080/api/admin/users/{userId}",
      body = $updatePayload
    )
    check updateResponse.code == Http200
    
    # 4. Admin verifies user update
    let updatedUserResponse = await httpClient.get(f"http://127.0.0.1:8080/api/admin/users/{userId}")
    let updatedUser = parseJson(await updatedUserResponse.body)
    check updatedUser["role"].getStr == "viewer"
    
    # 5. Admin deletes user
    let deleteResponse = await httpClient.delete(f"http://127.0.0.1:8080/api/admin/users/{userId}")
    check deleteResponse.code == Http204
```

## Test Automation

### Continuous Integration Tests

**CI/CD Pipeline Configuration**:
```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Nim
      uses: jiro4989/setup-nim-action@v1
      with:
        nim-version: '1.6.14'
    
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          libgstreamer1.0-dev \
          libgstreamer-plugins-base1.0-dev \
          libv4l-dev \
          ffmpeg \
          sqlite3
        nimble install -d
    
    - name: Run unit tests
      run: nimble test
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: rotordream_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup test environment
      run: |
        docker build -f Dockerfile.test -t rotordream-test .
        docker run --network host -v $PWD:/app rotordream-test nimble integration_test

  system-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup virtual camera
      run: |
        sudo modprobe v4l2loopback devices=1 video_nr=0 card_label="Virtual Camera"
        ffmpeg -f lavfi -i testsrc=duration=60:size=1920x1080:rate=30 -f v4l2 /dev/video0 &
    
    - name: Run system tests
      run: |
        docker build -f Dockerfile.test -t rotordream-test .
        docker run --device=/dev/video0 --network host rotordream-test nimble system_test

  performance-tests:
    runs-on: ubuntu-latest
    needs: system-tests
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run performance benchmarks
      run: |
        docker build -f Dockerfile.test -t rotordream-test .
        docker run --network host rotordream-test nimble performance_test
    
    - name: Upload performance results
      uses: actions/upload-artifact@v3
      with:
        name: performance-results
        path: tests/performance_results.json
```

### Test Data Management

**Test Data Generator**:
```nim
# tests/utils/test_data_generator.nim
import json, random, times, os

proc generateTestImages*(count: int, outputDir: string) =
  ## Generate test images for camera simulation
  createDir(outputDir)
  
  for i in 1..count:
    let filename = f"test_image_{i:04d}.jpg"
    let filepath = outputDir / filename
    
    # Generate using FFmpeg
    let cmd = f"ffmpeg -f lavfi -i testsrc=duration=1:size=1920x1080:rate=1 -vframes 1 -q:v 2 {filepath}"
    discard execShellCmd(cmd)

proc generateTestConfig*(filename: string) =
  ## Generate test configuration file
  let config = %*{
    "camera": {
      "device": "/dev/video0",
      "resolution": {"width": 1920, "height": 1080},
      "framerate": 30,
      "format": "h264"
    },
    "network": {
      "http_port": 8080,
      "rtsp_port": 554,
      "websocket_port": 8081
    },
    "storage": {
      "base_path": "/tmp/recordings",
      "max_size": 1000000000,
      "retention_days": 30
    },
    "authentication": {
      "jwt_secret": "test_secret_key_12345",
      "token_expiry": 3600
    }
  }
  
  writeFile(filename, pretty(config))

proc generateTestUsers*(count: int): seq[JsonNode] =
  ## Generate test user data
  result = @[]
  let roles = ["admin", "operator", "viewer"]
  
  for i in 1..count:
    let user = %*{
      "id": i,
      "username": f"testuser{i}",
      "email": f"user{i}@example.com",
      "role": sample(roles),
      "created_at": $now(),
      "active": true
    }
    result.add(user)

# Test data initialization
when isMainModule:
  echo "Generating test data..."
  
  generateTestImages(100, "tests/data/test_images")
  generateTestConfig("tests/data/test_config.json")
  
  let testUsers = generateTestUsers(50)
  writeFile("tests/data/test_users.json", pretty(%testUsers))
  
  echo "Test data generation complete!"
```

## Related Documentation

- [Build & Deploy](../operations/build-deploy.md) - Deployment testing
- [Monitoring](../operations/monitoring.md) - Test monitoring
- [API Reference](../api/http-api.md) - API testing
- [Performance](../operations/performance.md) - Performance testing

---

*Comprehensive testing strategies covering all aspects of system validation and quality assurance*
