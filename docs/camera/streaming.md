# Streaming

## Overview

The C Pro camera system provides real-time video streaming through multiple protocols including RTSP, WebRTC, and ONVIF. The streaming subsystem delivers low-latency video to multiple concurrent clients.

## Streaming Architecture

```mermaid
graph TB
    Cam[Camera Source] --> Pipeline[GStreamer Pipeline]
    Pipeline --> Encoder[H264 Encoder]
    
    Encoder --> RTSP[RTSP Server]
    Encoder --> WebRTC[WebRTC Server]
    Encoder --> ONVIF[ONVIF Stream]
    
    RTSP --> Client1[RTSP Clients]
    WebRTC --> Client2[Web Browsers]
    ONVIF --> Client3[ONVIF Clients]
    
    style Pipeline fill:#e1f5ff,stroke:#333,stroke-width:2px
    style Encoder fill:#ffcccc,stroke:#333,stroke-width:3px
```

## RTSP Streaming

### RTSP Server

```nim
# src/state/rc_rtsp.nim
proc initRtspServer*() =
  initObservable("rtspEnabled",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %true
  )
  
  initObservable("rtspPort",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %8554,
    validateType = Int
  )
  
  initObservable("rtspPath",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {},
    default = %"/stream1"
  )
```

### Stream Endpoints

**Primary Stream**:
```
rtsp://[hostname]:8554/stream1
```

**Secondary Stream** (lower quality):
```
rtsp://[hostname]:8554/stream2
```

**Authentication Required**:
```
rtsp://username:password@[hostname]:8554/stream1
```

### GStreamer RTSP Pipeline

```nim
# src/camserver/streamer.nim
proc createRtspPipeline*(config: StreamConfig): string =
  result = fmt"""
    v4l2src device={config.device} !
    video/x-raw,format=NV12,width={config.width},height={config.height},framerate={config.fps}/1 !
    v4l2h264enc extra-controls="controls,video_bitrate={config.bitrate}" !
    h264parse !
    rtph264pay name=pay0 pt=96
  """
```

### Stream Configuration

```json
{
  "rtsp": {
    "enabled": true,
    "port": 8554,
    "streams": [
      {
        "path": "/stream1",
        "resolution": "1920x1080",
        "fps": 60,
        "bitrate": 8000000,
        "profile": "high"
      },
      {
        "path": "/stream2",
        "resolution": "1280x720",
        "fps": 30,
        "bitrate": 4000000,
        "profile": "main"
      }
    ]
  }
}
```

## WebRTC Streaming

### WebRTC Server

```nim
# src/state/rc_webrtc.nim
proc initWebRtc*() =
  initObservable("webrtcEnabled",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %false  # Disabled by default
  )
  
  initObservable("webrtcIceServers",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %[
      {"urls": ["stun:stun.l.google.com:19302"]}
    ]
  )
```

### WebRTC Pipeline

```javascript
// Browser-side WebRTC client
const pc = new RTCPeerConnection({
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' }
    ]
});

// Request video stream
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

// Send offer to server
const response = await fetch('/api/webrtc/offer', {
    method: 'POST',
    body: JSON.stringify(offer)
});

const answer = await response.json();
await pc.setRemoteDescription(answer);

// Receive video track
pc.ontrack = (event) => {
    videoElement.srcObject = event.streams[0];
};
```

### Server-Side Implementation

```nim
proc handleWebRtcOffer*(offer: JsonNode): JsonNode =
  # Create GStreamer WebRTC pipeline
  let pipeline = fmt"""
    v4l2src device=/dev/video0 !
    video/x-raw,format=NV12,width=1920,height=1080 !
    v4l2h264enc !
    h264parse !
    rtph264pay !
    webrtcbin name=webrtc
  """
  
  # Process SDP offer and create answer
  let answer = createWebRtcAnswer(pipeline, offer)
  return answer
```

## Stream Settings

### Resolution and Framerates

```nim
# src/state/rc_stream_settings.nim
proc initStreamSettings*() =
  initObservable("streamResolution",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %"1920x1080",
    validateType = String
  )
  
  initObservable("streamFramerate",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %60,
    validateType = Int
  )
  
  initObservable("streamBitrate",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %8000000,  # 8 Mbps
    validateType = Int
  )
```

### Encoding Settings

```nim
initObservable("videoEncoder",
  permissionRead = {Media_r, Media_rw},
  permissionWrite = {Media_rw},
  default = %"h264",  # h264, h265, mjpeg
  validateType = String
)

initObservable("encoderProfile",
  permissionRead = {Media_r, Media_rw},
  permissionWrite = {Media_rw},
  default = %"high",  # baseline, main, high
  validateType = String
)

initObservable("encoderPreset",
  permissionRead = {Media_r, Media_rw},
  permissionWrite = {Media_rw},
  default = %"fast",  # ultrafast, fast, medium, slow
  validateType = String
)
```

## Stream Alignment

### Multi-Camera Synchronization

```nim
# src/state/rc_stream_alignment.nim
proc initStreamAlignment*() =
  initObservable("streamAlignment",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %{
      "enabled": true,
      "method": "timestamp",  # timestamp, hardware, software
      "maxLatencyMs": 100,
      "syncTolerance": 33  # ~1 frame at 30fps
    }
  )
```

### Timestamp Synchronization

```c
// src/camserver/nv12Timestamp.c
void add_timestamp_overlay(uint8_t* frame, int width, int height, int64_t pts) {
    // Render timestamp onto NV12 frame
    char timestamp[32];
    format_timestamp(timestamp, pts);
    
    // Draw text at specified position
    draw_text_nv12(frame, width, height, 10, 10, timestamp);
}
```

## Picture-in-Picture (PIP)

### PIP Configuration

```nim
# src/state/rc_pip.nim
proc initPip*() =
  initObservable("pipEnabled",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %false
  )
  
  initObservable("pipLayout",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %{
      "mainSource": "primary",
      "pipSource": "secondary",
      "pipPosition": "bottom-right",
      "pipScale": 0.25,  # 25% of main
      "pipBorder": true
    }
  )
```

### PIP Pipeline

```nim
proc createPipPipeline*(): string =
  result = """
    compositor name=comp
      sink_0::xpos=0 sink_0::ypos=0 sink_0::width=1920 sink_0::height=1080
      sink_1::xpos=1440 sink_1::ypos=810 sink_1::width=480 sink_1::height=270
      sink_1::zorder=1 !
    video/x-raw,width=1920,height=1080 !
    v4l2h264enc !
    h264parse !
    rtph264pay name=pay0
    
    v4l2src device=/dev/video0 ! comp.sink_0
    v4l2src device=/dev/video1 ! videoscale ! video/x-raw,width=480,height=270 ! comp.sink_1
  """
```

## Adaptive Bitrate

### Dynamic Bitrate Adjustment

```nim
proc adjustBitrate*(networkStats: NetworkStats) =
  let currentBitrate = State.get("streamBitrate").value.getInt
  
  if networkStats.packetLoss > 0.05:
    # High packet loss - reduce bitrate
    let newBitrate = (currentBitrate * 0.8).int
    State.get("streamBitrate").updateValue(%newBitrate)
  
  elif networkStats.availableBandwidth > currentBitrate * 1.5:
    # Bandwidth available - increase bitrate
    let newBitrate = min((currentBitrate * 1.2).int, 12000000)
    State.get("streamBitrate").updateValue(%newBitrate)
```

### Network Statistics

```nim
type
  NetworkStats* = object
    availableBandwidth*: int64  # bits per second
    packetLoss*: float          # 0.0 to 1.0
    rtt*: int                   # milliseconds
    jitter*: int                # milliseconds

proc collectNetworkStats*(): NetworkStats =
  # Collect from RTCP feedback
  result.packetLoss = getRtcpPacketLoss()
  result.rtt = getRtcpRtt()
  result.jitter = getRtcpJitter()
  result.availableBandwidth = estimateBandwidth()
```

## Client Streaming Examples

### VLC Player

```bash
# Stream via RTSP
vlc rtsp://username:password@rotoclear.local:8554/stream1

# With custom options
vlc rtsp://rotoclear.local:8554/stream1 \
  --network-caching=300 \
  --rtsp-tcp
```

### FFmpeg

```bash
# View stream
ffmpeg -rtsp_transport tcp \
  -i rtsp://rotoclear.local:8554/stream1 \
  -f sdl "C Pro Stream"

# Save stream to file
ffmpeg -rtsp_transport tcp \
  -i rtsp://rotoclear.local:8554/stream1 \
  -c copy output.mp4

# Re-stream to another RTSP server
ffmpeg -rtsp_transport tcp \
  -i rtsp://rotoclear.local:8554/stream1 \
  -c copy -f rtsp rtsp://destination:8554/stream
```

### GStreamer

```bash
# Play stream
gst-launch-1.0 rtspsrc location=rtsp://rotoclear.local:8554/stream1 ! \
  rtph264depay ! h264parse ! avdec_h264 ! autovideosink

# Record stream
gst-launch-1.0 rtspsrc location=rtsp://rotoclear.local:8554/stream1 ! \
  rtph264depay ! h264parse ! mp4mux ! filesink location=output.mp4
```

### Python Client

```python
import cv2

# Open RTSP stream
cap = cv2.VideoCapture('rtsp://username:password@rotoclear.local:8554/stream1')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Display frame
    cv2.imshow('C Pro Stream', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## Performance Tuning

### Latency Optimization

**Hardware Encoding**:
```nim
# Use hardware encoder for lower latency
let encoder = when defined(embeddedSystem):
  "v4l2h264enc"
else:
  "x264enc tune=zerolatency"
```

**Buffer Tuning**:
```nim
# Reduce buffering for lower latency
initObservable("streamLatencyMode",
  default = %"low",  # low, normal, high
)

proc getLatencyMs*(mode: string): int =
  case mode:
  of "low": 100
  of "normal": 500
  of "high": 2000
  else: 500
```

### Bandwidth Management

```nim
proc calculateOptimalBitrate*(resolution: string, fps: int): int =
  # Bitrate calculation based on resolution and FPS
  case resolution:
  of "3840x2160": 12000000 * (fps div 30)
  of "1920x1080": 8000000 * (fps div 30)
  of "1280x720": 4000000 * (fps div 30)
  of "640x480": 2000000 * (fps div 30)
  else: 4000000
```

## Monitoring and Analytics

### Stream Statistics

```nim
type
  StreamStats* = object
    clientCount*: int
    totalBytesStreamed*: int64
    currentBitrate*: int
    frameDrops*: int
    errors*: int
    uptime*: int64

proc getStreamStats*(): StreamStats =
  result.clientCount = getRtspClientCount()
  result.totalBytesStreamed = getTotalBytesSent()
  result.currentBitrate = getCurrentBitrate()
  result.frameDrops = getFrameDropCount()
  result.errors = getErrorCount()
  result.uptime = getStreamUptime()
```

### Health Checks

```nim
proc checkStreamHealth*(): bool =
  # Verify stream is healthy
  let stats = getStreamStats()
  
  if stats.frameDrops > 100:
    StateLogger.warn("High frame drop rate detected")
    return false
  
  if stats.errors > 10:
    StateLogger.error("Stream errors detected")
    return false
  
  if stats.currentBitrate == 0 and stats.clientCount > 0:
    StateLogger.error("Stream stalled")
    return false
  
  return true
```

## Troubleshooting

### No Stream Available

**Symptoms**: RTSP connection fails or no video displayed.

**Solutions**:
- Verify RTSP server is running: `curl rtsp://localhost:8554/stream1`
- Check firewall rules: `sudo ufw status`
- Test with VLC or FFmpeg
- Review stream logs: `journalctl -u rotordream | grep rtsp`

### High Latency

**Symptoms**: Significant delay between camera and display.

**Solutions**:
- Enable hardware encoding
- Reduce bitrate
- Use TCP instead of UDP for RTSP
- Decrease buffer sizes
- Use lower resolution/framerate

### Choppy Video

**Symptoms**: Video stutters or has dropped frames.

**Solutions**:
- Increase bitrate
- Check network bandwidth
- Verify camera is providing consistent FPS
- Monitor CPU usage
- Check for disk I/O bottlenecks

### Stream Freezes

**Symptoms**: Video stops updating but connection remains.

**Solutions**:
- Check encoder health
- Verify camera device is responsive
- Review system resource usage
- Check for timeout issues
- Restart streaming service

## Related Documentation

- [Hardware Interface](hardware-interface.md)
- [Recording](recording.md)
- [RTSP API](../api/rtsp-streaming.md)
- [Camera Pipeline](../architecture/camera-pipeline.md)
