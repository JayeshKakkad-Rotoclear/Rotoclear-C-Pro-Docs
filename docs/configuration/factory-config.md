# Factory Configuration

## Overview

The factory configuration system provides a flexible mechanism to customize RotoClear camera behavior for different deployment scenarios, customers, and use cases. Configuration files are embedded during the build process and control system behavior at runtime.

## Configuration Structure

### Directory Layout

```
rsc_config/
├── config_DEFAULT/     # Default minimal configuration
├── config_DEMO/        # Demo/trial version settings
├── config_DEV/         # Development environment
├── config_EDU/         # Educational institutions
├── config_rc_DMG/      # RotoClear DMG variant
└── config_VB/          # VB customer variant
```

Each configuration directory can contain:

- `factory_config.json` - System behavior and feature flags
- `license_config.json` - License and feature restrictions
- `style_variables_config.json` - UI customization
- `version_flavor` - Build variant identifier
- `imgs/` - Custom UI assets
- `hdmi_imgs/` - HDMI output specific assets
- `stylesheets/` - CSS overrides

## Factory Configuration File

### Structure

```json
{
  "systemName": "RotoClear DMG",
  "modelNumber": "RC-DMG-4K",
  "features": {
    "recording": true,
    "streaming": true,
    "onvif": true,
    "webrtc": false,
    "pip": true,
    "zoom": true,
    "autoRotate": true
  },
  "hardware": {
    "cameraHeads": 2,
    "maxResolution": "3840x2160",
    "maxFps": 60,
    "hasLightControl": true,
    "hasRotationMotor": true,
    "hasFpgaTemp": true
  },
  "network": {
    "defaultDhcp": true,
    "allowStaticIp": true,
    "allowWifi": false,
    "defaultHostname": "rotoclear"
  },
  "storage": {
    "localEnabled": true,
    "networkEnabled": true,
    "backupEnabled": true,
    "minDiskSpaceGB": 10
  },
  "ui": {
    "showWizard": true,
    "defaultLanguage": "en",
    "availableLanguages": ["en", "de"],
    "theme": "default"
  }
}
```

### Key Sections

#### Features
Controls which system features are enabled:
- `recording` - Video recording capabilities
- `streaming` - RTSP/WebRTC streaming
- `onvif` - ONVIF protocol support
- `webrtc` - WebRTC streaming
- `pip` - Picture-in-picture mode
- `zoom` - Digital zoom functionality
- `autoRotate` - Automatic rotation detection

#### Hardware
Defines hardware-specific capabilities:
- `cameraHeads` - Number of camera inputs
- `maxResolution` - Maximum video resolution
- `maxFps` - Maximum frames per second
- `hasLightControl` - Integrated lighting control
- `hasRotationMotor` - Motorized rotation platform
- `hasFpgaTemp` - FPGA temperature monitoring

#### Network
Network configuration defaults:
- `defaultDhcp` - Use DHCP by default
- `allowStaticIp` - Allow manual IP configuration
- `allowWifi` - Enable WiFi support
- `defaultHostname` - Default network hostname

## License Configuration

### Structure

```json
{
  "licenseType": "commercial",
  "expirationDate": null,
  "maxCameras": 2,
  "features": {
    "recording": true,
    "cloudUpload": false,
    "advancedAnalytics": false
  },
  "customer": {
    "name": "Acme Corporation",
    "id": "ACME-001",
    "support": "premium"
  },
  "restrictions": {
    "maxRecordingDays": 365,
    "maxUsers": 10,
    "watermark": false
  }
}
```

### License Types

- **commercial** - Full-featured commercial license
- **educational** - Educational institution license with restrictions
- **demo** - Time-limited demonstration license
- **development** - Development and testing only

## Style Variables Configuration

Customize UI appearance without code changes:

```json
{
  "colors": {
    "primary": "#123345",
    "secondary": "#FF6B35",
    "accent": "#FFA500",
    "background": "#FFFFFF",
    "text": "#333333"
  },
  "branding": {
    "logo": "custom-logo.svg",
    "favicon": "custom-favicon.ico",
    "companyName": "Custom Medical Equipment"
  },
  "layout": {
    "showCompanyLogo": true,
    "compactMode": false,
    "hideAdvancedSettings": true
  }
}
```

## Build Integration

### Configuration Selection

The build system selects configuration using the `CONFIG_VARIANT` environment variable:

```bash
# Build with specific configuration
CONFIG_VARIANT=rc_DMG nim c rotordream.nim

# Or use build script
nim c -r tools/buildRelease.nim --variant=rc_DMG
```

### Resource Embedding

The `buildResourceConfigs.nim` tool embeds configuration files into the binary:

```nim
# Embeds all files from selected config directory
proc embedConfig*(variant: string) =
  let configDir = "rsc_config" / "config_" & variant
  for file in walkDirRec(configDir):
    let resourceKey = file.relativePath(configDir)
    embedResource(resourceKey, readFile(file))
```

## Runtime Access

### Loading Configuration

```nim
import ./state/factory_config

# Access factory configuration
let config = getFactoryConfig()

if config.features.recording:
  initRecordingSystem()

if config.hardware.hasLightControl:
  initLightControl()
```

### Configuration Precedence

1. **Embedded factory config** - Compiled into binary
2. **Decrypted runtime config** - For licensed features
3. **User settings** - Stored in LocalStorage
4. **Default values** - Hardcoded fallbacks

## Configuration Variants

### config_DEFAULT
Minimal configuration for basic functionality. Used when no specific variant is selected.

### config_DEMO
- Time-limited operation (30 days)
- Watermark on video output
- Limited recording capacity
- All features enabled for evaluation

### config_DEV
- Extended logging enabled
- Debug endpoints exposed
- Relaxed security for development
- Simulator mode available

### config_EDU
- Educational institution branding
- Extended recording retention
- Multi-user collaboration features
- Reduced cost tier

### config_rc_DMG
- RotoClear DMG product line
- Dual camera head support
- Integrated rotation control
- Medical-grade recording quality

### config_VB
- Customer-specific customization
- Custom branding and colors
- Specialized workflow integration
- Unique feature set

## Security Considerations

### Encryption
- `license_config.json` is encrypted in production builds
- Decryption key stored in secure hardware element
- Configuration integrity verified at startup

### Tampering Prevention
- Configuration embedded in binary
- Runtime modification disabled in release builds
- Signature verification for updates

## Best Practices

### Creating New Variants

1. **Copy base configuration**
   ```bash
   cp -r rsc_config/config_DEFAULT rsc_config/config_NEWVARIANT
   ```

2. **Customize configuration files**
   - Update `factory_config.json` with specific settings
   - Add custom assets to `imgs/` directory
   - Modify `version_flavor` file

3. **Test thoroughly**
   ```bash
   CONFIG_VARIANT=NEWVARIANT nim c rotordream.nim
   ./rotordream
   ```

4. **Document changes**
   - Update this documentation
   - Add variant to CI/CD pipeline
   - Document customer-specific requirements

### Configuration Validation

Always validate configuration files before building:

```bash
# Validate JSON syntax
nim c -r tools/validateConfig.nim rsc_config/config_rc_DMG/factory_config.json

# Test configuration loading
nim c -r tests/test_factory_config.nim
```

## Troubleshooting

### Configuration Not Loaded

**Problem**: System uses default settings instead of variant configuration.

**Solution**:
- Verify `CONFIG_VARIANT` environment variable is set
- Check configuration directory exists
- Ensure `buildResourceConfigs.nim` was executed

### License Validation Fails

**Problem**: License configuration rejected at startup.

**Solution**:
- Verify license file encryption/decryption keys
- Check expiration date
- Validate JSON structure

### Custom Assets Not Displayed

**Problem**: Custom logos or images don't appear in UI.

**Solution**:
- Verify files exist in `imgs/` directory
- Check file paths in `style_variables_config.json`
- Ensure assets are embedded during build

## Related Documentation

- [Deployment Variants](deployment-variants.md)
- [License Configuration](license-config.md)
- [Build and Deploy](../operations/build-and-deploy.md)
- [Environments](environments.md)
