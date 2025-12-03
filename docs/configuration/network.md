# Network Configuration

**Comprehensive network setup and management for camera devices.**

## Overview

The RotorDream camera system provides flexible networking capabilities supporting wired Ethernet, wireless connectivity, and advanced network services for integration into various environments.

```mermaid
graph TB
    A[Camera Device] --> B[Network Interface]
    B --> C{Connection Type}
    C -->|Ethernet| D[Wired Network]
    C -->|WiFi| E[Wireless Network]
    C -->|USB Tethering| F[Mobile Network]
    
    D --> G[DHCP/Static IP]
    E --> H[WiFi Access Point]
    F --> I[USB Host Device]
    
    G --> J[Network Services]
    H --> J
    I --> J
    
    J --> K[HTTP/HTTPS Server]
    J --> L[RTSP Streaming]
    J --> M[WebSocket API]
    J --> N[ONVIF Service]
    J --> O[mDNS/Bonjour]
```

## Network Interfaces

### Ethernet Configuration

**Static IP Configuration**:
```bash
# /etc/systemd/network/eth0.network
[Match]
Name=eth0

[Network]
Address=192.168.1.100/24
Gateway=192.168.1.1
DNS=8.8.8.8
DNS=8.8.4.4
DHCP=no

[Route]
Gateway=192.168.1.1
Destination=0.0.0.0/0
```

**DHCP Configuration**:
```bash
# /etc/systemd/network/eth0.network
[Match]
Name=eth0

[Network]
DHCP=yes
IPForward=yes

[DHCP]
UseDNS=yes
UseRoutes=yes
SendHostname=yes
Hostname=rotorclear-cam
```

**Manual Configuration via API**:
```bash
# Set static IP
curl -X PUT "http://192.168.1.100:8080/api/config/network" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "ethernet": {
         "enabled": true,
         "mode": "static",
         "ip_address": "192.168.1.100",
         "subnet_mask": "255.255.255.0",
         "gateway": "192.168.1.1",
         "dns_servers": ["8.8.8.8", "8.8.4.4"]
       }
     }'

# Enable DHCP
curl -X PUT "http://192.168.1.100:8080/api/config/network" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "ethernet": {
         "enabled": true,
         "mode": "dhcp",
         "hostname": "rotorclear-cam"
       }
     }'
```

### WiFi Configuration

**WiFi Client Mode**:
```bash
# Connect to existing WiFi network
curl -X POST "http://192.168.1.100:8080/api/wifi/connect" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "ssid": "Office-WiFi",
       "password": "wifi_password",
       "security": "WPA2-PSK",
       "save_profile": true
     }'

# List available networks
curl -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     "http://192.168.1.100:8080/api/wifi/scan"
```

**WiFi Access Point Mode**:
```bash
# Create WiFi hotspot
curl -X POST "http://192.168.1.100:8080/api/wifi/hotspot" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "ssid": "RotorClear-CAM-001",
       "password": "rotorclear123",
       "security": "WPA2-PSK",
       "channel": 6,
       "ip_range": "192.168.4.0/24"
     }'
```

**wpa_supplicant Configuration**:
```bash
# /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="Office-WiFi"
    psk="wifi_password"
    key_mgmt=WPA-PSK
    priority=10
}

network={
    ssid="Guest-Network"
    key_mgmt=NONE
    priority=5
}

# Enterprise WiFi (WPA2-Enterprise)
network={
    ssid="Corporate-WiFi"
    key_mgmt=WPA-EAP
    eap=PEAP
    identity="username"
    password="password"
    phase2="auth=MSCHAPV2"
}
```

### Network Interface Management

**Enable/Disable Interfaces**:
```bash
# Enable Ethernet
sudo ip link set eth0 up

# Disable WiFi
sudo ip link set wlan0 down

# Restart networking
sudo systemctl restart systemd-networkd
sudo systemctl restart wpa_supplicant
```

**Monitor Interface Status**:
```bash
# Check interface status
ip addr show

# Monitor network statistics
watch -n 1 cat /proc/net/dev

# Check wireless signal strength
iwconfig wlan0
```

## Service Configuration

### HTTP/HTTPS Server

**Basic HTTP Configuration**:
```ini
# /etc/rotordream/server.conf
[http]
enabled = true
port = 8080
bind_address = 0.0.0.0
max_connections = 100
timeout = 30
cors_enabled = true
cors_origins = *

[https]
enabled = true
port = 8081
ssl_cert = /etc/ssl/certs/rotordream.crt
ssl_key = /etc/ssl/private/rotordream.key
ssl_protocols = TLSv1.2,TLSv1.3
ssl_ciphers = ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS
```

**SSL Certificate Generation**:
```bash
# Self-signed certificate for testing
openssl req -x509 -newkey rsa:4096 -keyout /etc/ssl/private/rotordream.key \
            -out /etc/ssl/certs/rotordream.crt -days 365 -nodes \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=rotorclear-cam"

# Let's Encrypt certificate (if domain is available)
certbot certonly --standalone --preferred-challenges http \
        -d rotorclear-cam.example.com
```

### RTSP Streaming Server

**RTSP Configuration**:
```ini
# /etc/rotordream/rtsp.conf
[rtsp]
enabled = true
port = 554
bind_address = 0.0.0.0
max_connections = 10
timeout = 60
authentication_required = true

[streams]
stream0_path = /stream0
stream0_resolution = 1920x1080
stream0_framerate = 30
stream0_bitrate = 4000000

stream1_path = /stream1
stream1_resolution = 640x480
stream1_framerate = 15
stream1_bitrate = 1000000
```

**RTSP URL Examples**:
```
# Primary high-resolution stream
rtsp://192.168.1.100:554/stream0

# Secondary low-resolution stream
rtsp://192.168.1.100:554/stream1

# With authentication
rtsp://admin:password@192.168.1.100:554/stream0
```

### mDNS/Bonjour Service Discovery

**Avahi Configuration**:
```xml
<!-- /etc/avahi/services/rotordream.service -->
<?xml version="1.0" standalone='no'?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">RotorClear Camera %h</name>
  <service>
    <type>_http._tcp</type>
    <port>8080</port>
    <txt-record>path=/</txt-record>
    <txt-record>version=1.0</txt-record>
    <txt-record>model=RotorClear</txt-record>
  </service>
  <service>
    <type>_rtsp._tcp</type>
    <port>554</port>
    <txt-record>path=/stream0</txt-record>
  </service>
  <service>
    <type>_onvif._tcp</type>
    <port>8080</port>
    <txt-record>path=/onvif/device_service</txt-record>
  </service>
</service-group>
```

**Service Discovery Client**:
```bash
# Discover RotorDream cameras on network
avahi-browse _http._tcp --resolve

# Discover RTSP services
avahi-browse _rtsp._tcp --resolve

# Query specific service
avahi-resolve -n rotorclear-cam.local
```

## Firewall Configuration

### iptables Rules

**Basic Firewall Setup**:
```bash
#!/bin/bash
# /etc/rotordream/firewall.sh

# Flush existing rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH (be careful!)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
iptables -A INPUT -p tcp --dport 8081 -j ACCEPT

# Allow RTSP
iptables -A INPUT -p tcp --dport 554 -j ACCEPT

# Allow RTP ports for RTSP streaming
iptables -A INPUT -p udp --dport 5004:5010 -j ACCEPT

# Allow mDNS
iptables -A INPUT -p udp --dport 5353 -j ACCEPT

# Allow ONVIF WS-Discovery
iptables -A INPUT -p udp --dport 3702 -j ACCEPT

# Allow ICMP (ping)
iptables -A INPUT -p icmp -j ACCEPT

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "iptables-dropped: "

# Save rules
iptables-save > /etc/iptables/rules.v4
```

**Advanced Rules with Rate Limiting**:
```bash
# Rate limit HTTP requests
iptables -A INPUT -p tcp --dport 8080 -m state --state NEW \
         -m recent --set --name http_limit
iptables -A INPUT -p tcp --dport 8080 -m state --state NEW \
         -m recent --update --seconds 60 --hitcount 20 --name http_limit \
         -j LOG --log-prefix "HTTP-RATE-LIMIT: "
iptables -A INPUT -p tcp --dport 8080 -m state --state NEW \
         -m recent --update --seconds 60 --hitcount 20 --name http_limit \
         -j DROP

# Block specific IPs
iptables -A INPUT -s 192.168.1.50 -j DROP

# Allow only specific subnet for admin access
iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP
```

### UFW (Uncomplicated Firewall)

**Basic UFW Configuration**:
```bash
# Enable UFW
sudo ufw enable

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (be careful!)
sudo ufw allow 22/tcp

# Allow HTTP services
sudo ufw allow 8080/tcp comment 'HTTP API'
sudo ufw allow 8081/tcp comment 'HTTPS API'

# Allow RTSP
sudo ufw allow 554/tcp comment 'RTSP streaming'
sudo ufw allow 5004:5010/udp comment 'RTP data'

# Allow mDNS
sudo ufw allow 5353/udp comment 'mDNS service discovery'

# Allow from specific subnet only
sudo ufw allow from 192.168.1.0/24 to any port 22

# Check status
sudo ufw status verbose
```

## Quality of Service (QoS)

### Traffic Shaping

**tc (Traffic Control) Configuration**:
```bash
#!/bin/bash
# /etc/rotordream/qos.sh

DEV=eth0
UPLOAD_RATE=100mbit
DOWNLOAD_RATE=100mbit

# Clear existing rules
tc qdisc del dev $DEV root 2>/dev/null

# Create root qdisc
tc qdisc add dev $DEV root handle 1: htb default 30

# Create classes
tc class add dev $DEV parent 1: classid 1:1 htb rate $UPLOAD_RATE

# High priority: RTSP/RTP traffic
tc class add dev $DEV parent 1:1 classid 1:10 htb rate 50mbit ceil 80mbit prio 1
tc class add dev $DEV parent 1:1 classid 1:20 htb rate 30mbit ceil 50mbit prio 2
tc class add dev $DEV parent 1:1 classid 1:30 htb rate 20mbit ceil 30mbit prio 3

# Filters for RTSP traffic
tc filter add dev $DEV protocol ip parent 1:0 prio 1 u32 \
    match ip dport 554 0xffff flowid 1:10
tc filter add dev $DEV protocol ip parent 1:0 prio 1 u32 \
    match ip dport 5004 0xfffc flowid 1:10

# Filters for HTTP API
tc filter add dev $DEV protocol ip parent 1:0 prio 2 u32 \
    match ip dport 8080 0xffff flowid 1:20
tc filter add dev $DEV protocol ip parent 1:0 prio 2 u32 \
    match ip dport 8081 0xffff flowid 1:20

# DSCP marking for video traffic
iptables -t mangle -A OUTPUT -p tcp --dport 554 -j DSCP --set-dscp 46
iptables -t mangle -A OUTPUT -p udp --dport 5004:5010 -j DSCP --set-dscp 46
```

### Bandwidth Monitoring

**Monitor Network Usage**:
```bash
# Real-time bandwidth monitoring
iftop -i eth0

# Network statistics
nload eth0

# Detailed interface statistics
cat /proc/net/dev

# Monitor specific ports
netstat -tuln | grep -E ':(554|8080|8081)'

# Monitor connections
ss -tuln | grep -E ':(554|8080|8081)'
```

## VPN Configuration

### OpenVPN Server

**Server Configuration**:
```bash
# /etc/openvpn/server/camera-access.conf
port 1194
proto udp
dev tun

ca /etc/openvpn/server/ca.crt
cert /etc/openvpn/server/camera-server.crt
key /etc/openvpn/server/camera-server.key
dh /etc/openvpn/server/dh.pem

server 10.8.0.0 255.255.255.0
ifconfig-pool-persist /var/log/openvpn/ipp.txt

# Routes to camera networks
push "route 192.168.1.0 255.255.255.0"
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"

keepalive 10 120
tls-auth /etc/openvpn/server/ta.key 0
cipher AES-256-CBC
auth SHA256

user nobody
group nogroup
persist-key
persist-tun

status /var/log/openvpn/openvpn-status.log
log-append /var/log/openvpn/openvpn.log
verb 3
```

### WireGuard Configuration

**WireGuard Server**:
```ini
# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <server-private-key>
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

# Client configurations
[Peer]
PublicKey = <client-public-key>
AllowedIPs = 10.0.0.2/32

[Peer]
PublicKey = <client2-public-key>
AllowedIPs = 10.0.0.3/32
```

## Network Diagnostics

### Connection Testing

**Basic Connectivity Tests**:
```bash
# Test network connectivity
ping -c 4 8.8.8.8

# Test DNS resolution
nslookup google.com

# Test HTTP connectivity
curl -I http://192.168.1.100:8080/health

# Test RTSP connectivity
curl -v rtsp://192.168.1.100:554/stream0

# Test port accessibility
nc -zv 192.168.1.100 8080
nc -zv 192.168.1.100 554
```

**Network Performance Testing**:
```bash
# Bandwidth testing with iperf3
# On camera device (server)
iperf3 -s

# On client
iperf3 -c 192.168.1.100 -t 30 -i 1

# UDP performance test
iperf3 -c 192.168.1.100 -u -b 10M -t 30

# Bidirectional test
iperf3 -c 192.168.1.100 --bidir -t 30
```

### Network Troubleshooting

**Common Issues and Solutions**:

**Connection Refused**:
```bash
# Check if service is running
sudo systemctl status rotordream

# Check if port is open
sudo netstat -tlnp | grep 8080

# Check firewall rules
sudo iptables -L -n | grep 8080
sudo ufw status
```

**Slow Performance**:
```bash
# Check network interface errors
cat /proc/net/dev | grep -E '(eth0|wlan0)'

# Monitor real-time traffic
tcpdump -i eth0 -n host 192.168.1.100

# Check for packet loss
ping -c 100 192.168.1.100 | tail -n 2
```

**WiFi Connection Issues**:
```bash
# Scan for networks
sudo iwlist wlan0 scan | grep ESSID

# Check signal strength
iwconfig wlan0

# Restart WiFi service
sudo systemctl restart wpa_supplicant

# Check WiFi logs
journalctl -u wpa_supplicant -f
```

### Network Monitoring Scripts

**Automated Network Health Check**:
```bash
#!/bin/bash
# /usr/local/bin/network-health-check.sh

LOG_FILE="/var/log/rotordream/network-health.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Function to log messages
log_message() {
    echo "[$DATE] $1" >> $LOG_FILE
}

# Check network interfaces
check_interfaces() {
    for iface in eth0 wlan0; do
        if ip link show $iface up > /dev/null 2>&1; then
            log_message "Interface $iface is UP"
        else
            log_message "ERROR: Interface $iface is DOWN"
        fi
    done
}

# Check connectivity
check_connectivity() {
    if ping -c 1 8.8.8.8 > /dev/null 2>&1; then
        log_message "Internet connectivity OK"
    else
        log_message "ERROR: No internet connectivity"
    fi
}

# Check services
check_services() {
    for port in 8080 554; do
        if nc -z localhost $port > /dev/null 2>&1; then
            log_message "Service on port $port is running"
        else
            log_message "ERROR: Service on port $port is not running"
        fi
    done
}

# Run checks
log_message "Starting network health check"
check_interfaces
check_connectivity
check_services
log_message "Network health check completed"
```

**Add to crontab for regular monitoring**:
```bash
# Run every 5 minutes
*/5 * * * * /usr/local/bin/network-health-check.sh
```

## Related Documentation

- [Security Configuration](../security/authentication.md) - Network security and access control
- [ONVIF Integration](../integration/onvif.md) - ONVIF network service configuration
- [Performance Tuning](../operations/performance.md) - Network performance optimization
- [Monitoring](../operations/monitoring.md) - Network monitoring and alerting

---

*Network configuration documentation based on systemd-networkd, iptables, and standard Linux networking tools*
