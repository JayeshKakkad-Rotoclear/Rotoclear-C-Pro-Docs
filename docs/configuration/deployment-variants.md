# Deployment Variants

## Overview

RotoClear camera systems support multiple deployment variants to accommodate different use cases, environments, and customer requirements. Each variant is a distinct build configuration with specific features, branding, and operational parameters.

## Variant Architecture

### Build-Time Configuration

Variants are selected at compile time using the `CONFIG_VARIANT` environment variable:

```bash
# Select variant during compilation
CONFIG_VARIANT=rc_DMG nim c -d:release rotordream.nim

# Variant-specific resources are embedded
# - Configuration files
# - UI assets
# - Custom stylesheets
# - Branding elements
```

### Variant Components

Each variant consists of:

1. **Factory Configuration** - System behavior and feature flags
2. **License Template** - Default licensing terms
3. **UI Customization** - Branding and appearance
4. **Asset Bundle** - Images, icons, stylesheets
5. **Version Flavor** - Variant identifier string

## Available Variants

### DEFAULT

**Purpose**: Base configuration for standard deployments

**Characteristics**:
- Minimal feature set
- Generic branding
- No customer-specific customizations
- Used as template for new variants

**Use Cases**:
- Development baseline
- Generic OEM deployments
- Proof-of-concept systems

**Configuration**:
```json
{
  "systemName": "RotoClear Camera",
  "modelNumber": "RC-STD",
  "features": {
    "recording": true,
    "streaming": true,
    "onvif": true
  }
}
```

### DEMO

**Purpose**: Demonstration and evaluation systems

**Characteristics**:
- 30-day time limit
- Watermark on video output
- All features enabled
- Telemetry for evaluation tracking

**Use Cases**:
- Trade show demonstrations
- Customer evaluations
- Sales presentations
- Training systems

**Restrictions**:
- Time-bombed operation
- Limited recording storage
- Visible watermark
- Telemetry enabled

**Configuration**:
```json
{
  "systemName": "RotoClear DEMO",
  "licenseType": "demo",
  "validity": {
    "durationDays": 30,
    "watermark": true
  },
  "telemetry": {
    "enabled": true,
    "uploadUrl": "https://telemetry.rotoclear.com/demo"
  }
}
```

### DEV

**Purpose**: Development and testing environment

**Characteristics**:
- Extended logging enabled
- Debug endpoints exposed
- Simulator mode available
- Relaxed security constraints

**Use Cases**:
- Software development
- Feature testing
- Integration testing
- Debugging sessions

**Special Features**:
- Camera simulator (no hardware required)
- Mock data generators
- Detailed trace logging
- Performance profiling tools

**Configuration**:
```json
{
  "systemName": "RotoClear DEV",
  "debug": {
    "enableSimulator": true,
    "verboseLogging": true,
    "exposeDebugApi": true,
    "disableSecurity": false
  },
  "features": {
    "allEnabled": true
  }
}
```

### EDU

**Purpose**: Educational institution deployments

**Characteristics**:
- Educational branding
- Multi-user collaboration
- Extended retention policies
- Curriculum-focused features

**Use Cases**:
- Medical schools
- Surgical training centers
- Research institutions
- Teaching hospitals

**Special Features**:
- Session recording with annotations
- Student collaboration tools
- Case library management
- Educational content tagging

**Configuration**:
```json
{
  "systemName": "RotoClear Educational",
  "modelNumber": "RC-EDU",
  "licenseType": "educational",
  "features": {
    "annotations": true,
    "multiUser": true,
    "caseLibrary": true,
    "extendedRetention": true
  },
  "users": {
    "maxConcurrent": 50,
    "roles": ["instructor", "student", "admin"]
  }
}
```

### rc_DMG

**Purpose**: RotoClear DMG product line

**Characteristics**:
- Dual camera head support
- Integrated rotation motor control
- FPGA-based image processing
- Medical-grade recording

**Use Cases**:
- Surgical microscopy
- Medical documentation
- Research applications
- Clinical procedures

**Hardware Requirements**:
- Dual camera inputs (V4L2)
- Rotation motor controller
- FPGA co-processor
- High-performance storage

**Special Features**:
- Automatic rotation detection
- Picture-in-picture mode
- Advanced image enhancement
- DICOM integration ready

**Configuration**:
```json
{
  "systemName": "RotoClear DMG",
  "modelNumber": "RC-DMG-4K",
  "hardware": {
    "cameraHeads": 2,
    "maxResolution": "3840x2160",
    "hasRotationMotor": true,
    "hasFpgaTemp": true,
    "hasLightControl": true
  },
  "features": {
    "pip": true,
    "autoRotate": true,
    "imageEnhancement": true
  }
}
```

### VB

**Purpose**: VB customer-specific variant

**Characteristics**:
- Custom branding
- Specialized workflow
- Integration requirements
- Unique feature set

**Use Cases**:
- Customer-specific deployments
- Custom OEM integration
- Specialized applications

**Customizations**:
- Custom UI theme and colors
- Specialized recording modes
- External system integration
- Custom data formats

## Creating New Variants

### Step 1: Directory Setup

```bash
# Create new variant directory
mkdir -p rsc_config/config_NEWVARIANT

# Copy base configuration
cp rsc_config/config_DEFAULT/* rsc_config/config_NEWVARIANT/
```

### Step 2: Configuration Files

Create/modify key configuration files:

**factory_config.json**:
```json
{
  "systemName": "RotoClear New Variant",
  "modelNumber": "RC-NV-001",
  "features": {
    "recording": true,
    "streaming": true
  }
}
```

**version_flavor**:
```
NewVariant-v1.0
```

**license_config.json**:
```json
{
  "licenseType": "commercial",
  "customer": {
    "name": "New Customer",
    "id": "NC-001"
  }
}
```

### Step 3: Custom Assets

Add custom branding assets:

```
config_NEWVARIANT/
├── imgs/
│   ├── logo.svg
│   ├── favicon.ico
│   └── splash.png
├── hdmi_imgs/
│   └── hdmi_logo.png
└── stylesheets/
    └── custom.css
```

### Step 4: Build and Test

```bash
# Build with new variant
CONFIG_VARIANT=NEWVARIANT nim c rotordream.nim

# Test deployment
./rotordream

# Verify configuration loaded
curl http://localhost:8080/api/system/info
```

### Step 5: CI/CD Integration

Add to build pipeline:

```yaml
# .github/workflows/build.yml
jobs:
  build-variants:
    strategy:
      matrix:
        variant: [DEFAULT, DEMO, DEV, EDU, rc_DMG, VB, NEWVARIANT]
    steps:
      - name: Build variant
        run: |
          export CONFIG_VARIANT=${{ matrix.variant }}
          nim c -d:release rotordream.nim
      - name: Package
        run: |
          tar czf rotordream-${{ matrix.variant }}.tar.gz rotordream
```

## Variant Selection at Runtime

### Auto-Detection

System can detect appropriate variant based on:

```nim
proc detectVariant*(): string =
  # Check hardware identifiers
  if hasDualCameraHeads() and hasRotationMotor():
    return "rc_DMG"
  
  # Check license file
  let license = tryLoadLicense()
  if license.licenseType == "educational":
    return "EDU"
  
  # Default variant
  return "DEFAULT"
```

### Manual Override

Override variant selection via environment variable:

```bash
# Force specific variant at runtime
export ROTOCLEAR_VARIANT=DEV
./rotordream
```

## Variant Comparison Matrix

| Feature | DEFAULT | DEMO | DEV | EDU | rc_DMG | VB |
|---------|---------|------|-----|-----|--------|-----|
| Recording | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Streaming | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ONVIF | ✓ | ✓ | ✓ | ✓ | ✓ | Custom |
| WebRTC | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Dual Cameras | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| Rotation Motor | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| Annotations | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| Simulator | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Watermark | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Max Users | 5 | 3 | ∞ | 50 | 10 | Custom |
| Support Level | Community | Trial | Developer | Educational | Premium | Custom |

## Variant Migration

### Upgrading Variants

To migrate from one variant to another:

```bash
# Backup current configuration
cp /config/*.json /backup/

# Deploy new variant binary
scp rotordream-NEWVARIANT root@device:/usr/local/bin/rotordream

# Update license (if required)
scp license-NEWVARIANT.json root@device:/config/decrypted_rsc/license_config.json

# Restart system
ssh root@device systemctl restart rotordream
```

### Preserving Settings

User settings are preserved across variant changes:

- Network configuration
- User accounts
- Recording library
- Tag categories (as of issue #150 fix)
- Custom settings

Factory-specific settings are reset to new variant defaults.

## Testing Variants

### Variant-Specific Tests

```nim
# tests/test_variant.nim
import unittest
import ../src/state/factory_config

suite "Variant Configuration":
  test "DEFAULT variant loads":
    let config = loadFactoryConfig("DEFAULT")
    check config.systemName == "RotoClear Camera"
  
  test "DEMO variant has watermark":
    let config = loadFactoryConfig("DEMO")
    check config.restrictions.watermark == true
  
  test "rc_DMG variant has dual cameras":
    let config = loadFactoryConfig("rc_DMG")
    check config.hardware.cameraHeads == 2
```

### Integration Testing

Test variant-specific workflows:

```bash
# Test recording with variant
pytest tests/test_recording.py --variant=rc_DMG

# Test API endpoints
pytest tests/test_api.py --variant=EDU

# Test hardware integration
pytest tests/test_hardware.py --variant=rc_DMG
```

## Troubleshooting

### Wrong Variant Loaded

**Symptom**: System shows incorrect variant name or features.

**Solution**:
- Check `CONFIG_VARIANT` environment variable during build
- Verify correct binary is deployed
- Check `/api/system/info` endpoint for loaded variant
- Review build logs for variant selection

### Missing Features

**Symptom**: Expected features not available in variant.

**Solution**:
- Review variant feature matrix
- Check factory configuration file
- Verify license permits feature
- Consult variant documentation

### Custom Assets Not Applied

**Symptom**: Custom logos or styles not displayed.

**Solution**:
- Verify assets exist in variant directory
- Check file paths in configuration
- Ensure assets embedded during build
- Review browser console for load errors

## Related Documentation

- [Factory Configuration](factory-config.md)
- [License Configuration](license-config.md)
- [Build and Deploy](../operations/build-and-deploy.md)
- [Environments](environments.md)
