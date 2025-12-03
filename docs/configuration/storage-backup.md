# Storage and Backup Configuration

**Comprehensive storage management, backup strategies, and data retention policies.**

## Overview

The C Pro storage system manages video recordings, snapshots, logs, and configuration data with automated backup capabilities and intelligent space management.

```mermaid
graph TB
    A[Storage Manager] --> B{Storage Types}
    
    B -->|Primary| C[Internal Storage]
    B -->|External| D[USB/SD Storage]
    B -->|Network| E[SMB/NFS Shares]
    B -->|Cloud| F[Remote Backup]
    
    C --> G[Data Categories]
    D --> G
    E --> G
    F --> H[Backup Manager]
    
    G --> I[Video Recordings]
    G --> J[Image Snapshots]
    G --> K[System Logs]
    G --> L[Configuration]
    
    I --> M[Retention Policy]
    J --> M
    K --> N[Log Rotation]
    L --> O[Config Backup]
    
    M --> P[Auto Cleanup]
    N --> P
    O --> H
    
    H --> Q[Scheduled Backup]
    H --> R[Incremental Sync]
    H --> S[Compression]
```

## Storage Architecture

### File System Structure

**Default Directory Layout**:
```
/media/data/
├── recordings/          # Video recordings
│   ├── continuous/      # Continuous recording segments
│   ├── triggered/       # Event-triggered recordings
│   └── manual/          # Manually initiated recordings
├── snapshots/           # Image captures
│   ├── manual/          # User-initiated snapshots
│   ├── scheduled/       # Time-lapse snapshots
│   └── event/           # Event-triggered snapshots
├── logs/                # System and application logs
│   ├── system/          # System-level logs
│   ├── camera/          # Camera-specific logs
│   └── network/         # Network activity logs
├── config/              # Configuration backups
│   ├── current/         # Active configuration
│   ├── backup/          # Configuration history
│   └── factory/         # Factory defaults
├── cache/               # Temporary files and cache
│   ├── thumbnails/      # Video/image thumbnails
│   ├── processing/      # Processing temporary files
│   └── uploads/         # Upload staging area
└── exports/             # Data exports and reports
    ├── logs/            # Exported log files
    ├── data/            # Exported datasets
    └── reports/         # System reports
```

### Storage Devices

**Primary Storage Configuration**:
```ini
# /etc/rotordream/storage.conf
[primary]
device = /dev/mmcblk0p2
mount_point = /media/data
filesystem = ext4
auto_mount = true
check_interval = 300

# Space management
warning_threshold = 85      # Warn at 85% full
critical_threshold = 95     # Critical at 95% full
auto_cleanup = true
cleanup_priority = oldest_first

[recordings]
path = /media/data/recordings
max_size_gb = 50
retention_days = 30
segment_duration = 900      # 15 minutes
max_segments = 2000

[snapshots]
path = /media/data/snapshots
max_size_gb = 10
retention_days = 60
max_files = 10000
```

**External Storage**:
```ini
[external]
enabled = true
auto_detect = true
mount_base = /media/external
supported_fs = ext4,ntfs,vfat,exfat

# USB storage
[usb_storage]
enabled = true
auto_backup = true
backup_schedule = "0 2 * * *"  # Daily at 2 AM
sync_mode = incremental

# Network storage
[network_storage]
enabled = false
type = smb
server = 192.168.1.200
share = camera_storage
username = camera_user
password_file = /etc/rotordream/smb_password
mount_options = vers=3.0,uid=1000,gid=1000
```

## Storage Monitoring

### Space Management

**Real-time Monitoring**:
```bash
# Check storage usage via API
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/api/storage/status

# Response format
{
  "storage": {
    "total_space": 34359738368,
    "used_space": 17179869184,
    "available_space": 17179869184,
    "usage_percent": 50.0,
    "warning_level": "normal"
  },
  "categories": {
    "recordings": {
      "size": 15032385536,
      "files": 156,
      "oldest": "2025-01-08T10:30:00Z",
      "newest": "2025-01-15T10:30:00Z"
    },
    "snapshots": {
      "size": 1073741824,
      "files": 423,
      "oldest": "2025-01-01T00:00:00Z",
      "newest": "2025-01-15T10:30:00Z"
    },
    "logs": {
      "size": 134217728,
      "files": 89,
      "oldest": "2025-01-01T00:00:00Z",
      "newest": "2025-01-15T10:30:00Z"
    }
  }
}
```

**Automated Cleanup**:
```bash
# Configure cleanup policies
curl -X PUT "http://192.168.1.100:8080/api/storage/cleanup" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "trigger_threshold": 85,
       "target_threshold": 70,
       "policies": [
         {
           "category": "recordings",
           "method": "oldest_first",
           "preserve_minimum": 10,
           "preserve_recent_hours": 24
         },
         {
           "category": "snapshots", 
           "method": "least_accessed",
           "preserve_minimum": 50
         }
       ]
     }'

# Manual cleanup
curl -X POST "http://192.168.1.100:8080/api/storage/cleanup" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "category": "recordings",
       "older_than_days": 7,
       "dry_run": false
     }'
```

### Health Monitoring

**File System Health**:
```bash
# Check file system integrity
fsck -n /dev/mmcblk0p2

# Monitor I/O statistics
iostat -x 1 5

# Check SMART data (if supported)
smartctl -a /dev/mmcblk0

# Check mount status
mount | grep /media/data
df -h /media/data
```

**Storage Health API**:
```bash
# Get detailed health information
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/api/storage/health

# Response includes
{
  "health": {
    "filesystem": "healthy",
    "write_speed": 15.2,
    "read_speed": 23.5,
    "error_count": 0,
    "temperature": 42,
    "smart_status": "passed"
  },
  "performance": {
    "avg_write_latency_ms": 12.3,
    "avg_read_latency_ms": 8.1,
    "iops_read": 150,
    "iops_write": 100
  }
}
```

## Backup Configuration

### Local Backup

**USB/External Drive Backup**:
```bash
# Configure USB backup
curl -X PUT "http://192.168.1.100:8080/api/backup/config" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "backup_type": "usb",
       "enabled": true,
       "schedule": "0 2 * * *",
       "include_categories": ["recordings", "snapshots", "config"],
       "compression": true,
       "encryption": false,
       "retention_copies": 7
     }'

# Manual backup
curl -X POST "http://192.168.1.100:8080/api/backup/start" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "backup_type": "usb",
       "categories": ["recordings"],
       "date_range": {
         "start": "2025-01-14T00:00:00Z",
         "end": "2025-01-15T23:59:59Z"
       }
     }'
```

**Rsync Configuration**:
```bash
# /etc/rotordream/backup-rsync.conf
[rsync]
enabled = true
schedule = "0 3 * * *"
source = /media/data/
destination = /media/external/backup/
options = -avz --delete --exclude=cache/ --exclude=*.tmp

# Include/exclude patterns
include_patterns = *.avi,*.jpg,*.log,*.conf
exclude_patterns = *.tmp,*.lock,cache/*

# Bandwidth limiting
bandwidth_limit = 10000  # KB/s
```

### Network Backup

**SMB/CIFS Backup**:
```bash
# Mount network share
sudo mount -t cifs //192.168.1.200/camera_backup /mnt/network_backup \
     -o username=backup_user,password_file=/etc/rotordream/smb_password,vers=3.0

# Configure network backup
curl -X PUT "http://192.168.1.100:8080/api/backup/config" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "backup_type": "network",
       "enabled": true,
       "server": "192.168.1.200",
       "share": "camera_backup",
       "credentials": {
         "username": "backup_user",
         "password_file": "/etc/rotordream/smb_password"
       },
       "schedule": "0 1 * * *",
       "compression": true,
       "incremental": true
     }'
```

**FTP/SFTP Backup**:
```bash
# Configure SFTP backup
curl -X PUT "http://192.168.1.100:8080/api/backup/config" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "backup_type": "sftp",
       "enabled": true,
       "server": "backup.example.com",
       "port": 22,
       "username": "camera_backup",
       "key_file": "/etc/rotordream/ssh_backup_key",
       "remote_path": "/backups/camera001/",
       "schedule": "0 4 * * 0",
       "compression": true,
       "encryption": true
     }'
```

### Cloud Backup

**S3-Compatible Storage**:
```bash
# Configure S3 backup
curl -X PUT "http://192.168.1.100:8080/api/backup/config" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "backup_type": "s3",
       "enabled": true,
       "endpoint": "s3.amazonaws.com",
       "bucket": "camera-backups",
       "region": "us-east-1",
       "access_key": "AKIAIOSFODNN7EXAMPLE",
       "secret_key_file": "/etc/rotordream/s3_secret",
       "prefix": "camera001/",
       "schedule": "0 5 * * 0",
       "storage_class": "STANDARD_IA",
       "encryption": "AES256"
     }'
```

### Backup Monitoring

**Backup Status**:
```bash
# Get backup status
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/api/backup/status

# Response includes
{
  "backup_status": {
    "last_backup": "2025-01-15T02:00:00Z",
    "last_backup_status": "success",
    "last_backup_size": 2147483648,
    "last_backup_duration": 1800,
    "next_backup": "2025-01-16T02:00:00Z",
    "backup_type": "usb"
  },
  "backup_history": [
    {
      "timestamp": "2025-01-15T02:00:00Z",
      "status": "success",
      "size": 2147483648,
      "duration": 1800,
      "files_backed_up": 156,
      "backup_type": "usb"
    }
  ]
}

# List backup jobs
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/api/backup/jobs
```

## Data Retention Policies

### Retention Configuration

**Policy Definition**:
```json
{
  "retention_policies": {
    "recordings": {
      "default_retention_days": 30,
      "rules": [
        {
          "name": "critical_events",
          "pattern": "*_critical_*",
          "retention_days": 365,
          "priority": "high"
        },
        {
          "name": "manual_recordings",
          "source": "manual",
          "retention_days": 90,
          "priority": "medium"
        },
        {
          "name": "continuous_recordings",
          "source": "continuous",
          "retention_days": 14,
          "priority": "low"
        }
      ]
    },
    "snapshots": {
      "default_retention_days": 60,
      "rules": [
        {
          "name": "high_quality",
          "quality": ">= 95",
          "retention_days": 180
        },
        {
          "name": "thumbnails",
          "type": "thumbnail",
          "retention_days": 30
        }
      ]
    },
    "logs": {
      "default_retention_days": 90,
      "rules": [
        {
          "name": "error_logs",
          "level": "error",
          "retention_days": 365
        },
        {
          "name": "debug_logs",
          "level": "debug",
          "retention_days": 7
        }
      ]
    }
  }
}
```

**Apply Retention Policies**:
```bash
# Set retention policy
curl -X PUT "http://192.168.1.100:8080/api/storage/retention" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "category": "recordings",
       "default_days": 30,
       "rules": [
         {
           "pattern": "*_important_*",
           "retention_days": 365
         }
       ]
     }'

# Check retention status
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/api/storage/retention/status
```

## Data Export and Import

### Export Operations

**Bulk Data Export**:
```bash
# Export recordings by date range
curl -X POST "http://192.168.1.100:8080/api/storage/export" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "export_type": "recordings",
       "date_range": {
         "start": "2025-01-10T00:00:00Z",
         "end": "2025-01-15T23:59:59Z"
       },
       "format": "zip",
       "include_metadata": true,
       "destination": "/media/external/exports/"
     }'

# Export system configuration
curl -X POST "http://192.168.1.100:8080/api/storage/export" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "export_type": "configuration",
       "include_logs": true,
       "format": "tar.gz",
       "destination": "/media/external/config_backup/"
     }'
```

**Export Status**:
```bash
# Check export progress
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/api/storage/export/status

# Download exported archive
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     http://192.168.1.100:8080/api/storage/export/download/export_20250115.zip \
     --output export_20250115.zip
```

### Import Operations

**Data Import**:
```bash
# Import recordings archive
curl -X POST "http://192.168.1.100:8080/api/storage/import" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -F "file=@recordings_backup.zip" \
     -F "import_type=recordings" \
     -F "overwrite=false"

# Import configuration
curl -X POST "http://192.168.1.100:8080/api/storage/import" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -F "file=@config_backup.tar.gz" \
     -F "import_type=configuration" \
     -F "restore_mode=merge"
```

## Performance Optimization

### I/O Optimization

**File System Tuning**:
```bash
# Optimize ext4 for video workloads
tune2fs -o journal_data_writeback /dev/mmcblk0p2
tune2fs -E stride=16,stripe-width=64 /dev/mmcblk0p2

# Mount options for performance
mount -o remount,noatime,nodiratime,commit=60 /media/data

# Scheduler optimization
echo deadline > /sys/block/mmcblk0/queue/scheduler
echo 4096 > /sys/block/mmcblk0/queue/read_ahead_kb
```

**Memory Management**:
```bash
# Adjust dirty page parameters for sustained writes
echo 5 > /proc/sys/vm/dirty_background_ratio
echo 20 > /proc/sys/vm/dirty_ratio
echo 1500 > /proc/sys/vm/dirty_expire_centisecs
echo 500 > /proc/sys/vm/dirty_writeback_centisecs
```

### Storage Performance Monitoring

**Performance Metrics**:
```bash
# Monitor I/O performance
iostat -x 1

# Check write patterns
iotop -o

# Monitor file system cache
cat /proc/meminfo | grep -E '(Dirty|Writeback|Cached)'

# Storage benchmark
dd if=/dev/zero of=/media/data/test_write bs=1M count=1000 oflag=sync
dd if=/media/data/test_write of=/dev/null bs=1M
```

## Troubleshooting

### Common Storage Issues

**Disk Full**:
```bash
# Emergency cleanup
find /media/data/cache -type f -mtime +1 -delete
find /media/data/recordings -name "*.tmp" -delete

# Check for large files
du -ah /media/data | sort -rh | head -20

# Find files by size
find /media/data -size +100M -type f -exec ls -lh {} \;
```

**Backup Failures**:
```bash
# Check backup logs
tail -f /var/log/rotordream/backup.log

# Test backup destination
rsync -avz --dry-run /media/data/test/ /media/external/test/

# Check network connectivity
ping -c 4 192.168.1.200
nc -zv 192.168.1.200 445  # SMB
nc -zv backup.example.com 22  # SSH/SFTP
```

**Corruption Recovery**:
```bash
# File system check and repair
umount /media/data
fsck -f /dev/mmcblk0p2
mount /media/data

# Recover from backup
rsync -avz /media/external/backup/ /media/data/

# Check file integrity
find /media/data -name "*.avi" -exec ffprobe {} \; 2>&1 | grep -i error
```

## Related Documentation

- [Performance Tuning](../operations/performance.md) - System performance optimization
- [Monitoring](../operations/monitoring.md) - Storage monitoring and alerting
- [Security](../security/authentication.md) - Backup encryption and security
- [API Reference](../api/http-api.md) - Storage management API endpoints

---

*Storage configuration documentation based on ext4, rsync, and standard Linux storage tools*
