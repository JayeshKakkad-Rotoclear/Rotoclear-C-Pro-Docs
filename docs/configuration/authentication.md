# Authentication and Security Configuration

**Comprehensive security configuration including authentication, authorization, encryption, and network security.**

## Overview

C Pro implements multi-layered security with role-based access control, secure communication protocols, and comprehensive audit logging.

```mermaid
graph TB
    A[Client Request] --> B{Authentication Layer}
    
    B -->|API Key| C[API Key Validation]
    B -->|JWT Token| D[JWT Validation]
    B -->|Certificate| E[Client Certificate]
    
    C --> F{Authorization Layer}
    D --> F
    E --> F
    
    F -->|Role Check| G[Role-Based Access Control]
    F -->|Permission Check| H[Resource Permissions]
    
    G --> I{Access Decision}
    H --> I
    
    I -->|Allow| J[Request Processing]
    I -->|Deny| K[Access Denied]
    
    J --> L[Audit Logging]
    K --> L
    
    L --> M[Security Events]
    M --> N[SIEM Integration]
    
    style B fill:#ff9999
    style F fill:#99ff99
    style L fill:#9999ff
```

## Authentication Methods

### API Key Authentication

**API Key Management**:
```bash
# Generate new API key
curl -X POST "http://192.168.1.100:8080/api/auth/apikey" \
     -H "Authorization: Bearer admin_token" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "monitoring_client",
       "description": "External monitoring system",
       "expires_in_days": 365,
       "permissions": ["camera:read", "system:read"],
       "ip_restrictions": ["192.168.1.0/24"]
     }'

# Response
{
  "api_key": "1a2B3c4D5e6f7G8h9I0j1K2l3M4n5O6p",
  "key_id": "key_001",
  "created": "2025-01-15T10:30:00Z",
  "expires": "2026-01-15T10:30:00Z",
  "permissions": ["camera:read", "system:read"]
}

# List API keys
curl -H "Authorization: Bearer admin_token" \
     http://192.168.1.100:8080/api/auth/apikeys

# Revoke API key
curl -X DELETE "http://192.168.1.100:8080/api/auth/apikey/key_001" \
     -H "Authorization: Bearer admin_token"
```

**API Key Configuration**:
```ini
# /etc/rotordream/auth.conf
[api_keys]
enabled = true
default_expiry_days = 90
max_keys_per_client = 10
require_ip_restrictions = false
audit_key_usage = true

# Key validation
validate_on_request = true
cache_validation = true
cache_timeout = 300

# Rate limiting per API key
rate_limit_enabled = true
requests_per_minute = 60
burst_allowance = 10
```

### JWT Token Authentication

**JWT Configuration**:
```json
{
  "jwt": {
    "enabled": true,
    "secret_key_file": "/etc/rotordream/jwt_secret",
    "algorithm": "HS256",
    "token_expiry": 3600,
    "refresh_expiry": 86400,
    "issuer": "rotordream-cam",
    "audience": "rotordream-api"
  },
  "token_validation": {
    "validate_issuer": true,
    "validate_audience": true,
    "validate_expiry": true,
    "clock_skew_seconds": 30
  }
}
```

**JWT Token Operations**:
```bash
# Login to get JWT token
curl -X POST "http://192.168.1.100:8080/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin",
       "password": "secure_password",
       "remember_me": false
     }'

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "username": "admin",
    "role": "administrator",
    "permissions": ["*"]
  }
}

# Refresh token
curl -X POST "http://192.168.1.100:8080/api/auth/refresh" \
     -H "Content-Type: application/json" \
     -d '{
       "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
     }'

# Logout
curl -X POST "http://192.168.1.100:8080/api/auth/logout" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Certificate-Based Authentication

**Client Certificate Setup**:
```bash
# Generate CA certificate
openssl genrsa -out ca-key.pem 4096
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem \
    -subj "/C=US/ST=CA/L=SF/O=RotorDream/OU=Security/CN=RotorDream-CA"

# Generate client certificate
openssl genrsa -out client-key.pem 4096
openssl req -subj '/CN=client' -new -key client-key.pem -out client.csr
openssl x509 -req -days 365 -in client.csr -CA ca.pem -CAkey ca-key.pem \
    -out client-cert.pem -sha256 -CAcreateserial

# Configure server for client certificates
```

**Certificate Configuration**:
```ini
# /etc/rotordream/tls.conf
[client_certificates]
enabled = true
ca_cert_file = /etc/rotordream/ssl/ca.pem
verify_client = require
verify_depth = 2

# Certificate validation
check_revocation = true
crl_file = /etc/rotordream/ssl/crl.pem
ocsp_enable = false

# Certificate mapping
[cert_mapping]
# Map certificate CN to username/role
admin = role:administrator
monitoring = role:operator,permissions:camera:read,system:read
readonly = role:viewer,permissions:camera:read
```

## Authorization and Access Control

### Role-Based Access Control (RBAC)

**Role Definitions**:
```json
{
  "roles": {
    "administrator": {
      "description": "Full system access",
      "permissions": ["*"],
      "inherits": []
    },
    "operator": {
      "description": "Camera operation and monitoring",
      "permissions": [
        "camera:read", "camera:write", "camera:control",
        "recordings:read", "recordings:write",
        "system:read", "logs:read"
      ],
      "inherits": []
    },
    "viewer": {
      "description": "Read-only access to camera feeds",
      "permissions": [
        "camera:read", "recordings:read", "system:read"
      ],
      "inherits": []
    },
    "maintenance": {
      "description": "System maintenance access",
      "permissions": [
        "system:read", "system:write", "logs:read", "logs:write",
        "storage:read", "backup:read", "backup:write"
      ],
      "inherits": ["viewer"]
    }
  }
}
```

**User Management**:
```bash
# Create user with role
curl -X POST "http://192.168.1.100:8080/api/auth/users" \
     -H "Authorization: Bearer admin_token" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "operator1",
       "password": "secure_password",
       "email": "operator1@company.com",
       "role": "operator",
       "enabled": true,
       "password_expires": true,
       "must_change_password": true
     }'

# Update user permissions
curl -X PUT "http://192.168.1.100:8080/api/auth/users/operator1" \
     -H "Authorization: Bearer admin_token" \
     -H "Content-Type: application/json" \
     -d '{
       "role": "operator",
       "additional_permissions": ["backup:read"],
       "ip_restrictions": ["192.168.1.0/24"],
       "time_restrictions": {
         "allowed_hours": "08:00-18:00",
         "allowed_days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
       }
     }'

# List users
curl -H "Authorization: Bearer admin_token" \
     http://192.168.1.100:8080/api/auth/users
```

### Permission System

**Permission Categories**:
```json
{
  "permission_categories": {
    "camera": {
      "read": "View camera feeds and status",
      "write": "Modify camera settings",
      "control": "Control camera movements and actions"
    },
    "recordings": {
      "read": "View and download recordings",
      "write": "Create and manage recordings",
      "delete": "Delete recordings"
    },
    "system": {
      "read": "View system status and information",
      "write": "Modify system configuration",
      "admin": "System administration functions"
    },
    "users": {
      "read": "View user information",
      "write": "Create and modify users",
      "admin": "Full user management"
    },
    "logs": {
      "read": "View system logs",
      "write": "Modify log settings",
      "admin": "Log administration"
    },
    "storage": {
      "read": "View storage information",
      "write": "Modify storage settings",
      "admin": "Storage administration"
    },
    "backup": {
      "read": "View backup status",
      "write": "Create and manage backups",
      "admin": "Backup administration"
    }
  }
}
```

**Resource-Level Permissions**:
```bash
# Set camera-specific permissions
curl -X PUT "http://192.168.1.100:8080/api/auth/permissions" \
     -H "Authorization: Bearer admin_token" \
     -H "Content-Type: application/json" \
     -d '{
       "user": "operator1",
       "resource_type": "camera",
       "resource_id": "camera_001",
       "permissions": ["read", "control"]
     }'

# Check user permissions
curl -H "Authorization: Bearer admin_token" \
     "http://192.168.1.100:8080/api/auth/permissions/operator1"
```

## Network Security

### HTTPS/TLS Configuration

**TLS Server Configuration**:
```ini
# /etc/rotordream/tls.conf
[tls]
enabled = true
cert_file = /etc/rotordream/ssl/server.crt
key_file = /etc/rotordream/ssl/server.key
ca_file = /etc/rotordream/ssl/ca.crt

# TLS settings
min_tls_version = 1.2
max_tls_version = 1.3
cipher_suites = ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256
prefer_server_ciphers = true

# HSTS (HTTP Strict Transport Security)
hsts_enabled = true
hsts_max_age = 31536000
hsts_include_subdomains = true
hsts_preload = true
```

**Certificate Management**:
```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/rotordream/ssl/server.key \
    -out /etc/rotordream/ssl/server.crt \
    -subj "/C=US/ST=CA/L=SF/O=RotorDream/CN=192.168.1.100"

# Generate CSR for CA-signed certificate
openssl req -new -newkey rsa:2048 -nodes \
    -keyout /etc/rotordream/ssl/server.key \
    -out /etc/rotordream/ssl/server.csr \
    -subj "/C=US/ST=CA/L=SF/O=RotorDream/CN=camera.example.com"

# Check certificate expiration
openssl x509 -in /etc/rotordream/ssl/server.crt -noout -dates

# Verify certificate
openssl verify -CAfile /etc/rotordream/ssl/ca.crt /etc/rotordream/ssl/server.crt
```

### Firewall Configuration

**IPTables Rules**:
```bash
#!/bin/bash
# /etc/rotordream/firewall.sh

# Clear existing rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH (admin access)
iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT

# Allow HTTPS API
iptables -A INPUT -p tcp --dport 443 -s 192.168.1.0/24 -j ACCEPT

# Allow HTTP API (if enabled)
iptables -A INPUT -p tcp --dport 8080 -s 192.168.1.0/24 -j ACCEPT

# Allow RTSP streaming
iptables -A INPUT -p tcp --dport 554 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p udp --dport 5004:5100 -s 192.168.1.0/24 -j ACCEPT

# Allow WebSocket connections
iptables -A INPUT -p tcp --dport 8081 -s 192.168.1.0/24 -j ACCEPT

# Allow ONVIF discovery
iptables -A INPUT -p udp --dport 3702 -j ACCEPT

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "iptables-dropped: "

# Save rules
iptables-save > /etc/iptables/rules.v4
```

**Network Access Control**:
```json
{
  "network_access": {
    "allow_networks": [
      "192.168.1.0/24",
      "10.0.0.0/8"
    ],
    "deny_networks": [
      "0.0.0.0/0"
    ],
    "rate_limiting": {
      "enabled": true,
      "requests_per_minute": 100,
      "burst_size": 20,
      "ban_duration": 300
    },
    "geo_blocking": {
      "enabled": false,
      "allowed_countries": ["US", "CA"],
      "blocked_countries": []
    }
  }
}
```

## Data Encryption

### Encryption Configuration

**Storage Encryption**:
```bash
# Setup LUKS encryption for storage
cryptsetup luksFormat /dev/sdb
cryptsetup luksOpen /dev/sdb encrypted_storage

# Create filesystem on encrypted device
mkfs.ext4 /dev/mapper/encrypted_storage

# Mount encrypted storage
mount /dev/mapper/encrypted_storage /media/encrypted_data

# Auto-mount configuration in /etc/crypttab
encrypted_storage /dev/sdb /etc/rotordream/luks_keyfile luks

# Auto-mount in /etc/fstab
/dev/mapper/encrypted_storage /media/encrypted_data ext4 defaults 0 0
```

**Backup Encryption**:
```bash
# Configure encrypted backups
curl -X PUT "http://192.168.1.100:8080/api/backup/encryption" \
     -H "Authorization: Bearer admin_token" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "method": "AES256",
       "key_derivation": "PBKDF2",
       "iterations": 100000,
       "password_file": "/etc/rotordream/backup_password"
     }'

# GPG encryption for backups
gpg --gen-key
gpg --armor --export backup@rotordream.com > backup_public.key
gpg --armor --export-secret-keys backup@rotordream.com > backup_private.key
```

### Stream Encryption

**RTSP over TLS (RTSPS)**:
```ini
# /etc/rotordream/streaming.conf
[rtsp_security]
tls_enabled = true
tls_port = 322
require_authentication = true
encryption_method = AES128

# Stream encryption
[stream_encryption]
enabled = true
key_rotation_interval = 3600
encryption_algorithm = AES-256-CTR
```

**Encrypted Video Streams**:
```bash
# Configure encrypted streaming
curl -X PUT "http://192.168.1.100:8080/api/streaming/encryption" \
     -H "Authorization: Bearer admin_token" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "algorithm": "AES-256-GCM",
       "key_exchange": "ECDHE",
       "key_rotation_seconds": 3600
     }'
```

## Audit and Logging

### Security Event Logging

**Audit Configuration**:
```json
{
  "audit": {
    "enabled": true,
    "log_file": "/var/log/rotordream/audit.log",
    "log_level": "info",
    "max_file_size": "100MB",
    "max_files": 10,
    "events": {
      "authentication": true,
      "authorization": true,
      "api_access": true,
      "configuration_changes": true,
      "user_management": true,
      "system_access": true,
      "camera_access": true,
      "file_access": true
    }
  }
}
```

**Security Events**:
```bash
# View security events
curl -H "Authorization: Bearer admin_token" \
     "http://192.168.1.100:8080/api/audit/events?type=security&limit=100"

# Response format
{
  "events": [
    {
      "timestamp": "2025-01-15T10:30:00Z",
      "event_type": "authentication_failure",
      "source_ip": "192.168.1.50",
      "username": "admin",
      "user_agent": "curl/7.68.0",
      "details": {
        "reason": "invalid_password",
        "attempts": 3
      }
    },
    {
      "timestamp": "2025-01-15T10:25:00Z",
      "event_type": "api_access",
      "source_ip": "192.168.1.25",
      "username": "operator1",
      "endpoint": "/api/camera/status",
      "method": "GET",
      "status_code": 200
    }
  ]
}
```

### SIEM Integration

**Syslog Configuration**:
```ini
# /etc/rotordream/syslog.conf
[syslog]
enabled = true
server = 192.168.1.100
port = 514
protocol = udp
facility = local0
format = rfc3164

# Security events
send_security_events = true
send_audit_logs = true
send_system_events = true
```

**Log Forwarding**:
```bash
# Configure rsyslog for security events
echo "local0.* @@192.168.1.100:514" >> /etc/rsyslog.conf
systemctl restart rsyslog

# Test log forwarding
logger -p local0.info "Test security event from RotorDream"
```

## Security Hardening

### System Hardening

**Service Configuration**:
```bash
# Disable unnecessary services
systemctl disable bluetooth
systemctl disable cups
systemctl disable avahi-daemon

# SSH hardening
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
echo "AllowUsers admin operator" >> /etc/ssh/sshd_config

# Kernel hardening
echo "kernel.dmesg_restrict = 1" >> /etc/sysctl.conf
echo "net.ipv4.conf.all.send_redirects = 0" >> /etc/sysctl.conf
echo "net.ipv4.conf.all.accept_redirects = 0" >> /etc/sysctl.conf
sysctl -p
```

**File System Security**:
```bash
# Set secure permissions
chmod 700 /etc/rotordream/
chmod 600 /etc/rotordream/*.conf
chmod 600 /etc/rotordream/ssl/*

# Remove SUID bits from unnecessary files
find /usr/bin -perm -4000 -exec ls -la {} \;
```

### Application Security

**Security Headers**:
```json
{
  "security_headers": {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  }
}
```

**Input Validation**:
```bash
# API input validation rules
curl -X PUT "http://192.168.1.100:8080/api/security/validation" \
     -H "Authorization: Bearer admin_token" \
     -H "Content-Type: application/json" \
     -d '{
       "input_validation": {
         "max_request_size": 10485760,
         "max_url_length": 2048,
         "max_header_count": 50,
         "sanitize_inputs": true,
         "block_sql_injection": true,
         "block_xss": true
       }
     }'
```

## Security Monitoring

### Intrusion Detection

**Fail2Ban Configuration**:
```ini
# /etc/fail2ban/jail.local
[rotordream-auth]
enabled = true
port = 8080,443
filter = rotordream-auth
logpath = /var/log/rotordream/audit.log
maxretry = 5
bantime = 3600

[rotordream-api]
enabled = true
port = 8080,443
filter = rotordream-api
logpath = /var/log/rotordream/access.log
maxretry = 10
bantime = 1800
```

**Security Monitoring API**:
```bash
# Get security status
curl -H "Authorization: Bearer admin_token" \
     http://192.168.1.100:8080/api/security/status

# Response includes
{
  "security_status": {
    "last_scan": "2025-01-15T10:30:00Z",
    "vulnerabilities": 0,
    "failed_logins": 3,
    "blocked_ips": ["192.168.1.75"],
    "certificate_expiry": "2026-01-15T10:30:00Z",
    "security_score": 95
  }
}
```

## Troubleshooting Security Issues

### Common Problems

**Certificate Issues**:
```bash
# Check certificate validity
openssl x509 -in /etc/rotordream/ssl/server.crt -text -noout

# Test TLS connection
openssl s_client -connect 192.168.1.100:443 -verify_hostname camera.example.com

# Debug TLS handshake
curl -vvv https://192.168.1.100:443/api/status
```

**Authentication Problems**:
```bash
# Test API key
curl -H "X-API-Key: 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/api/status

# Validate JWT token
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     http://192.168.1.100:8080/api/user/profile

# Check user permissions
curl -H "Authorization: Bearer admin_token" \
     http://192.168.1.100:8080/api/auth/debug/user/operator1
```

## Related Documentation

- [Network Configuration](./network.md) - Network setup and security
- [Monitoring](../operations/monitoring.md) - Security monitoring and alerting
- [API Reference](../api/http-api.md) - Authentication API endpoints
- [Troubleshooting](../operations/troubleshooting.md) - Security troubleshooting

---

*Security configuration documentation following industry best practices and OWASP guidelines*
