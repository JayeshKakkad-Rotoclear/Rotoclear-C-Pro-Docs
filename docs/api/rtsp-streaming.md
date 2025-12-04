# RTSP Streaming Protocol

**Real-time streaming protocol for live video access and camera control.**

## Overview

The RTSP streaming implementation provides H.264 video streams for real-time monitoring and recording applications. Built on GStreamer pipeline with V4L2 hardware acceleration.

```mermaid
graph LR
    A[Camera Device] --> B[V4L2 Driver]
    B --> C[GStreamer Pipeline]
    C --> D[H.264 Encoder]
    D --> E[RTP Packetizer]
    E --> F[RTSP Server]
    F --> G[RTSP Client]
    G --> H[Media Player]
    
    style C fill:#e1f5ff,stroke:#333,stroke-width:2px
    style D fill:#ffcccc,stroke:#333,stroke-width:2px
    style F fill:#ccffcc,stroke:#333,stroke-width:3px
```

## RTSP URLs and Authentication

### Primary Stream URL
```
rtsp://192.168.1.100:554/stream0
rtsp://admin:password@192.168.1.100:554/stream0
rtsp://192.168.1.100:554/stream0?token=1a2B3c4D5e6f7G8h
```

### Secondary Stream (Low Resolution)
```
rtsp://192.168.1.100:554/stream1
rtsp://192.168.1.100:554/stream1?resolution=640x480
```

### Authentication Methods

**Basic Authentication**:
```bash
# VLC media player
vlc rtsp://admin:password@192.168.1.100:554/stream0

# FFmpeg
ffmpeg -i rtsp://admin:password@192.168.1.100:554/stream0 output.mp4

# GStreamer
gst-launch-1.0 rtspsrc location=rtsp://admin:password@192.168.1.100:554/stream0 ! decodebin ! autovideosink
```

**Token Authentication**:
```bash
# Using query parameter
vlc "rtsp://192.168.1.100:554/stream0?token=1a2B3c4D5e6f7G8h"

# Using custom header (application dependent)
ffmpeg -headers "Authorization: Bearer 1a2B3c4D5e6f7G8h" -i rtsp://192.168.1.100:554/stream0 output.mp4
```

## Stream Parameters

### Primary Stream (stream0)
- **Resolution**: 1920×1080 (configurable)
- **Frame Rate**: 30 fps (configurable) 
- **Bitrate**: 4-8 Mbps (adaptive)
- **Codec**: H.264 Main Profile Level 4.0
- **Container**: RTP/RTSP

### Secondary Stream (stream1)  
- **Resolution**: 640×480 (configurable)
- **Frame Rate**: 15 fps (configurable)
- **Bitrate**: 500 Kbps - 2 Mbps
- **Codec**: H.264 Baseline Profile Level 3.1
- **Container**: RTP/RTSP

### Dynamic Parameters
```
rtsp://192.168.1.100:554/stream0?resolution=1280x720&fps=25&bitrate=2000
rtsp://192.168.1.100:554/stream1?resolution=320x240&fps=10
```

## GStreamer Pipeline Architecture

### Source Pipeline (Device Side)
```bash
# Primary high-resolution stream
gst-launch-1.0 \
    v4l2src device=/dev/video0 ! \
    video/x-raw,format=YUY2,width=1920,height=1080,framerate=30/1 ! \
    v4l2h264enc extra-controls="controls,video_bitrate=4000000" ! \
    video/x-h264,profile=main ! \
    rtph264pay config-interval=1 pt=96 ! \
    udpsink host=0.0.0.0 port=5004

# Secondary low-resolution stream  
gst-launch-1.0 \
    v4l2src device=/dev/video0 ! \
    video/x-raw,format=YUY2,width=1920,height=1080,framerate=30/1 ! \
    videoscale ! \
    video/x-raw,width=640,height=480 ! \
    v4l2h264enc extra-controls="controls,video_bitrate=1000000" ! \
    video/x-h264,profile=baseline ! \
    rtph264pay config-interval=1 pt=96 ! \
    udpsink host=0.0.0.0 port=5006
```

### Client Pipeline Examples
```bash
# Receive and display
gst-launch-1.0 \
    rtspsrc location=rtsp://192.168.1.100:554/stream0 ! \
    rtph264depay ! \
    avdec_h264 ! \
    videoconvert ! \
    autovideosink

# Receive and record to file
gst-launch-1.0 \
    rtspsrc location=rtsp://192.168.1.100:554/stream0 ! \
    rtph264depay ! \
    h264parse ! \
    mp4mux ! \
    filesink location=recording.mp4

# Receive with custom buffer settings
gst-launch-1.0 \
    rtspsrc location=rtsp://192.168.1.100:554/stream0 \
             latency=200 buffer-mode=auto ! \
    rtph264depay ! \
    avdec_h264 max-threads=4 ! \
    videoconvert ! \
    autovideosink sync=false
```

## Client Integration Examples

### VLC Media Player
```bash
# Command line
vlc rtsp://admin:password@192.168.1.100:554/stream0

# With custom cache
vlc --network-caching=300 rtsp://admin:password@192.168.1.100:554/stream0

# Transcoding while viewing
vlc rtsp://admin:password@192.168.1.100:554/stream0 \
    --sout "#transcode{vcodec=h264,vb=1024,scale=1}:file{dst=output.mp4}"
```

### FFmpeg Integration
```bash
# Live viewing with FFplay
ffplay -fflags nobuffer -flags low_delay -framedrop \
       rtsp://admin:password@192.168.1.100:554/stream0

# Recording to file
ffmpeg -i rtsp://admin:password@192.168.1.100:554/stream0 \
       -c copy -f mp4 recording.mp4

# Re-streaming to another RTSP server
ffmpeg -i rtsp://admin:password@192.168.1.100:554/stream0 \
       -c copy -f rtsp rtsp://destination-server:554/restream

# Extracting frames at intervals
ffmpeg -i rtsp://admin:password@192.168.1.100:554/stream0 \
       -vf fps=1/10 frame_%03d.jpg
```

### OpenCV Python Integration
```python
import cv2
import numpy as np

# Connect to RTSP stream
rtsp_url = "rtsp://admin:password@192.168.1.100:554/stream0"
cap = cv2.VideoCapture(rtsp_url)

# Configure buffer to reduce latency
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FPS, 30)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Process frame
    cv2.imshow('RTSP Stream', frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### HTML5 Video Integration
```html
<!DOCTYPE html>
<html>
<head>
    <title>RTSP Stream Viewer</title>
</head>
<body>
    <h1>Live Camera Feed</h1>
    
    <!-- Convert RTSP to WebRTC or HLS for browser support -->
    <video id="rtspPlayer" width="1920" height="1080" controls autoplay>
        <source src="http://192.168.1.100:8080/hls/stream0/index.m3u8" type="application/x-mpegURL">
        Your browser does not support the video tag.
    </video>

    <script>
        // Alternative: Use MSE (Media Source Extensions) with WebSocket
        const video = document.getElementById('rtspPlayer');
        
        // Configure for low latency
        video.setAttribute('playsinline', '');
        video.muted = true; // Required for autoplay in many browsers
        
        // Handle stream events
        video.addEventListener('loadstart', () => {
            console.log('Started loading video');
        });
        
        video.addEventListener('canplay', () => {
            console.log('Video ready to play');
            video.play();
        });
    </script>
</body>
</html>
```

## Advanced Configuration

### Adaptive Bitrate Streaming
```ini
# Device configuration file
[rtsp]
adaptive_bitrate = true
max_bitrate = 8000000
min_bitrate = 500000
target_buffer_time = 2.0

[stream_profiles]
profile_high = "resolution=1920x1080,fps=30,bitrate=6000000"
profile_medium = "resolution=1280x720,fps=25,bitrate=3000000"  
profile_low = "resolution=640x480,fps=15,bitrate=1000000"
```

### Quality of Service (QoS)
```bash
# Network QoS configuration for RTSP traffic
# On device (Linux)
tc qdisc add dev eth0 root handle 1: htb default 30
tc class add dev eth0 parent 1: classid 1:1 htb rate 100mbit
tc class add dev eth0 parent 1:1 classid 1:10 htb rate 10mbit ceil 50mbit prio 1
tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip dport 554 0xffff flowid 1:10

# DSCP marking for RTSP packets
iptables -t mangle -A OUTPUT -p tcp --dport 554 -j DSCP --set-dscp 46
iptables -t mangle -A OUTPUT -p udp --dport 5004:5010 -j DSCP --set-dscp 46
```

### Multi-Camera Setup
```yaml
# Configuration for multiple camera streams
cameras:
  - id: 0
    device: "/dev/video0"
    name: "Main Camera"
    streams:
      - url: "rtsp://192.168.1.100:554/camera0/stream0"
        resolution: "1920x1080"
        fps: 30
      - url: "rtsp://192.168.1.100:554/camera0/stream1" 
        resolution: "640x480"
        fps: 15
        
  - id: 1
    device: "/dev/video1"
    name: "Secondary Camera"
    streams:
      - url: "rtsp://192.168.1.100:554/camera1/stream0"
        resolution: "1280x720"
        fps: 25
```

## RTSP Protocol Details

### RTSP Methods Supported
- **DESCRIBE**: Get media description (SDP)
- **SETUP**: Setup transport for media stream
- **PLAY**: Start media transmission
- **PAUSE**: Temporarily halt transmission
- **TEARDOWN**: Stop transmission and cleanup
- **GET_PARAMETER**: Query session parameters
- **SET_PARAMETER**: Modify session parameters

### SDP (Session Description Protocol)
```
v=0
o=- 1642247400 1642247400 IN IP4 192.168.1.100
s=RTSP Session
c=IN IP4 192.168.1.100
t=0 0
m=video 5004 RTP/AVP 96
a=rtpmap:96 H264/90000
a=fmtp:96 packetization-mode=1;profile-level-id=4d001e;sprop-parameter-sets=Z00AHpWoKA9puAgIAAADAAQAAAMAPA8WLqA=,aO48gA==
a=control:stream=0
```

### RTP Payload Format
- **Payload Type**: 96 (H.264 dynamic)
- **Packetization Mode**: 1 (Non-interleaved mode)
- **Profile Level ID**: 4d001e (Main Profile Level 3.0)
- **Maximum Packet Size**: 1400 bytes (MTU consideration)

## Performance Optimization

### Latency Reduction
```bash
# Ultra-low latency pipeline (< 100ms)
gst-launch-1.0 \
    v4l2src device=/dev/video0 ! \
    video/x-raw,format=YUY2,width=1920,height=1080,framerate=30/1 ! \
    v4l2h264enc extra-controls="controls,video_bitrate=4000000,h264_profile=1,h264_level=13" \
               tune=0x00000004 ! \
    video/x-h264,profile=baseline ! \
    rtph264pay config-interval=-1 pt=96 ! \
    udpsink host=0.0.0.0 port=5004 sync=false
```

### Hardware Acceleration
```bash
# Use hardware encoder if available
v4l2h264enc extra-controls="controls,video_bitrate=4000000,video_gop_size=30"

# VAAPI acceleration (Intel GPUs)
vaapih264enc bitrate=4000 keyframe-period=30

# NVENC acceleration (NVIDIA GPUs)  
nvh264enc bitrate=4000 gop-size=30 preset=low-latency-hq
```

### Network Optimization
```bash
# Buffer tuning for network stability
echo 'net.core.rmem_max = 67108864' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 67108864' >> /etc/sysctl.conf
echo 'net.ipv4.udp_mem = 102400 873800 16777216' >> /etc/sysctl.conf
sysctl -p
```

## Troubleshooting

### Common Issues

**"Connection refused" or "No route to host"**:
```bash
# Check RTSP server status
netstat -tlnp | grep :554

# Test connectivity
telnet 192.168.1.100 554

# Check firewall rules
iptables -L | grep 554
```

**"Authentication failed"**:
```bash
# Test with curl
curl -v "rtsp://admin:password@192.168.1.100:554/stream0"

# Check credentials in device config
cat /etc/rotordream/auth.conf
```

**"No video data received"**:
```bash
# Check video device
v4l2-ctl --device=/dev/video0 --list-formats

# Test local pipeline
gst-launch-1.0 v4l2src device=/dev/video0 ! autovideosink

# Monitor RTP packets
tcpdump -i eth0 -n port 5004
```

**High latency or buffering**:
```bash
# Reduce client buffer
vlc --network-caching=50 rtsp://192.168.1.100:554/stream0

# Check network quality
ping -c 10 192.168.1.100
iperf3 -c 192.168.1.100 -t 30
```

### Debug Commands
```bash
# Enable GStreamer debug output
export GST_DEBUG=3
gst-launch-1.0 rtspsrc location=rtsp://192.168.1.100:554/stream0 ! fakesink

# RTSP protocol debugging
export GST_DEBUG=rtspsrc:5
vlc --intf dummy --extraintf logger --verbose 2 rtsp://192.168.1.100:554/stream0

# Network packet analysis
wireshark -i eth0 -f "host 192.168.1.100 and (port 554 or portrange 5004-5010)"
```

## Security Considerations

### Access Control
- Default authentication required for all streams
- Support for user-specific stream access permissions
- IP-based access control lists
- Session timeout and automatic cleanup

### Encryption
```bash
# RTSP over TLS (RTSPS) - if supported
rtsps://admin:password@192.168.1.100:8554/stream0

# VPN tunnel for secure transmission
openvpn --config camera_access.ovpn
```

### Bandwidth Management
```bash
# Rate limiting per client
iptables -A OUTPUT -p udp --dport 5004:5010 -m limit --limit 10000/sec -j ACCEPT
iptables -A OUTPUT -p udp --dport 5004:5010 -j DROP
```

## Related Documentation

- [Camera Pipeline](../architecture/camera-pipeline.md) - Hardware integration details
- [WebSocket API](websocket-api.md) - Alternative real-time interface
- [HTTP API](http-api.md) - REST endpoints for control
- [Performance Tuning](../operations/performance.md) - Optimization guidelines

---

*RTSP documentation based on GStreamer implementation in `src/camserver/streamer.nim` and client examples*
