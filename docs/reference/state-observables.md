# State Observables Reference

## Overview

This document provides a comprehensive reference of all state observables in the C Pro camera system. Observables are the core state management mechanism, providing reactive updates and persistent storage.

## Observable System

### Core Concepts

```nim
type
  Observable* = ref object
    key*: string                    # Unique identifier
    value: JsonNode                 # Current value
    default*: JsonNode              # Default value
    save*: bool                     # Persist to LocalStorage
    permissionRead*: StatePermissions   # Read permissions required
    permissionWrite*: StatePermissions  # Write permissions required
    isOnlyAskState*: bool          # Action-only (not persistent state)
```

### Observable Categories

- **Device Control**: Camera, motor, light settings
- **Media Management**: Recording, streaming, tags
- **Network Configuration**: IP, hostname, services
- **Storage**: Paths, space monitoring
- **System**: Info, time, updates
- **User Management**: Users, roles, sessions

## Device Observables

### Camera Settings

#### `activeCameraHead`
- **Type**: Integer (0 = Primary, 1 = Secondary)
- **Default**: `0`
- **Permissions**: Read: `Device_r, Device_rw` | Write: `Device_rw`
- **Saved**: No
- **Description**: Currently active camera head (rc_DMG variant)

#### `cameraHeadSettings`
- **Type**: Object
- **Default**:
```json
{
  "primary": {"device": "/dev/video0", "format": "NV12", "resolution": "1920x1080", "fps": 60},
  "secondary": {"device": "/dev/video1", "format": "NV12", "resolution": "1920x1080", "fps": 60}
}
```
- **Permissions**: Read: `Device_r, Device_rw` | Write: `Device_rw`
- **Saved**: Yes
- **Description**: Configuration for each camera head

#### `imageSettings`
- **Type**: Object
- **Default**:
```json
{
  "brightness": 50,
  "contrast": 50,
  "saturation": 50,
  "hue": 0,
  "sharpness": 50,
  "gamma": 100
}
```
- **Permissions**: Read: `Device_r, Device_rw` | Write: `Device_rw`
- **Saved**: Yes
- **Description**: Image adjustment parameters

### Motor Control

#### `discRotation`
- **Type**: Object
- **Default**:
```json
{
  "enabled": false,
  "direction": "stopped",
  "speed": 0,
  "position": 0
}
```
- **Permissions**: Read: `Device_r, Device_rw` | Write: `Device_rw`
- **Saved**: No
- **Description**: Rotation motor control (rc_DMG variant)

#### `autoRotate`
- **Type**: Object
- **Default**:
```json
{
  "enabled": false,
  "sensitivity": 5,
  "threshold": 10
}
```
- **Permissions**: Read: `Device_r, Device_rw` | Write: `Device_rw`
- **Saved**: Yes
- **Description**: Automatic rotation detection settings

### Lighting

#### `lightEnabled`
- **Type**: Boolean
- **Default**: `true`
- **Permissions**: Read: `Device_r, Device_rw` | Write: `Device_rw`
- **Saved**: Yes
- **Description**: Light power state

#### `lightIntensity`
- **Type**: Integer (0-100)
- **Default**: `100`
- **Permissions**: Read: `Device_r, Device_rw` | Write: `Device_rw`
- **Saved**: Yes
- **Description**: Light brightness percentage

#### `lightTemperature`
- **Type**: Integer (Kelvin)
- **Default**: `5500`
- **Permissions**: Read: `Device_r, Device_rw` | Write: `Device_rw`
- **Saved**: Yes
- **Description**: Color temperature in Kelvin

## Media Observables

### Recording

#### `recordingState`
- **Type**: String (`"stopped"`, `"recording"`, `"paused"`)
- **Default**: `"stopped"`
- **Permissions**: Read: `Media_r, Media_rw` | Write: `Media_rw`
- **Saved**: No
- **Description**: Current recording state

#### `recordingMode`
- **Type**: String (`"video"`, `"timelapse"`, `"slowmotion"`)
- **Default**: `"video"`
- **Permissions**: Read: `Media_r, Media_rw` | Write: `Media_rw`
- **Saved**: Yes
- **Description**: Recording mode selection

#### `currentRecordingFile`
- **Type**: String
- **Default**: `""`
- **Permissions**: Read: `Media_r, Media_rw` | Write: -
- **Saved**: No
- **Description**: Filename of active recording

### Streaming

#### `rtspEnabled`
- **Type**: Boolean
- **Default**: `true`
- **Permissions**: Read: `Media_r, Media_rw` | Write: `Media_rw`
- **Saved**: Yes
- **Description**: RTSP server enabled

#### `rtspPort`
- **Type**: Integer
- **Default**: `8554`
- **Permissions**: Read: `Media_r, Media_rw` | Write: `Media_rw`
- **Saved**: Yes
- **Description**: RTSP server port

#### `streamResolution`
- **Type**: String
- **Default**: `"1920x1080"`
- **Permissions**: Read: `Media_r, Media_rw` | Write: `Media_rw`
- **Saved**: Yes
- **Description**: Stream resolution (WIDTHxHEIGHT)

#### `streamFramerate`
- **Type**: Integer
- **Default**: `60`
- **Permissions**: Read: `Media_r, Media_rw` | Write: `Media_rw`
- **Saved**: Yes
- **Description**: Stream frames per second

#### `streamBitrate`
- **Type**: Integer
- **Default**: `8000000`
- **Permissions**: Read: `Media_r, Media_rw` | Write: `Media_rw`
- **Saved**: Yes
- **Description**: Stream bitrate in bits/second

### Tags and Categories

#### `categories`
- **Type**: Object
- **Default**: `{}`
- **Permissions**: Read: `Media_r, Media_rw` | Write: -
- **Saved**: Yes
- **Description**: Tag category definitions (preserved across factory reset per #150)

#### `categoryCounter`
- **Type**: Integer
- **Default**: `1`
- **Permissions**: Read: - | Write: -
- **Saved**: Yes
- **Description**: Auto-increment counter for category IDs

#### `changeTagCategory`
- **Type**: Object (action-only)
- **Default**: `{}`
- **Permissions**: Read: `Media_r, Media_rw` | Write: `Media_rw`
- **Saved**: No
- **Description**: Create/update/delete tag categories

## Network Observables

### Network Configuration

#### `hostname`
- **Type**: String
- **Default**: `"rotoclear"`
- **Permissions**: Read: `Network_r, Network_rw` | Write: `Network_rw`
- **Saved**: Yes
- **Description**: System hostname

#### `dhcpEnabled`
- **Type**: Boolean
- **Default**: `true`
- **Permissions**: Read: `Network_r, Network_rw` | Write: `Network_rw`
- **Saved**: Yes
- **Description**: Use DHCP for IP address

#### `ipAddress`
- **Type**: String
- **Default**: `""`
- **Permissions**: Read: `Network_r, Network_rw` | Write: `Network_rw`
- **Saved**: Yes
- **Description**: Static IP address (when DHCP disabled)

#### `subnetMask`
- **Type**: String
- **Default**: `"255.255.255.0"`
- **Permissions**: Read: `Network_r, Network_rw` | Write: `Network_rw`
- **Saved**: Yes
- **Description**: Network subnet mask

#### `gateway`
- **Type**: String
- **Default**: `""`
- **Permissions**: Read: `Network_r, Network_rw` | Write: `Network_rw`
- **Saved**: Yes
- **Description**: Default gateway

#### `dnsServers`
- **Type**: Array of Strings
- **Default**: `["8.8.8.8", "8.8.4.4"]`
- **Permissions**: Read: `Network_r, Network_rw` | Write: `Network_rw`
- **Saved**: Yes
- **Description**: DNS server addresses

## Storage Observables

### Storage Management

#### `recordingStorage`
- **Type**: Object
- **Default**:
```json
{
  "primary": "/media/data/recordings",
  "backup": "/media/backup/recordings",
  "network": ""
}
```
- **Permissions**: Read: `Storage_r, Storage_rw` | Write: `Storage_rw`
- **Saved**: Yes
- **Description**: Recording storage locations

#### `storageDevices`
- **Type**: Array
- **Default**: `[]`
- **Permissions**: Read: `Storage_r, Storage_rw` | Write: -
- **Saved**: No
- **Description**: Available storage devices (dynamic)

#### `storageSpace`
- **Type**: Object (dynamic)
- **Default**: `{}`
- **Permissions**: Read: `Storage_r, Storage_rw` | Write: -
- **Saved**: No
- **Description**: Storage space statistics

### Network Storage

#### `netStorageEnabled`
- **Type**: Boolean
- **Default**: `false`
- **Permissions**: Read: `Storage_r, Storage_rw` | Write: `Storage_rw`
- **Saved**: Yes
- **Description**: Enable network storage (NFS/SMB)

#### `netStoragePath`
- **Type**: String
- **Default**: `""`
- **Permissions**: Read: `Storage_r, Storage_rw` | Write: `Storage_rw`
- **Saved**: Yes
- **Description**: Network storage mount path

## System Observables

### System Information

#### `systemInfo`
- **Type**: Object (read-only)
- **Default**: `{}`
- **Permissions**: Read: `System_r, System_rw` | Write: -
- **Saved**: No
- **Description**: System hardware and software info

#### `cpuUsage`
- **Type**: Float
- **Default**: `0.0`
- **Permissions**: Read: `System_r, System_rw` | Write: -
- **Saved**: No
- **Description**: Current CPU usage percentage

#### `memoryUsage`
- **Type**: Object
- **Default**: `{"used": 0, "total": 0, "percent": 0}`
- **Permissions**: Read: `System_r, System_rw` | Write: -
- **Saved**: No
- **Description**: Memory usage statistics

#### `fpgaTemperature`
- **Type**: Float
- **Default**: `25.0`
- **Permissions**: Read: `Device_r, Device_rw` | Write: -
- **Saved**: No
- **Description**: FPGA temperature in Celsius (rc_DMG variant)

### Time and Date

#### `time`
- **Type**: String (ISO 8601)
- **Default**: Current time
- **Permissions**: Read: `System_r, System_rw` | Write: -
- **Saved**: No
- **Description**: Current system time

#### `timezone`
- **Type**: String
- **Default**: `"UTC"`
- **Permissions**: Read: `System_r, System_rw` | Write: `System_rw`
- **Saved**: Yes
- **Description**: System timezone

#### `ntpEnabled`
- **Type**: Boolean
- **Default**: `true`
- **Permissions**: Read: `Network_r, Network_rw` | Write: `Network_rw`
- **Saved**: Yes
- **Description**: Enable NTP time synchronization

#### `ntpServers`
- **Type**: Array of Strings
- **Default**: `["pool.ntp.org"]`
- **Permissions**: Read: `Network_r, Network_rw` | Write: `Network_rw`
- **Saved**: Yes
- **Description**: NTP server addresses

### Firmware and Updates

#### `swVersionNumber`
- **Type**: String
- **Default**: Build version
- **Permissions**: Read: `System_r, System_rw, FirmwareUpdate_r, FirmwareUpdate_rw` | Write: -
- **Saved**: Yes
- **Description**: Software version number

#### `updateAvailable`
- **Type**: Boolean
- **Default**: `false`
- **Permissions**: Read: `FirmwareUpdate_r, FirmwareUpdate_rw` | Write: -
- **Saved**: No
- **Description**: Firmware update available flag

## User Observables

### User Management

#### `users`
- **Type**: Object
- **Default**: `{}`
- **Permissions**: Read: `User_r, User_rw` | Write: `User_rw`
- **Saved**: Yes
- **Description**: User accounts and roles

#### `userPasswords`
- **Type**: Object
- **Default**: `{}`
- **Permissions**: Read: - | Write: `User_rw`
- **Saved**: Yes
- **Description**: Hashed passwords (never readable)

#### `currentUser`
- **Type**: String
- **Default**: `""`
- **Permissions**: Read: All authenticated | Write: -
- **Saved**: No
- **Description**: Currently authenticated user

## Action Observables

### System Actions

#### `restart`
- **Type**: Boolean (action-only)
- **Default**: `false`
- **Permissions**: Read: `Reboot_rw` | Write: `Reboot_rw`
- **Saved**: No
- **Description**: Trigger system restart

#### `reset`
- **Type**: Boolean (action-only)
- **Default**: `false`
- **Permissions**: Read: `FirmwareUpdate_rw` | Write: `FirmwareUpdate_rw`
- **Saved**: No
- **Description**: Factory reset (preserves categories per #150)

#### `systemReboot`
- **Type**: Boolean (action-only)
- **Default**: `false`
- **Permissions**: Read: `Reboot_rw` | Write: `Reboot_rw`
- **Saved**: No
- **Description**: Reboot system

## Usage Examples

### Reading Observable State

```nim
# Get observable
let recordingState = State.get("recordingState")

# Read current value
let isRecording = recordingState.value.getStr == "recording"

# Access with permissions check
if userPermissions.canRead(recordingState):
  echo "Recording state: ", recordingState.value
```

### Writing Observable State

```nim
# Get observable
let streamBitrate = State.get("streamBitrate")

# Update value (triggers save if save=true)
streamBitrate.updateValue(%8000000)

# With permissions check
if userPermissions.canWrite(streamBitrate):
  streamBitrate.updateValue(%newBitrate)
```

### Observing Changes

```nim
# Subscribe to changes
let recording = State.get("recordingState")
recording.onchange.subscribe proc(obs: Observable) =
  echo "Recording state changed to: ", obs.value
```

## Related Documentation

- [State Management](../architecture/state-management.md)
- [Observable Pattern](../architecture/state-management.md#observable-pattern)
- [Permissions](../security/permissions.md)
- [API Reference](../api/websocket-api.md)
