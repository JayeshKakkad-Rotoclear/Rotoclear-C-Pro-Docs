# License Configuration

## Overview

The license configuration system controls feature availability, usage limits, and commercial terms for RotoClear camera deployments. It supports various licensing models from perpetual to subscription-based.

## License Types

### Commercial License
Full-featured license for commercial deployments:
- Unlimited recording duration
- All features enabled
- Commercial support included
- No watermarks or restrictions
- Software updates included

### Educational License
Discounted license for educational institutions:
- Extended recording retention
- Multi-user support
- Educational pricing
- Limited to academic use
- Community support

### Demo License
Time-limited evaluation license:
- 30-day evaluation period
- All features enabled
- Watermark on output
- Technical support during trial
- Easy upgrade path

### Development License
Development and testing only:
- No production use
- Extended logging enabled
- Debug features accessible
- Simulator mode available
- No encryption requirements

## License File Format

### Structure

```json
{
  "version": 1,
  "licenseType": "commercial",
  "issuedTo": {
    "organization": "Acme Medical Center",
    "customerId": "ACME-MED-001",
    "contact": "admin@acmemedical.com"
  },
  "validity": {
    "issuedDate": "2025-01-01T00:00:00Z",
    "expirationDate": "2026-01-01T00:00:00Z",
    "gracePerodDays": 30
  },
  "features": {
    "recording": {
      "enabled": true,
      "maxDurationDays": 365,
      "formats": ["mp4", "avi"]
    },
    "streaming": {
      "enabled": true,
      "protocols": ["rtsp", "webrtc"],
      "maxConcurrentClients": 10
    },
    "onvif": {
      "enabled": true,
      "version": "2.0"
    },
    "cloudIntegration": {
      "enabled": false,
      "provider": null
    },
    "analytics": {
      "enabled": false,
      "modules": []
    }
  },
  "hardware": {
    "maxCameraHeads": 2,
    "maxResolution": "3840x2160",
    "maxFps": 60
  },
  "users": {
    "maxUsers": 10,
    "roles": ["admin", "operator", "viewer"]
  },
  "storage": {
    "localEnabled": true,
    "networkEnabled": true,
    "cloudEnabled": false,
    "maxStorageGB": null
  },
  "support": {
    "level": "premium",
    "responseTimeSLA": "4h",
    "phone": "+1-800-ROTOCLEAR",
    "email": "support@rotoclear.com"
  },
  "restrictions": {
    "watermark": false,
    "offlineMode": true,
    "transferable": false
  },
  "cryptography": {
    "encrypted": true,
    "algorithm": "AES-256-GCM",
    "signatureRequired": true
  }
}
```

## License Validation

### Runtime Validation

The system validates licenses at startup and periodically during operation:

```nim
import ./state/rc_licenses

proc validateLicense*(): LicenseStatus =
  let license = loadLicense()
  
  # Check expiration
  if license.validity.expirationDate < now():
    if (now() - license.validity.expirationDate).inDays > license.validity.gracePerodDays:
      return LicenseStatus.Expired
    else:
      return LicenseStatus.GracePeriod
  
  # Check signature
  if license.cryptography.signatureRequired:
    if not verifySignature(license):
      return LicenseStatus.Invalid
  
  # Check hardware binding
  if not validateHardwareBinding(license):
    return LicenseStatus.HardwareMismatch
  
  return LicenseStatus.Valid
```

### Validation Checks

1. **Signature verification** - Cryptographic signature validation
2. **Expiration check** - Compare current date with expiration
3. **Hardware binding** - Verify system hardware matches license
4. **Feature flags** - Validate requested features are licensed
5. **Usage limits** - Check current usage against license limits

## License Installation

### Via Web Interface

1. Navigate to **Settings > License**
2. Click **Upload License File**
3. Select `license_config.json` file
4. System validates and activates license
5. Restart required for full activation

### Via Command Line

```bash
# Copy license file to system
scp license_config.json root@rotoclear:/tmp/

# Install license
ssh root@rotoclear
cd /config
cp /tmp/license_config.json .
systemctl restart rotordream
```

### Encrypted License Installation

For production systems with encrypted licenses:

```bash
# License comes pre-encrypted
# Copy to decrypted_rsc directory
cp encrypted_license.json /config/decrypted_rsc/license_config.json

# System automatically decrypts on startup
systemctl restart rotordream
```

## License Generation

### Using License Generator Tool

```bash
# Generate new license
nim c -r licenser/licenser.nim generate \
  --customer="Acme Medical" \
  --type=commercial \
  --duration=365 \
  --features=all \
  --output=license_config.json

# Encrypt license for production
nim c -r fcrypter/fcrypter.nim encrypt \
  --input=license_config.json \
  --output=encrypted_license.json \
  --key-file=master.key
```

### License Parameters

- `--customer` - Organization name
- `--type` - License type (commercial, educational, demo, dev)
- `--duration` - Validity period in days
- `--features` - Comma-separated feature list or "all"
- `--max-cameras` - Maximum camera heads
- `--max-users` - Maximum concurrent users
- `--hardware-id` - Bind to specific hardware (optional)

## Feature Enforcement

### Runtime Feature Checks

```nim
# Check if feature is licensed
if State.get("licenseRecordingEnabled").value.getBool:
  startRecording()
else:
  showLicenseError("Recording not enabled in license")

# Check usage limits
let currentUsers = getActiveUsers().len
let maxUsers = State.get("licenseMaxUsers").value.getInt
if currentUsers >= maxUsers:
  rejectNewConnection("Maximum users reached")
```

### Observable Integration

License features are exposed as observables:

- `licenseType` - License type string
- `licenseValid` - Boolean validity status
- `licenseExpirationDate` - Expiration timestamp
- `licenseRecordingEnabled` - Recording feature flag
- `licenseStreamingEnabled` - Streaming feature flag
- `licenseMaxUsers` - Maximum user count
- `licenseMaxCameras` - Maximum camera heads

## Hardware Binding

### Binding Mechanism

Licenses can be bound to specific hardware to prevent unauthorized transfers:

```nim
proc generateHardwareId*(): string =
  # Combine multiple hardware identifiers
  let cpuSerial = getCpuSerialNumber()
  let macAddress = getMacAddress("eth0")
  let boardSerial = getBoardSerialNumber()
  
  # Create unique hash
  result = sha256(cpuSerial & macAddress & boardSerial).toHex()
```

### Binding Strategies

1. **CPU Serial** - Bind to processor serial number
2. **MAC Address** - Bind to network interface
3. **Board Serial** - Bind to hardware board serial
4. **Combined** - Use combination for stronger binding

## License Expiration Handling

### Expiration States

1. **Valid** - License within validity period
2. **Grace Period** - Expired but within grace period
3. **Expired** - Past grace period, features disabled
4. **Revoked** - License explicitly revoked

### Grace Period Behavior

During grace period (default 30 days):
- System continues operating with warnings
- Warning notifications displayed in UI
- Email notifications sent to administrator
- Recording continues but watermark added
- Streaming remains available

After grace period:
- Recording disabled
- Streaming limited to local network
- ONVIF access restricted
- Administrative functions only

## Subscription Licensing

### Subscription Model

For subscription-based licenses:

```json
{
  "licenseType": "subscription",
  "subscription": {
    "tier": "premium",
    "billingCycle": "monthly",
    "autoRenew": true,
    "paymentStatus": "current"
  },
  "validity": {
    "currentPeriodEnd": "2025-02-01T00:00:00Z",
    "renewalUrl": "https://portal.rotoclear.com/renew"
  }
}
```

### Online Validation

Subscription licenses require periodic online validation:

```nim
# Check license status with licensing server
proc validateOnline*(): Future[LicenseStatus] {.async.} =
  let response = await httpClient.get(
    "https://license.rotoclear.com/validate",
    headers = {"X-Hardware-ID": getHardwareId()}
  )
  
  if response.status == 200:
    let status = parseJson(response.body)
    return status["valid"].getBool
```

## Troubleshooting

### License Not Recognized

**Symptoms**: System operates in demo mode despite license installation.

**Solutions**:
- Verify license file location (`/config/decrypted_rsc/license_config.json`)
- Check file permissions (should be readable by rotordream process)
- Review startup logs for license validation errors
- Ensure license is properly encrypted/decrypted

### Hardware Binding Mismatch

**Symptoms**: License shows as invalid on target hardware.

**Solutions**:
- Verify hardware ID matches license: `cat /config/hardware_id`
- Contact support for license transfer
- Request hardware-id update for license
- Use non-hardware-bound license for development

### Expired License

**Symptoms**: Features disabled, expiration warnings displayed.

**Solutions**:
- Check current date and time settings
- Verify system clock is synchronized (NTP)
- Contact support for license renewal
- Upload new license file

### Feature Not Available

**Symptoms**: Feature appears disabled despite license.

**Solutions**:
- Review license file features section
- Check observable values: `curl http://localhost:8080/api/state`
- Verify factory configuration allows feature
- Restart system after license change

## Security Best Practices

### License Storage

- Store licenses in secure directory with restricted permissions
- Use encrypted licenses for production deployments
- Never commit license files to version control
- Rotate encryption keys periodically

### License Distribution

- Use secure channels for license delivery (encrypted email, HTTPS)
- Validate license recipient before distribution
- Track license installations and activations
- Implement revocation mechanism for compromised licenses

### Audit Logging

Enable comprehensive license audit logging:

```nim
# Log all license-related events
proc auditLog(event: string, details: JsonNode) =
  StateLogger.info("LICENSE_AUDIT", event, details)

auditLog("license_installed", %{
  "customer": license.issuedTo.organization,
  "expiration": license.validity.expirationDate,
  "features": license.features
})
```

## Related Documentation

- [Factory Configuration](factory-config.md)
- [Authentication](../security/authentication.md)
- [Permissions](../security/permissions.md)
- [Build and Deploy](../operations/build-and-deploy.md)
