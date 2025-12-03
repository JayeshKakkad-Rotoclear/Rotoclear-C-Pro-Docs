# SSL Certificates

## Overview

The RotoClear camera system supports SSL/TLS encryption for secure communication. SSL certificates protect web interface access, API calls, and streaming protocols from eavesdropping and man-in-the-middle attacks.

## Certificate Management

### Certificate Storage

```
/config/
├── server.crt       # SSL certificate
├── server.key       # Private key
└── ca.crt          # Certificate Authority (optional)
```

**Configuration**:
```nim
# src/settings.nim
const
  CrtDir* = when defined(embeddedSystem): "/config/server.crt"
            else: getCurrentDir() / "server.crt"
  
  KeyDir* = when defined(embeddedSystem): "/config/server.key"
            else: getCurrentDir() / "server.key"
```

### Self-Signed Certificates

Generate self-signed certificate for development/testing:

```bash
# Generate private key
openssl genrsa -out server.key 2048

# Generate self-signed certificate (valid for 365 days)
openssl req -new -x509 -key server.key -out server.crt -days 365 \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=rotoclear.local"

# Copy to device
scp server.crt server.key root@rotoclear:/config/
```

### Certificate Authority (CA) Signed

For production deployments, use CA-signed certificates:

```bash
# Generate private key
openssl genrsa -out server.key 2048

# Generate certificate signing request (CSR)
openssl req -new -key server.key -out server.csr \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=rotoclear.example.com"

# Submit CSR to Certificate Authority
# Receive signed certificate (server.crt)

# Install certificate and key
scp server.crt server.key root@rotoclear:/config/
ssh root@rotoclear systemctl restart rotordream
```

### Let's Encrypt Certificates

Free certificates from Let's Encrypt:

```bash
# Install certbot
apt-get install certbot

# Obtain certificate (requires port 80 accessible)
certbot certonly --standalone \
  -d rotoclear.example.com \
  --email admin@example.com \
  --agree-tos

# Certificates stored in /etc/letsencrypt/live/rotoclear.example.com/

# Copy to RotoClear device
scp /etc/letsencrypt/live/rotoclear.example.com/fullchain.pem root@rotoclear:/config/server.crt
scp /etc/letsencrypt/live/rotoclear.example.com/privkey.pem root@rotoclear:/config/server.key

# Auto-renewal with cron
echo "0 0 * * * certbot renew --quiet && scp /etc/letsencrypt/live/rotoclear.example.com/*.pem root@rotoclear:/config/" | crontab -
```

## Web Server SSL Configuration

### HTTPS Server Setup

```nim
# src/servers/webserver.nim
import std/net
import std/asynchttpserver

proc startHttpsServer*() =
  let server = newAsyncHttpServer()
  
  # Load SSL context
  let ctx = newContext(
    verifyMode = CVerifyNone,
    certFile = CrtDir,
    keyFile = KeyDir
  )
  
  proc handler(req: Request) {.async.} =
    # Handle HTTPS requests
    await handleHttpRequest(req)
  
  # Start HTTPS server on port 443
  waitFor server.serve(Port(443), handler, ctx)
```

### HTTP to HTTPS Redirect

```nim
proc startHttpRedirectServer*() =
  # Redirect HTTP (port 80) to HTTPS (port 443)
  let server = newAsyncHttpServer()
  
  proc redirectHandler(req: Request) {.async.} =
    let host = req.headers.getOrDefault("Host", "")
    let location = "https://" & host & req.url.path
    
    await req.respond(Http301, "", newHttpHeaders([
      ("Location", location)
    ]))
  
  waitFor server.serve(Port(80), redirectHandler)
```

## RTSP SSL/TLS

### RTSPS Protocol

Secure RTSP over TLS (RTSPS):

```nim
# src/state/rc_rtsp.nim
proc initRtspsServer*() =
  initObservable("rtspsEnabled",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %false  # Disabled by default
  )
  
  initObservable("rtspsPort",
    permissionRead = {Media_r, Media_rw},
    permissionWrite = {Media_rw},
    default = %322,  # RTSPS default port
    validateType = Int
  )
```

**Client Connection**:
```bash
# VLC with RTSPS
vlc rtsps://username:password@rotoclear.local:322/stream1

# FFmpeg with RTSPS
ffmpeg -rtsp_transport tcp \
  -i rtsps://rotoclear.local:322/stream1 \
  -c copy output.mp4
```

## Certificate Validation

### Certificate Information

```nim
proc getCertificateInfo*(): JsonNode =
  try:
    let cert = readFile(CrtDir)
    
    # Parse certificate using OpenSSL
    let x509 = parseCertificate(cert)
    
    result = %{
      "subject": %x509.subject,
      "issuer": %x509.issuer,
      "validFrom": %x509.notBefore.format("yyyy-MM-dd"),
      "validTo": %x509.notAfter.format("yyyy-MM-dd"),
      "daysRemaining": %((x509.notAfter - now()).inDays),
      "isExpired": %(now() > x509.notAfter),
      "isSelfSigned": %(x509.subject == x509.issuer)
    }
  except:
    result = %{"error": "Certificate not found or invalid"}
```

### Certificate Expiration Monitoring

```nim
proc checkCertificateExpiration*() =
  let info = getCertificateInfo()
  
  if info.hasKey("error"):
    Notification.trigger("certificateWarning", "status", "missing")
    return
  
  let daysRemaining = info["daysRemaining"].getInt
  
  if info["isExpired"].getBool:
    Notification.trigger("certificateWarning", "status", "expired")
  elif daysRemaining < 30:
    Notification.trigger("certificateWarning", "status", "expiring")
    Notification.trigger("certificateWarning", "daysRemaining", $daysRemaining)

# Check certificate expiration daily
setInterval(24 * 60 * 60 * 1000):  # 24 hours
  checkCertificateExpiration()
```

## Client Certificate Authentication

### Mutual TLS (mTLS)

Require client certificates for enhanced security:

```nim
proc configureMutualTls*() =
  let ctx = newContext(
    verifyMode = CVerifyPeer,  # Require client certificate
    certFile = CrtDir,
    keyFile = KeyDir,
    caCertFile = "/config/ca.crt"  # Client CA
  )
  
  # Clients must present valid certificate signed by CA
  ctx.wrapSocket(socket)
```

**Client Configuration**:
```bash
# Generate client certificate
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -out client.crt

# Use client certificate with cURL
curl --cert client.crt --key client.key \
  https://rotoclear.local/api/system/info
```

## Certificate Formats

### PEM Format (Recommended)

Text-based format, easy to read and edit:

```
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAKL0UG+mRbRzMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
...
-----END CERTIFICATE-----
```

### DER Format

Binary format, more compact:

```bash
# Convert PEM to DER
openssl x509 -in server.crt -outform der -out server.der

# Convert DER to PEM
openssl x509 -in server.der -inform der -out server.crt
```

### PKCS#12 Format

Combined certificate and key in one file:

```bash
# Create PKCS#12 bundle
openssl pkcs12 -export -out server.p12 \
  -inkey server.key -in server.crt \
  -password pass:secret

# Extract certificate and key
openssl pkcs12 -in server.p12 -out server.crt -clcerts -nokeys -password pass:secret
openssl pkcs12 -in server.p12 -out server.key -nocerts -nodes -password pass:secret
```

## Security Best Practices

### Certificate Security

```bash
# Secure file permissions
chmod 600 /config/server.key      # Private key: owner read/write only
chmod 644 /config/server.crt      # Certificate: world-readable
chown rotordream:rotordream /config/server.*
```

### Key Length

- **Minimum**: 2048-bit RSA keys
- **Recommended**: 4096-bit RSA keys or ECDSA P-256
- **Not recommended**: 1024-bit RSA (insecure)

```bash
# Generate strong 4096-bit key
openssl genrsa -out server.key 4096

# Or use ECDSA (smaller, faster)
openssl ecparam -genkey -name prime256v1 -out server.key
```

### Certificate Renewal

Set calendar reminders for certificate renewal:

- **90 days before expiration**: Plan renewal
- **60 days**: Obtain new certificate
- **30 days**: Install and test new certificate
- **0 days**: Emergency renewal if not completed

## Troubleshooting

### Certificate Not Found

**Symptoms**: SSL/TLS handshake fails, server falls back to HTTP.

**Solutions**:
```bash
# Verify certificate files exist
ls -l /config/server.crt /config/server.key

# Check file permissions
stat /config/server.key

# Review server logs
journalctl -u rotordream | grep -i ssl
```

### Invalid Certificate

**Symptoms**: Browser shows security warning, clients reject connection.

**Solutions**:
```bash
# Verify certificate is valid
openssl x509 -in /config/server.crt -text -noout

# Check certificate matches key
openssl x509 -noout -modulus -in /config/server.crt | openssl md5
openssl rsa -noout -modulus -in /config/server.key | openssl md5
# MD5 hashes should match

# Verify certificate chain
openssl verify -CAfile /config/ca.crt /config/server.crt
```

### Certificate Expired

**Symptoms**: Clients reject connection with expiration error.

**Solutions**:
```bash
# Check expiration date
openssl x509 -in /config/server.crt -noout -enddate

# Renew certificate immediately
# Follow certificate generation process

# Temporary: Use self-signed certificate
openssl req -new -x509 -key /config/server.key \
  -out /config/server.crt -days 365
```

### Mixed Content Warnings

**Symptoms**: Browser shows mixed content warnings on HTTPS pages.

**Solutions**:
- Ensure all resources (images, scripts, CSS) use HTTPS URLs
- Use protocol-relative URLs: `//rotoclear.local/image.jpg`
- Enable HSTS to force HTTPS

## HTTP Strict Transport Security (HSTS)

### Enable HSTS

```nim
proc addHstsHeader*(headers: HttpHeaders) =
  # Force HTTPS for 1 year, include subdomains
  headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

proc handleRequest*(req: Request) {.async.} =
  var headers = newHttpHeaders()
  addHstsHeader(headers)
  
  # ...handle request...
  
  await req.respond(Http200, body, headers)
```

## Certificate Pinning

For enhanced security, pin specific certificates:

```nim
const ExpectedCertFingerprint = "E3:B0:C4:42:98:FC:1C:14:9A:FB:F4:C8:99:6F:B9:24"

proc validateCertificatePin*(cert: Certificate): bool =
  let fingerprint = sha256(cert.raw).toHex()
  return fingerprint == ExpectedCertFingerprint
```

## Related Documentation

- [Authentication](authentication.md)
- [Network Configuration](../configuration/network.md)
- [Security Best Practices](security-best-practices.md)
- [Operations](../operations/troubleshooting.md)
