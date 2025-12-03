# Build and Deploy

**Complete guide for building and deploying the C Pro Camera Server.**

## Build System Overview

The project uses Nim's compiler with custom build scripts in the `tools/` directory for cross-compilation and deployment to ARM64 embedded systems.

## Development Build

### Local Compilation

```bash
# Quick development build
nim c -r rotordream.nim

# With debug information
nim c -r -d:RuntimeCallDebug=true rotordream.nim

# Release build (local)
nim c -d:release --mm:orc rotordream.nim
```

### VS Code Integration

Use configured VS Code tasks (Ctrl+Shift+B):

- **local-test-file**: Compile and run current file
- **local-test-rotordream**: Compile and run main application
- **remote-test**: Test on remote device
- **remote-release**: Build and deploy release

### Build Configuration

Core build settings (from `config.nims`):

```nim
switch("define", "leveldb")
switch("define", "directCompile=true")
switch("mm", "orc")  # ORC memory management
```

## Production Build

### Cross-compilation for ARM64

**Build Release for ARM64 Target:**

```bash
nim c -r tools/buildRelease.nim [falcon_firmware_path]
```

**Example:**
```bash
nim c -r tools/buildRelease.nim ../falcon_firmware
```

### Build Flags (from `tools/buildRelease.nim`)

```bash
nim c -d:release \
  --floatChecks:off \
  --overflowChecks:off \
  --passC:"-flto -ffast-math -funroll-loops -O3 -fno-strict-aliasing" \
  --nimcache:cache/release \
  -d:directCompile=true \
  -d:embeddedSystem \
  -d:useRobustFileExists=true \
  --cpu:arm64 \
  --os:linux \
  -o:'../falcon_firmware/projectroot/usr/bin/rotoclear_server' \
  rotordream.nim
```

### Embedded System Flags (from `tools/common.nim`)

```nim
proc getEmbeddedFlags*(isArm32: bool = true): string =
  result.add(" -d:directCompile=true -d:embeddedSystem -d:useRobustFileExists=true")
  result.add(" -d:CorunLogsDir=/media/data/logs ")
  
  if isArm32:
    # ARM32 library linking
    for (kind, path) in walkDir("libs-petalinux"):
      if kind == pcFile:
        result.add "-L:" & path & " "
    result.add " --passC:\"-D_FILE_OFFSET_BITS=64\""
  else:
    # ARM64 cross-compilation
    result.add(" --cpu:arm64 --os:linux -d:nosimd")
    result.add(" --clibdir:../falcon_firmware/platform-zynqmp/sysroot-target/usr/lib")
    result.add(" --passL:\"-L../falcon_firmware/platform-zynqmp/sysroot-target/usr/lib\"")
    result.add(" --passC:\"-I../falcon_firmware/platform-zynqmp/sysroot-target/usr/include\"")
```

## Deployment

### Environment Setup

Configure deployment target:

```bash
export C3_BOX_IP="192.168.1.100"  # Target device IP
export C3_BOX_PW="admin"           # SSH password
```

### Remote Deployment

**Deploy Release Build:**

```bash
nim c -r tools/remoteRelease.nim
```

**Deploy with Custom Path:**

```bash
nim c -r tools/remoteRelease.nim /path/to/falcon_firmware
```

### Deployment Process (from `tools/remoteRelease.nim`)

1. **Cross-compile** for ARM64 target
2. **Package** binary and assets
3. **SSH Transfer** to target device
4. **Install** on target system
5. **Restart** services

### SSH Configuration (from `tools/common.nim`)

```nim
var boxAddress* = "root@" & getEnv("C3_BOX_IP", default = "rotoclear-cam.fritz.box")
var boxPassword* = getEnv("C3_BOX_PW", default = "root")
var sshpass* = if defined(windows): "" else: "sshpass -p " & boxPassword & " "
```

## Build Dependencies

### System Requirements

**Development Environment:**
```bash
# Build tools
sudo apt-get install build-essential

# Media libraries
sudo apt install ffmpeg
sudo apt install libturbojpeg

# Cross-compilation tools (for ARM64)
sudo apt install gcc-aarch64-linux-gnu
```

**Nim Dependencies:**

```bash
# Install project dependencies
nim c -r tools/installDeps.nim
nimble setup
```

### Nim Package Dependencies (from `rotordream.nimble`)

```nim
requires "nim >= 2.2.2"
requires "corun >= 0.7.10"
requires "xxtea"
requires "checksums >= 0.2.1"
```

## Build Artifacts

### Output Locations

| Build Type | Output Path | Purpose |
|------------|-------------|---------|
| Development | `./rotordream` | Local testing binary |
| Release | `../falcon_firmware/projectroot/usr/bin/rotoclear_server` | ARM64 production binary |
| Cache | `cache/release/` | Nim compilation cache |

### Binary Size Optimization

Production builds use aggressive optimization:

- **Link-time optimization**: `-flto`
- **Fast math**: `-ffast-math`
- **Loop unrolling**: `-funroll-loops`
- **Maximum optimization**: `-O3`
- **No strict aliasing**: `-fno-strict-aliasing`

## Testing Deployment

### Remote Testing

```bash
nim c -r tools/remoteTest.nim
```

### Manual Verification

**Check Service Status:**
```bash
ssh root@$C3_BOX_IP "systemctl status rotoclear_server"
```

**View Logs:**
```bash
ssh root@$C3_BOX_IP "tail -f /media/data/logs/rotoclear.log"
```

**Test API Connectivity:**
```bash
curl "http://$C3_BOX_IP/api/status?token=1a2B3c4D5e6f7G8h"
```

## Configuration Deployment

### Environment-specific Builds

Deploy with specific configurations:

```bash
# Deploy DMG configuration
BUILD_CONFIG=DMG nim c -r tools/remoteRelease.nim

# Deploy EDU configuration  
BUILD_CONFIG=EDU nim c -r tools/remoteRelease.nim
```

### Asset Deployment

Deploy environment-specific assets:

```bash
# Copy configuration files
scp -r rsc_config/config_DMG/* root@$C3_BOX_IP:/opt/rotoclear/config/

# Copy web assets
scp -r assets/* root@$C3_BOX_IP:/opt/rotoclear/assets/
```

## Build Troubleshooting

### Common Build Issues

**Missing Cross-compiler:**
```bash
# Install ARM64 cross-compiler
sudo apt install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu
```

**Library Not Found:**
```bash
# Check library paths
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ldconfig
```

**Nim Cache Issues:**
```bash
# Clear Nim cache
rm -rf ~/.cache/nim/
rm -rf cache/
```

### Deployment Issues

**SSH Connection Failed:**
```bash
# Test SSH connectivity
ssh-keyscan $C3_BOX_IP
ssh root@$C3_BOX_IP "echo 'Connection successful'"
```

**Permission Denied:**
```bash
# Check SSH key or password
ssh-copy-id root@$C3_BOX_IP
```

**Service Won't Start:**
```bash
# Check dependencies
ssh root@$C3_BOX_IP "ldd /usr/bin/rotoclear_server"

# Check configuration
ssh root@$C3_BOX_IP "ls -la /opt/rotoclear/config/"
```

## Build Optimization

### Compilation Speed

**Parallel Compilation:**
```bash
nim c --threads:on --parallelBuild:4 rotordream.nim
```

**Cache Utilization:**
```bash
# Use persistent cache
nim c --nimcache:cache/dev rotordream.nim
```

### Binary Size Reduction

**Strip Debug Symbols:**
```bash
nim c -d:release --passL:"-s" rotordream.nim
```

**Link-time Optimization:**
```bash
nim c -d:release --passC:"-flto" --passL:"-flto" rotordream.nim
```

### Automated Builds

**Build Matrix:**
- Development (x86-64)
- Production ARM64 (multiple configurations)
- Cross-platform testing

**Deployment Pipeline:**
1. Build verification
2. Unit test execution
3. Cross-compilation
4. Deployment to staging
5. Integration testing
6. Production deployment

## Monitoring and Health Checks

### Post-deployment Verification

**Service Health:**
```bash
# Check process status
ssh root@$C3_BOX_IP "ps aux | grep rotoclear_server"

# Check port binding
ssh root@$C3_BOX_IP "netstat -tlnp | grep :80"
```

**API Health Check:**
```bash
# WebSocket connectivity
wscat -c "ws://$C3_BOX_IP/api?token=1a2B3c4D5e6f7G8h"

# HTTP endpoint
curl -f "http://$C3_BOX_IP/camera.jpeg?token=1a2B3c4D5e6f7G8h"
```

### Rollback Procedures

**Service Rollback:**
```bash
# Stop current service
ssh root@$C3_BOX_IP "systemctl stop rotoclear_server"

# Restore previous binary
ssh root@$C3_BOX_IP "cp /usr/bin/rotoclear_server.backup /usr/bin/rotoclear_server"

# Restart service
ssh root@$C3_BOX_IP "systemctl start rotoclear_server"
```

## Related Documentation

- [Getting Started](../getting-started.md) - Development setup
- [Environment Configuration](../configuration/environments.md) - Multi-environment configs
- [Testing Strategy](../testing/testing-strategy.md) - Testing procedures

---

*Build and deployment documentation derived from `tools/buildRelease.nim`, `tools/common.nim`, and `rotordream.nimble`*
