# Getting Started with C Pro Camera Server

**Quick start guide to get your C Pro camera system up and running.**

## Overview

This guide will help you set up, configure, and start using the C Pro camera server for the first time, whether you're working with the embedded system or setting up a development environment.

## Prerequisites

### Hardware Requirements

**Minimum for Development**:
- x86_64 or ARM64 processor
- 2GB RAM
- 10GB disk space

**Recommended for Production**:
- ARM64 embedded platform (Cortex-A53+)
- 4GB RAM
- Ethernet

### Software Requirements

**Linux System**:
- Ubuntu 20.04+ 
- Kernel 4.9+ (for V4L2 support)

**Runtime Dependencies**:
- GStreamer 1.14+
- SQLite 3.20+
- LevelDB 1.20+
- V4L2 drivers

**Build Dependencies** (development only):
- Nim compiler 1.6+
- GCC 7+ or Clang 10+
- pkg-config
- Linux kernel headers

## Quick Start (Embedded System)

If you received a pre-configured embedded device, follow these steps:

### 1. Physical Setup

```bash
# Connect hardware components
1. Connect camera(s) to camera ports
2. Connect Ethernet cable
3. Connect power supply
4. Wait 30-60 seconds for boot
```

### 2. Network Configuration

**Default Network Settings**:
- **DHCP**: Enabled by default
- **Hostname**: `rotoclear-XXXXXX` (based on MAC address)
- **Discovery**: mDNS/Bonjour enabled

**Find Your Device**:
```bash
# Using mDNS (Linux/Mac)
avahi-browse -rt _http._tcp

# Or scan your network
nmap -sn 192.168.1.0/24

# Or check DHCP leases on your router
```

### 3. Access Web Interface

```bash
# Open browser and navigate to:
http://rotoclear-XXXXXX.local
# or
http://<device-ip-address>

# Default credentials:
Username: admin
Password: admin  # Change immediately!
```

### 4. Initial Configuration

1. **Change Default Password**
   - Navigate to Settings → Users
   - Update admin password
   - Click "Save Changes"

2. **Verify Camera Detection**
   - Go to Camera → Settings
   - Confirm camera(s) detected
   - Adjust resolution/fps if needed

3. **Configure Network** (optional)
   - Go to Network → Settings
   - Set static IP if required
   - Configure hostname

4. **Test Streaming**
   - Navigate to Live View
   - Verify video feed appears
   - Test RTSP stream: `rtsp://<device-ip>:554/stream1`

## Quick Start (Development)

### 1. Install Dependencies

**Ubuntu/Debian**:
```bash
# Install system dependencies
sudo apt update
sudo apt install -y \
  build-essential \
  git \
  pkg-config \
  sqlite3 \
  libleveldb-dev \
  gstreamer1.0-tools \
  gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-ugly \
  libgstreamer1.0-dev \
  libgstreamer-plugins-base1.0-dev

# Install Nim compiler
curl https://nim-lang.org/choosenim/init.sh -sSf | sh
export PATH=$HOME/.nimble/bin:$PATH
choosenim stable
```

**Verify Installation**:
```bash
nim --version      # Should show Nim 1.6+
gst-inspect-1.0    # Should list GStreamer plugins
```

### 2. Clone Repository

```bash
git clone https://github.com/cortona-rotoclear/rotordream.git
cd rotordream
```

### 3. Install Nim Dependencies

```bash
# Install required Nim packages
nimble install -y corun

# Check tools directory exists
ls tools/
```

### 4. Build Development Version

```bash
# Build for development (with debug symbols)
nim c -d:debug rotordream.nim

# Or use the build tool
nim c -r tools/buildRelease.nim --target:local
```

### 5. Run Development Server

```bash
# Run with default settings
./rotordream

# Or with custom configuration
./rotordream --config=config.json
```

**Expected Output**:
```
GStreamer initialized
Camera client started
State system initialized
HTTP server listening on :80
HTTPS server listening on :443
RTSP server listening on :554
```

### 6. Access Development Interface

```bash
# Open browser
http://localhost:80

# Default development credentials:
Username: admin
Password: admin
```

## Configuration

### Factory Configuration

The system uses build-time variant configuration. See [Deployment Variants](configuration/deployment-variants.md) for details.

**Configuration Files**:
```
rsc_config/
├── config_DEFAULT/      # Development
├── config_DEMO/         # Demo mode
├── config_DEV/          # Factory testing
├── config_EDU/          # Education variant
├── config_rc_DMG/       # Production
└── config_VB/           # OEM variant
```

**Select Variant at Build**:
```bash
# Build with specific variant
nim c -d:variant_EDU rotordream.nim
```

### Runtime Configuration

**State Persistence**: Stored in LevelDB
- **Embedded**: `/media/data/state.db`
- **Desktop**: `./state.db`

**Metadata Database**: SQLite
- **Embedded**: `/media/data/metadata.db`
- **Desktop**: `./metadata.db`

**Media Storage**:
- **Embedded**: `/media/data/videos/`
- **Desktop**: `./videos/`

## Basic Operations

### Start/Stop Services

**Embedded System** (systemd):
```bash
# Check status
systemctl status rotordream

# Start service
sudo systemctl start rotordream

# Stop service
sudo systemctl stop rotordream

# Restart service
sudo systemctl restart rotordream

# Enable auto-start on boot
sudo systemctl enable rotordream
```

**Development**:
```bash
# Start in foreground
./rotordream

# Stop with Ctrl+C

# Run in background
./rotordream &

# Stop background process
killall rotordream
```

### Check System Status

**Via Web API**:
```bash
# System info
curl http://localhost/api/info

# System status
curl http://localhost/api/status

# Camera status
curl http://localhost/api/camera/status
```

**Via Logs**:
```bash
# Embedded system
journalctl -u rotordream -f

# Development
tail -f /var/log/rotordream.log
```

### Test Camera

**Verify Camera Detection**:
```bash
# List V4L2 devices
v4l2-ctl --list-devices

# Get camera capabilities
v4l2-ctl -d /dev/video0 --all
```

**Test GStreamer Pipeline**:
```bash
# Test camera capture
gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! autovideosink

# Test encoding
gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! x264enc ! filesink location=test.h264
```

### Test Streaming

**RTSP Stream**:
```bash
# Using VLC
vlc rtsp://localhost:554/stream1

# Using FFmpeg
ffplay rtsp://localhost:554/stream1

# Using GStreamer
gst-launch-1.0 playbin uri=rtsp://localhost:554/stream1
```

**WebSocket API**:
```bash
# Using websocat (install: cargo install websocat)
websocat ws://localhost/api/v1

# Send state update
{"light0": true}
```

## First Recording

### Via Web Interface

1. Navigate to **Recording** section
2. Click **Start Recording**
3. Recording appears in **Recordings** list
4. Click **Stop Recording** when done
5. View recording in **Playback** section

### Via API

**HTTP API**:
```bash
# Start recording
curl -X POST http://localhost/api/recording/start

# Stop recording
curl -X POST http://localhost/api/recording/stop

# List recordings
curl http://localhost/api/recordings
```

**WebSocket API**:
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost/api/v1');

// Start recording
ws.send(JSON.stringify({
  "record": true
}));

// Stop recording
ws.send(JSON.stringify({
  "record": false
}));
```

## User Management

### Create Additional Users

**Via Web Interface**:
1. Settings → Users → Add User
2. Enter username, password, email
3. Assign role (Operator, Viewer, Admin)
4. Click "Create User"

**Via API**:
```bash
curl -X POST http://localhost/api/users \
  -u admin:admin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "doctor1",
    "password": "secure_password",
    "email": "doctor1@hospital.com",
    "role": "operator"
  }'
```

### User Roles

| Role | Permissions |
|------|-------------|
| **Admin** | Full system access, user management, configuration |
| **Operator** | Camera control, recording, streaming, tagging |
| **Viewer** | View streams, playback recordings (read-only) |
| **Guest** | Limited view-only access |

See [Permissions Documentation](security/permissions.md) for details.

## Network Configuration

### Static IP Configuration

**Via Web Interface**:
1. Network → Settings
2. Disable DHCP
3. Enter IP, Netmask, Gateway, DNS
4. Click "Apply"
5. System will restart with new network settings

**Via Command Line** (embedded):
```bash
# Edit network configuration
sudo nano /etc/network/interfaces

# Example static configuration:
auto eth0
iface eth0 inet static
  address 192.168.1.100
  netmask 255.255.255.0
  gateway 192.168.1.1
  dns-nameservers 8.8.8.8

# Apply changes
sudo systemctl restart networking
```

### Port Forwarding

If accessing from external network, forward these ports:

| Port | Protocol | Service |
|------|----------|---------|
| 80 | TCP | HTTP Web Interface |
| 443 | TCP | HTTPS Web Interface |
| 554 | TCP | RTSP Streaming |
| 8080 | TCP | Alternative HTTP |

## Troubleshooting

### Camera Not Detected

```bash
# Check USB devices
lsusb

# Check V4L2 devices
ls -l /dev/video*

# Check permissions
sudo usermod -aG video $USER

# Reboot if needed
sudo reboot
```

### Cannot Access Web Interface

```bash
# Check if service is running
systemctl status rotordream

# Check port availability
sudo netstat -tlnp | grep :80

# Check firewall
sudo ufw status
sudo ufw allow 80/tcp
```

### No Video Stream

```bash
# Check GStreamer plugins
gst-inspect-1.0 | grep v4l2

# Test camera directly
gst-launch-1.0 v4l2src ! autovideosink

# Check system logs
journalctl -u rotordream -n 100
```

### Poor Video Quality

1. **Check Resolution Settings**
   - Camera → Settings → Resolution
   - Lower resolution for better performance

2. **Check Frame Rate**
   - Camera → Settings → FPS
   - Try 30 FPS instead of 60 FPS

3. **Check Network Bandwidth**
   ```bash
   # Test network speed
   iperf3 -c <server-ip>
   ```

4. **Check CPU Usage**
   ```bash
   # Monitor system resources
   htop
   ```

## Next Steps

### Learn More

- **[Architecture Overview](architecture/overview.md)**: Understand system design
- **[API Documentation](api/README.md)**: Integrate with external systems
- **[Configuration Guide](configuration/factory-config.md)**: Advanced configuration
- **[Security Setup](security/authentication.md)**: Secure your deployment
- **[Operations Guide](operations/build-and-deploy.md)**: Production deployment

### Explore Features

- **[Recording System](camera/recording.md)**: Advanced recording features
- **[Streaming Options](camera/streaming.md)**: RTSP, WebRTC, ONVIF
- **[Image Processing](camera/image-processing.md)**: Enhancement, overlays
- **[Tag Management](camera/recording.md#tag-system)**: Organize recordings

### Get Help

- **[Troubleshooting Guide](operations/troubleshooting.md)**: Common issues
- **[Glossary](glossary.md)**: Technical terminology
- **GitHub Issues**: Report bugs or request features
- **Support Email**: support@rotoclear.com

## Common Use Cases

### Medical Education Setup

```bash
# Build EDU variant
nim c -d:variant_EDU rotordream.nim

# Configure dual cameras
# - Scope camera (main view)
# - Overview camera (PIP)

# Enable features:
# - Picture-in-Picture
# - Real-time tagging
# - Multi-user annotation
```

### Production Line Inspection

```bash
# Build rc_DMG variant
nim c -d:variant_rc_DMG rotordream.nim

# Configure for continuous operation
# - Enable auto-recording on motion
# - Set retention policy (30 days)
# - Configure network storage (SMB/NFS)
# - Enable ONVIF for NVR integration
```

### Research Documentation

```bash
# Build DEFAULT variant
nim c rotordream.nim

# Configure for flexibility
# - Enable all recording modes
# - Configure detailed metadata
# - Enable tag categories
# - Export recordings with metadata
```

## FAQ

**Q: What cameras are supported?**  
A: Any V4L2-compatible USB camera (UVC) or CSI camera on supported platforms.

**Q: Can I use multiple cameras?**  
A: Yes, the EDU and rc_DMG variants support multiple cameras with PIP.

**Q: What video formats are supported?**  
A: H.264/AVC (primary), MJPEG, with AVI and MP4 container formats.

**Q: How do I backup recordings?**  
A: Configure network storage (SMB/NFS) or use USB backup. See [Storage Configuration](configuration/storage-backup.md).

**Q: Is HTTPS/SSL supported?**  
A: Yes, see [SSL Certificates](security/ssl-certificates.md) for setup.

**Q: Can I integrate with my existing system?**  
A: Yes, via HTTP REST API, WebSocket API, RTSP streaming, or ONVIF protocol. See [API Documentation](api/README.md).

**Q: What's the maximum recording duration?**  
A: Limited only by available storage. System automatically manages storage when full.

**Q: How do I update the software?**  
A: Via web interface (System → Update) or manually. See [Build and Deploy](operations/build-and-deploy.md).

