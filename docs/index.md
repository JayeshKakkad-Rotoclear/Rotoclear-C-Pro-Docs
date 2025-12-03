# Rotoclear C Pro Server Documentation

Welcome to the comprehensive documentation for the Rotoclear C Pro server system - an industrial-grade camera control and streaming platform for industrial imaging applications.

## Overview

C Pro is a high-performance camera server built with the Nim programming language, providing:

- **Real-time video streaming** via RTSP, WebRTC, and ONVIF protocols
- **High-quality recording** with multiple formats and metadata tagging
- **Advanced camera control** for professional imaging applications
- **Multi-camera support** with picture-in-picture capabilities
- **Flexible deployment** across embedded and desktop platforms
- **Comprehensive API** for integration with external systems

## Quick Links

### Getting Started
- [Getting Started Guide](getting-started.md) - Installation and first steps
- [Development Setup](operations/development-setup.md) - Set up development environment
- [Build and Deploy](operations/build-and-deploy.md) - Build from source

### Architecture
- [System Overview](architecture/overview.md) - High-level architecture
- [State Management](architecture/state-management.md) - Observable state system
- [Camera Pipeline](architecture/camera-pipeline.md) - Video capture and processing
- [Metadata Storage](architecture/metadata-sqlite.md) - SQLite-based metadata system

### Configuration
- [Factory Configuration](configuration/factory-config.md) - Build-time configuration
- [Deployment Variants](configuration/deployment-variants.md) - Product variants (DEFAULT, DEMO, DEV, EDU, rc_DMG, VB)
- [License Configuration](configuration/license-config.md) - License management
- [Network Setup](configuration/network.md) - Network configuration

### Camera System
- [Hardware Interface](camera/hardware-interface.md) - V4L2, UVC, GPIO, motors, lighting
- [Streaming](camera/streaming.md) - RTSP, WebRTC, multi-stream
- [Recording](camera/recording.md) - Recording modes, metadata, tags
- [Image Processing](camera/image-processing.md) - Enhancement, overlays, FPGA acceleration

### API Reference
- [HTTP API](api/http-api.md) - REST endpoints
- [WebSocket API](api/websocket-api.md) - Real-time state updates
- [RTSP Streaming](api/rtsp-streaming.md) - RTSP protocol details
- [State Observables](reference/state-observables.md) - Complete observable reference

### Security
- [Authentication](security/authentication.md) - User authentication methods
- [Permissions](security/permissions.md) - Role-based access control
- [SSL Certificates](security/ssl-certificates.md) - TLS/SSL configuration

### Operations
- [Monitoring](operations/monitoring.md) - System monitoring
- [Troubleshooting](operations/troubleshooting.md) - Common issues and solutions
- [Performance](operations/performance.md) - Performance tuning

## System Features

### Video Capabilities
- **Resolutions**: Up to 4K (3840x2160) at 60 FPS
- **Formats**: H.264, H.265, MJPEG
- **Recording Modes**: Standard video, timelapse, slow motion
- **Streaming Protocols**: RTSP, WebRTC, ONVIF
- **Multi-Camera**: Dual camera support with PIP mode

### Storage & Organization
- **Local Storage**: Internal and USB storage
- **Network Storage**: NFS and SMB support
- **Metadata System**: SQLite-based with full-text search
- **Tag & Categories**: Organize recordings with tags and categories
- **Automatic Cleanup**: Retention policies and space management

### Hardware Integration
- **Camera Interfaces**: V4L2, USB (UVC), MIPI CSI-2
- **Motor Control**: Rotation platform with auto-detection
- **Lighting**: PWM-controlled LED lighting
- **Sensors**: Temperature, proximity, position sensors
- **HDMI Output**: Real-time display output

### Security Features
- **Authentication**: Basic, Digest, Bearer token, Session-based
- **Authorization**: Fine-grained permission system with RBAC
- **Encryption**: SSL/TLS for all network communication
- **Audit Logging**: Comprehensive security event logging

### Deployment Options
- **Embedded Systems**: Optimized for ARM-based embedded platforms
- **Desktop Systems**: Development and testing on x86/x64
- **Docker**: Containerized deployment (optional)
- **Multiple Variants**: 6 pre-configured deployment variants

## Deployment Variants

| Variant | Purpose | Use Case |
|---------|---------|----------|
| **DEFAULT** | Base configuration | Standard deployments |
| **DEMO** | Evaluation | Trade shows, trials |
| **DEV** | Development | Software development |
| **EDU** | Educational | Medical schools, training |
| **rc_DMG** | DMG Product Line | Surgical microscopy |
| **VB** | Custom OEM | Customer-specific |

## Architecture Highlights

### Observable State System
Reactive state management with persistent storage:
- 50+ system observables
- Automatic persistence
- Permission-based access control
- Real-time updates via WebSocket

### Modular Design
Component-based architecture:
- **Camera Server**: V4L2/GStreamer integration
- **Web Server**: HTTP and WebSocket APIs
- **ONVIF Service**: Standards-compliant protocol support
- **State Manager**: Centralized observable state
- **Storage Manager**: Recording and metadata handling

### Performance
- **Hardware Acceleration**: V4L2 encoders, FPGA processing
- **Low Latency**: <100ms glass-to-glass latency
- **Concurrent Streams**: Multiple simultaneous clients
- **Efficient Storage**: H.264/H.265 compression

## Technology Stack

- **Programming Language**: Nim (compiled to native code)
- **Framework**: Corun (async I/O framework)
- **Video Pipeline**: GStreamer
- **Database**: SQLite for metadata
- **Storage**: LevelDB for persistent state
- **Protocols**: HTTP, WebSocket, RTSP, WebRTC, ONVIF
- **Build System**: Nim compiler with custom build scripts

## Support & Resources

### Documentation
- [API Examples](api/examples/) - Multi-language client examples
- [Integration Guide](integration/onvif-protocol.md) - ONVIF integration
- [Glossary](glossary.md) - Technical terminology

### Development
- [GitHub Repository](https://github.com/cortona-rotoclear/rotordream)
- [Issue Tracker](https://github.com/cortona-rotoclear/rotordream/issues)
- [Changelog](releases/CHANGELOG.md)

### Contact
- **Technical Support**: support@rotoclear.com
- **Sales Inquiries**: sales@rotoclear.com
- **Website**: https://rotoclear.com

## Recent Updates

### Comprehensive Documentation Release
Complete architectural documentation covering all system components, configuration options, security model, and operational procedures.

## License

See [License Configuration](configuration/license-config.md) for licensing information and terms.

---

**Version**: 1.0.0  
**Last Updated**: December 2025
