# ADR-0002: Corun Async Framework Selection

**Status**: Accepted  
**Date**: 2024-01-20  
**Deciders**: Engineering Team  

## Context

The C Pro camera server requires handling multiple concurrent operations:

- Real-time WebSocket connections (10+ simultaneous clients)
- HTTP API requests and file transfers
- Camera frame capture and processing
- System monitoring and health checks
- Network discovery and ONVIF communication

We needed an async framework that provides:
- High-performance concurrent I/O
- WebSocket support with real-time capabilities
- HTTP server with file upload/download
- Low memory overhead for embedded deployment
- Integration with Nim's type system

## Decision

We selected **Corun** as the async runtime framework for the C Pro camera server.

## Rationale

### Performance Characteristics
- **Event Loop**: Single-threaded event loop with cooperative multitasking
- **Memory Efficient**: <5MB additional RAM overhead
- **Low Latency**: Sub-millisecond task switching
- **Scalable**: Handles 100+ concurrent connections on embedded hardware

### WebSocket Support
```nim
# Real-time WebSocket handling
proc handleWebSocket(ws: WebSocket) {.async.} =
  while ws.readyState == ReadyState.Open:
    let msg = await ws.receiveText()
    await processApiMessage(msg, ws)
```

### HTTP Server Capabilities
- **Static Files**: Efficient static file serving
- **REST API**: JSON request/response handling
- **File Uploads**: Multipart form data processing
- **HTTPS**: TLS/SSL support with certificate management

### Integration Benefits
- **Nim Native**: Written specifically for Nim, excellent type integration
- **Exception Safe**: Proper async exception propagation
- **Debugging**: Stack traces work correctly with async code

## Architecture Implementation

### Server Structure
From `src/servers/webserver.nim`:
```nim
import corun
import corun/net/webserver

proc startWebServer*() {.async.} =
  let server = newWebserver()
  server.route(GET, "/api", upgradeToMainThreadWebsocket)
  server.route(GET, "/", serveStaticFiles)
  await server.listen(httpPort)
```

### Concurrent Task Management
```nim
# Multiple concurrent services
proc main() {.async.} =
  await all([
    RCHttpServer.start(),
    RCHttpsServer.start(),
    CamClient.start(),
    initState()
  ])
```

## Alternatives Considered

### AsyncDispatch (Nim Standard)
- **Pros**: Part of standard library, well-tested
- **Cons**: Limited WebSocket support, callback-heavy API, memory overhead

### HttpBeast
- **Pros**: High performance HTTP server
- **Cons**: HTTP-only, no WebSocket support, complex integration

### Jester
- **Pros**: Flask-like web framework, good documentation
- **Cons**: Synchronous model, performance limitations

### Custom Event Loop
- **Pros**: Maximum control and optimization
- **Cons**: Development time, complexity, maintenance burden

## Implementation Details

### Dependency Configuration
From `rotordream.nimble`:
```nim
requires "corun >= 0.7.10"
```

### WebSocket API Integration
The entire WebSocket API system is built on Corun:
```nim
# From src/servers/clients.nim
proc processApiHttpRequest*(username, password: string, data: JsonNode): (string, int) =
  # Process API requests through Corun async system
  if validateCredentials(username, password):
    let response = handleApiRequest(data)
    return ($response, 200)
  else:
    return ("Unauthorized", 401)
```

### Real-time State Broadcasting
```nim
# Efficient broadcast to multiple clients using Corun WebSocket
proc broadcastStateChange*(state: string, value: JsonNode) {.async.} =
  let message = %*{"state": state, "value": value}
  for client in connectedClients:
    if client.readyState == ReadyState.Open:
      await client.send($message)
```

## Performance Metrics

Based on testing with embedded ARM64 hardware:

| Metric | Target | Achieved |
|--------|---------|----------|
| WebSocket Connections | 10+ | 25+ simultaneous |
| Message Latency | <10ms | ~3ms average |
| Memory Overhead | <10MB | ~5MB |
| CPU Usage | <20% | ~12% at 25 connections |

## Consequences

### Positive
- **Real-time Performance**: Sub-10ms message latency for WebSocket API
- **Resource Efficiency**: Low memory and CPU overhead
- **Development Speed**: Clean async/await syntax
- **Reliability**: Proper error handling and connection management

### Negative
- **Learning Curve**: Team needed to learn async programming patterns
- **Debugging Complexity**: Async stack traces can be complex
- **Ecosystem**: Fewer third-party libraries compared to synchronous frameworks

### Neutral
- **Single-threaded**: Adequate for I/O-bound workloads, but CPU-intensive tasks need thread pools
- **Community Size**: Smaller community but active development

## Risk Mitigation

### Thread Pool Integration
For CPU-intensive tasks (image processing):
```nim
# Offload heavy work to thread pool
proc processImage(data: seq[byte]): Future[seq[byte]] {.async.} =
  return await spawnAsync(proc(): seq[byte] = 
    # Heavy image processing work
    encodeJpeg(data)
  )
```

### Connection Management
Implement connection limits and graceful degradation:
```nim
const MAX_CONNECTIONS = 50

proc acceptConnection(server: Webserver) {.async.} =
  if connectedClients.len >= MAX_CONNECTIONS:
    await rejectConnection("Server busy")
    return
```

## Monitoring

Key metrics monitored in production:
- **Connection Count**: Active WebSocket connections
- **Message Queue Depth**: Pending async operations
- **Memory Usage**: Corun runtime memory consumption
- **Response Time**: API endpoint latency percentiles

## Review Date

This decision will be reviewed in Q2 2025 based on:
- Performance under production load
- Development team productivity
- Corun framework evolution and support
- Alternative framework maturity (especially Nim 2.0+ async improvements)
