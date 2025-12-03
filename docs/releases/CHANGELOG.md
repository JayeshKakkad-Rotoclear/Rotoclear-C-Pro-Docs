# Changelog

**Human-readable release history for Rotoclear Camera Server.**

## Format

This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation set
- API reference with working examples
- Multi-environment configuration guide

### Changed
- > TODO: Document pending changes

### Deprecated
- > TODO: Document deprecated features

### Removed
- > TODO: Document removed features

### Fixed
- > TODO: Document bug fixes

### Security
- > TODO: Document security improvements

## [1.0.0] - Current Version

**Current stable release (from `rotordream.nimble`)**

### Features
- **Real-time WebSocket API** - Bidirectional camera control and state management
- **Multi-camera Support** - Multiple camera heads with sensor selection
- **Video Recording** - AVI recording with configurable quality settings
- **Image Capture** - JPEG snapshots with timestamp overlays
- **HTTP/HTTPS Servers** - Web interface and file operations
- **RTSP Streaming** - Standards-based video streaming
- **Permission System** - Role-based access control with API tokens
- **Observable State** - Reactive state management with 40+ specialized modules
- **Cross-platform Build** - Development on x86, deployment on ARM64
- **Multi-environment Config** - DEV/DEMO/EDU/VB/DMG configuration variants

### Technical Stack
- **Language**: Nim 2.2.2+
- **Framework**: Corun async runtime
- **Camera Interface**: V4L2 with GStreamer pipeline
- **Memory Management**: ORC garbage collector
- **Authentication**: Token-based with Basic Auth fallback
- **Configuration**: JSON-based multi-environment system

### API Endpoints
- **WebSocket**: `ws://host:port/api?token=<TOKEN>`
- **Camera Image**: `http://host:port/camera.jpeg?token=<TOKEN>`
- **Web Interface**: `http://host:port/`
- **RTSP Stream**: `rtsp://host:port/stream`

### Supported Platforms
- **Development**: Ubuntu/Debian Linux, Windows with WSL2
- **Production**: ARM64 embedded Linux (C Pro hardware)

## Version History Template

### [Version] - YYYY-MM-DD

#### Added
- New features and capabilities

#### Changed  
- Changes to existing functionality

#### Deprecated
- Features marked for removal in future versions

#### Removed
- Features removed in this version

#### Fixed
- Bug fixes and corrections

#### Security
- Security improvements and vulnerability fixes

## Release Process

> TODO: Document the release process steps

### Pre-release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] Changelog updated
- [ ] Security review completed

### Release Steps
1. **Version Bump**: Update version in `rotordream.nimble`
2. **Build Testing**: Test cross-compilation for ARM64
3. **Documentation**: Update documentation for new features
4. **Release Notes**: Prepare human-readable release notes
5. **Deployment Testing**: Verify deployment on target hardware
6. **Tag Release**: Create Git tag with version number

### Post-release Steps
1. **Deployment**: Deploy to production devices
2. **Monitoring**: Monitor deployment health
3. **Feedback**: Collect user feedback
4. **Documentation**: Update any missing documentation

## Versioning Strategy

### Semantic Versioning

- **MAJOR**: Breaking changes, incompatible API changes
- **MINOR**: New features, backward-compatible additions
- **PATCH**: Bug fixes, backward-compatible fixes

### Version Components

**Format**: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Examples**:
- `1.0.0` - Stable release
- `1.1.0-beta.1` - Pre-release version
- `1.0.1+20240903.commit.abc123` - Build metadata

### API Versioning

API versions are managed separately from application versions:
- **WebSocket API**: Currently V1 (`websocketApiV1Handler.nim`)
- **HTTP API**: Version in URL path or headers
- **RTSP**: Standards-based versioning

## Breaking Changes

### Migration Guide Template

When breaking changes are introduced, include migration guidance:

#### From Version X.Y.Z to A.B.C

**Configuration Changes:**
```json
// Old format
{
  "oldProperty": "value"
}

// New format
{
  "newProperty": {
    "subProperty": "value"
  }
}
```

**API Changes:**
```javascript
// Old API
ws.send(JSON.stringify({"old-command": true}));

// New API  
ws.send(JSON.stringify({"new-command": {"enabled": true}}));
```

## Support and Compatibility

### Supported Versions

| Version | Status | Support Until | Notes |
|---------|--------|---------------|-------|
| 1.0.x | Current | Active | Current stable release |
| 0.9.x | Legacy | > TODO | Previous generation |

### Compatibility Matrix

| Component | Version | Compatibility |
|-----------|---------|---------------|
| Nim | 2.2.2+ | Required |
| Corun | 0.7.10+ | Required |
| GStreamer | 1.0+ | Recommended |
| V4L2 | Linux 4.0+ | Required |

## Known Issues

### Current Limitations

> TODO: Document known issues and limitations

### Workarounds

> TODO: Document workarounds for known issues

## Contributors

> TODO: Acknowledge contributors and maintainers

## License

Licensed under Rotoclear proprietary license. See `rotordream.nimble` for details.

---

*This changelog will be updated with each release. For the most current information, check the repository tags and commit history.*
