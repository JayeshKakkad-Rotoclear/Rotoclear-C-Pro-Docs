# Environment Configuration

**Multi-environment configuration system for different deployment scenarios.**

## Configuration Overview

The Rotoclear Camera Server uses a multi-environment configuration system located in `rsc_config/` with separate configurations for different deployment scenarios.

## Environment Variants

| Environment | Directory | Purpose | Target |
|-------------|-----------|---------|---------|
| **DEFAULT** | `config_DEFAULT/` | Base configuration | Fallback |
| **DEV** | `config_DEV/` | Development | Local development |
| **DEMO** | `config_DEMO/` | Demonstration | Demo systems |
| **EDU** | `config_EDU/` | Educational | Educational institutions |
| **VB** | `config_VB/` | Version B | Variant B hardware |
| **DMG** | `config_rc_DMG/` | DMG Variant | DMG specific deployment |

## Configuration Files

### Factory Configuration (`factory_config.json`)

Controls core system behavior and server settings.

**Development Example** (`config_DEV/factory_config.json`):
```json
{
  "oneWebserverIsAlwaysRunning": true,
  "httpOn": true,
  "httpsOn": true,
  "discRotation": false,
  "rpm": 4000
}
```

**DMG Production Example** (`config_rc_DMG/factory_config.json`):
```json
{
  "oneWebserverIsAlwaysRunning": true,
  "httpOn": true,
  "httpsOn": true,
  "discRotation": true,
  "rpm": 6000,
  "httpPort": 80,
  "httpsPort": 443
}
```

#### Factory Configuration Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `oneWebserverIsAlwaysRunning` | boolean | Keep web server active | `true` |
| `httpOn` | boolean | Enable HTTP server | `true` |
| `httpsOn` | boolean | Enable HTTPS server | `false` |
| `discRotation` | boolean | Enable disc rotation motor | `false` |
| `rpm` | integer | Rotation speed (RPM) | `4000` |
| `httpPort` | integer | HTTP server port | `3000` |
| `httpsPort` | integer | HTTPS server port | `3001` |

### License Configuration (`license_config.json`)

Controls feature licensing and capabilities.

**DMG Example** (`config_rc_DMG/license_config.json`):
```json
{
  "stream4K": false
}
```

**EDU Example** (`config_EDU/license_config.json`):
```json
{
  "stream4K": true,
  "advancedRecording": true,
  "networkStorage": false
}
```

> TODO: Document complete license configuration options

### Version Flavor (`version_flavor`)

Identifies the specific variant or flavor of the deployment.

**Examples:**
- `config_DEMO/version_flavor`: Contains deployment-specific identifier
- `config_EDU/version_flavor`: Educational version identifier
- `config_VB/version_flavor`: Version B hardware identifier

### Style Configuration (`style_variables_config.json`)

UI styling and theming configuration (DMG variant):

```json
{
  "primaryColor": "#2196F3",
  "secondaryColor": "#FFC107",
  "backgroundColor": "#FAFAFA",
  "textColor": "#212121"
}
```

> TODO: Document complete style configuration options

## Asset Management

### Images Directory Structure

Each environment can include custom images:

```
config_EDU/
├── imgs/
│   ├── logo.png
│   ├── background.jpg
│   └── icons/
└── hdmi_imgs/
    ├── splash.png
    └── overlay.png
```

### Stylesheets

Custom CSS files for web interface theming:

```
config_rc_DMG/
└── stylesheets/
    ├── main.css
    ├── mobile.css
    └── themes/
```

## Configuration Selection

### Build-time Selection

Configuration is selected during the build process using environment-specific flags:

```bash
# Build with DEV configuration
nim c -d:config=DEV rotordream.nim

# Build with DMG configuration  
nim c -d:config=DMG rotordream.nim
```

### Runtime Configuration Loading

The application loads configuration from the appropriate directory at startup:

```nim
# From src/state/factory_config.nim (inferred)
proc loadFactoryConfig*(environment: string): FactoryConfig =
  let configPath = fmt"rsc_config/config_{environment}/factory_config.json"
  # Load and parse configuration
```

## Local Development Configuration

### Development Factory Config

Create `config_rc/factory_config.json` for local development:

```json
{
  "oneWebserverIsAlwaysRunning": true,
  "httpOn": true,
  "httpsOn": false,
  "discRotation": false,
  "rpm": 4000,
  "httpPort": 3000,
  "httpsPort": 3001
}
```

### Environment Variables

Configure runtime behavior with environment variables:

```bash
# Target device configuration
export C3_BOX_IP="192.168.1.100"
export C3_BOX_PW="admin"

# Alternative IP configuration
export ROTOCLEAR_IP="rotoclear-cam.local"
```

## Deployment Configuration

### Cross-compilation Flags

Different configurations require different compilation flags (from `tools/common.nim`):

```nim
# ARM32 embedded system
proc getEmbeddedFlags*(isArm32: bool = true): string =
  result.add(" -d:directCompile=true -d:embeddedSystem")
  
  if isArm32:
    # ARM32 specific libraries
    for (kind, path) in walkDir("libs-petalinux"):
      result.add "-L:" & path & " "
  else:
    # ARM64 specific configuration
    result.add(" --cpu:arm64 --os:linux")
```

### Remote Deployment

Configuration deployment via SSH (from `tools/remoteRelease.nim`):

```bash
# Deploy specific configuration
nim c -r tools/remoteRelease.nim DMG

# Deploy with custom target
C3_BOX_IP="192.168.1.200" nim c -r tools/remoteRelease.nim EDU
```

## Configuration Validation

### Required Files

Each configuration environment should include:

- `factory_config.json` - Core system configuration
- `version_flavor` - Version identification
- `license_config.json` - Feature licensing (optional)

### Validation Checklist

- [ ] JSON syntax is valid
- [ ] Required properties are present
- [ ] Port numbers don't conflict
- [ ] Image assets exist if referenced
- [ ] Permissions are appropriate for target system

## Configuration Inheritance

### Default Fallback

If a configuration file is missing from an environment, the system falls back to:

1. `config_DEFAULT/` directory
2. Built-in defaults in source code
3. Safe fallback values

### Override Hierarchy

```
Built-in defaults
    ↓
config_DEFAULT/
    ↓
config_<ENVIRONMENT>/
    ↓
Runtime environment variables
```

## Troubleshooting

### Common Issues

**Missing Configuration File:**
```
Error: Could not load factory_config.json
Solution: Ensure file exists in config_<ENV>/ directory
```

**Invalid JSON:**
```
Error: JSON parsing failed
Solution: Validate JSON syntax with online validator
```

**Port Conflicts:**
```
Error: Address already in use
Solution: Change httpPort/httpsPort in factory_config.json
```

### Configuration Debugging

Enable configuration debugging:

```bash
nim c -r -d:ConfigDebug=true rotordream.nim
```

## Best Practices

1. **Version Control**: Keep all configurations in version control
2. **Documentation**: Document custom configurations in comments
3. **Validation**: Test configurations before deployment
4. **Backup**: Maintain backups of working configurations
5. **Security**: Don't commit sensitive credentials

## Related Documentation

- [Getting Started - Local Configuration](../getting-started.md#environment-configuration)
- [Build and Deploy](../operations/build-and-deploy.md)
- [Security Configuration](../security/authentication.md)

---

*Configuration documentation derived from analysis of `rsc_config/` directories and build scripts*
