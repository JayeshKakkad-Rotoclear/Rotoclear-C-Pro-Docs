# Third-Party Integrations

**Comprehensive integration guide for connecting C Pro with external systems, services, and platforms.**

## Overview

C Pro provides extensive integration capabilities with third-party systems including video management systems, analytics platforms, cloud services, and enterprise applications.

```mermaid
graph TB
    A[C Pro System] --> B{Integration Layer}
    
    B -->|Video Management| C[VMS Integration]
    B -->|Cloud Platforms| D[Cloud Services]
    B -->|Analytics| E[AI/ML Platforms]
    B -->|Enterprise| F[Enterprise Systems]
    B -->|Storage| G[Storage Solutions]
    B -->|Monitoring| H[Monitoring Tools]
    
    C --> C1[Milestone XProtect]
    C --> C2[Genetec Security Center]
    C --> C3[Avigilon Control Center]
    C --> C4[Hikvision iVMS]
    
    D --> D1[AWS S3/Kinesis]
    D --> D2[Azure Media Services]
    D --> D3[Google Cloud Video]
    D --> D4[IBM Watson Video]
    
    E --> E1[NVIDIA DeepStream]
    E --> E2[Intel OpenVINO]
    E --> E3[TensorFlow Serving]
    E --> E4[Azure Cognitive Services]
    
    F --> F1[Active Directory]
    F --> F2[LDAP/SAML]
    F --> F3[REST APIs]
    F --> F4[MQTT/Message Queues]
```

## Video Management Systems (VMS)

### Milestone XProtect Integration

**ONVIF Integration**:
```bash
# Configure for Milestone XProtect via ONVIF
curl -X PUT "http://192.168.1.100:8080/api/integrations/milestone" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "integration_type": "onvif",
       "device_name": "C Pro Camera 001",
       "manufacturer": "Rotoclear",
       "model": "RD-CAM-001",
       "onvif_endpoints": {
         "device_service": "http://192.168.1.100:8080/onvif/device_service",
         "media_service": "http://192.168.1.100:8080/onvif/media_service",
         "ptz_service": "http://192.168.1.100:8080/onvif/ptz_service",
         "event_service": "http://192.168.1.100:8080/onvif/event_service"
       },
       "streaming": {
         "rtsp_url": "rtsp://192.168.1.100:554/onvif/profile_1",
         "backup_url": "rtsp://192.168.1.100:554/onvif/profile_2"
       },
       "authentication": {
         "username": "milestone",
         "password": "milestone123"
       }
     }'
```

**Direct API Integration**:
```bash
# Configure direct API integration for advanced features
curl -X PUT "http://192.168.1.100:8080/api/integrations/milestone/api" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "milestone_server": "192.168.1.10",
       "api_version": "2021.1",
       "authentication": {
         "username": "admin",
         "password": "admin123"
       },
       "camera_mapping": {
         "camera_guid": "12345678-1234-1234-1234-123456789012",
         "hardware_id": "RD-CAM-001",
         "recording_server": "192.168.1.11"
       },
       "features": {
         "metadata_overlay": true,
         "analytics_events": true,
         "alarm_integration": true
       }
     }'
```

### Genetec Security Center

**Security Center Integration**:
```bash
# Configure Genetec Security Center integration
curl -X PUT "http://192.168.1.100:8080/api/integrations/genetec" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "server_address": "192.168.1.15",
       "directory_server": "192.168.1.16",
       "authentication": {
         "username": "genetec_user",
         "password": "genetec123",
         "domain": "COMPANY"
       },
       "camera_configuration": {
         "entity_name": "C Pro Camera 001",
         "entity_type": "Camera",
         "archiver": "Main Archiver",
         "partition": "Default Partition"
       },
       "streaming_profiles": [
         {
           "name": "Live",
           "rtsp_url": "rtsp://192.168.1.100:554/live",
           "codec": "H264",
           "resolution": "1920x1080",
           "framerate": 30
         },
         {
           "name": "Playback",
           "rtsp_url": "rtsp://192.168.1.100:554/playback",
           "codec": "H264",
           "resolution": "1280x720",
           "framerate": 15
         }
       ]
     }'
```

### Generic VMS Integration

**RTSP/ONVIF Standard Integration**:
```python
#!/usr/bin/env python3
# vms_integration.py

import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class VMSIntegration:
    def __init__(self, camera_ip, camera_port=8080, api_key=None):
        self.camera_ip = camera_ip
        self.camera_port = camera_port
        self.api_key = api_key
        self.base_url = f"http://{camera_ip}:{camera_port}"
        
    def get_camera_capabilities(self):
        """Get camera capabilities for VMS configuration"""
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        response = requests.get(f"{self.base_url}/api/camera/capabilities", headers=headers)
        return response.json()
    
    def get_streaming_endpoints(self):
        """Get available streaming endpoints"""
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        response = requests.get(f"{self.base_url}/api/streaming/endpoints", headers=headers)
        return response.json()
    
    def configure_for_vms(self, vms_type, vms_config):
        """Configure camera for specific VMS"""
        config_data = {
            "vms_type": vms_type,
            "configuration": vms_config,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        response = requests.post(
            f"{self.base_url}/api/integrations/vms/configure",
            json=config_data,
            headers=headers
        )
        return response.json()
    
    def get_onvif_wsdl_urls(self):
        """Get ONVIF WSDL URLs for VMS auto-discovery"""
        base_onvif = f"{self.base_url}/onvif"
        
        return {
            "device_service": f"{base_onvif}/device_service?wsdl",
            "media_service": f"{base_onvif}/media_service?wsdl",
            "ptz_service": f"{base_onvif}/ptz_service?wsdl",
            "event_service": f"{base_onvif}/event_service?wsdl",
            "analytics_service": f"{base_onvif}/analytics_service?wsdl"
        }

# Example VMS configurations
def configure_milestone_xprotect():
    vms = VMSIntegration("192.168.1.100", api_key="your_api_key")
    
    milestone_config = {
        "manufacturer": "Rotoclear",
        "model": "RD-CAM-001",
        "driver_name": "ONVIF",
        "connection_method": "ONVIF",
        "primary_stream": "rtsp://192.168.1.100:554/onvif/profile_1",
        "secondary_stream": "rtsp://192.168.1.100:554/onvif/profile_2",
        "username": "milestone_user",
        "password": "milestone_pass",
        "recording_enabled": True,
        "motion_detection": True,
        "event_forwarding": True
    }
    
    return vms.configure_for_vms("milestone", milestone_config)

def configure_genetec_security_center():
    vms = VMSIntegration("192.168.1.100", api_key="your_api_key")
    
    genetec_config = {
        "entity_type": "Camera",
        "manufacturer": "Rotoclear",
        "model": "RD-CAM-001",
        "connection_type": "IP",
        "video_format": "H264",
        "audio_support": False,
        "ptz_support": True,
        "alarm_inputs": 0,
        "alarm_outputs": 0,
        "streaming_urls": {
            "live": "rtsp://192.168.1.100:554/live",
            "playback": "rtsp://192.168.1.100:554/playback"
        }
    }
    
    return vms.configure_for_vms("genetec", genetec_config)

if __name__ == "__main__":
    # Configure for Milestone XProtect
    milestone_result = configure_milestone_xprotect()
    print("Milestone Configuration:", milestone_result)
    
    # Configure for Genetec Security Center
    genetec_result = configure_genetec_security_center()
    print("Genetec Configuration:", genetec_result)
```

## Cloud Platform Integrations

### AWS Integration

**AWS S3 Storage Integration**:
```bash
# Configure AWS S3 for video storage
curl -X PUT "http://192.168.1.100:8080/api/integrations/aws/s3" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "region": "us-east-1",
       "bucket_name": "C Pro-camera-storage",
       "access_key_id": "AKIAIOSFODNN7EXAMPLE",
       "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
       "encryption": {
         "enabled": true,
         "method": "AES256"
       },
       "upload_settings": {
         "auto_upload": true,
         "upload_schedule": "0 */6 * * *",
         "compression": true,
         "retention_days": 90
       },
       "lifecycle_policy": {
         "transition_to_ia": 30,
         "transition_to_glacier": 90,
         "expiration_days": 365
       }
     }'
```

**AWS Kinesis Video Streams**:
```bash
# Configure AWS Kinesis Video Streams
curl -X PUT "http://192.168.1.100:8080/api/integrations/aws/kinesis" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "region": "us-east-1",
       "stream_name": "rotordream-camera-001",
       "access_key_id": "AKIAIOSFODNN7EXAMPLE",
       "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
       "stream_settings": {
         "data_retention_hours": 24,
         "shard_count": 1,
         "fragment_duration_ms": 2000
       },
       "producer_config": {
         "buffer_duration_ms": 3000,
         "key_frame_fragmentation": true,
         "absolute_fragment_times": true,
         "fragment_acks": true
       }
     }'
```

**AWS Rekognition Integration**:
```bash
# Configure AWS Rekognition for video analysis
curl -X PUT "http://192.168.1.100:8080/api/integrations/aws/rekognition" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "region": "us-east-1",
       "access_key_id": "AKIAIOSFODNN7EXAMPLE",
       "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
       "analysis_settings": {
         "face_detection": true,
         "object_detection": true,
         "text_detection": false,
         "celebrity_recognition": false,
         "unsafe_content_detection": true
       },
       "processing": {
         "real_time": false,
         "batch_interval": 300,
         "confidence_threshold": 80,
         "max_results": 50
       },
       "notification": {
         "sns_topic": "arn:aws:sns:us-east-1:123456789012:rekognition-results",
         "include_metadata": true
       }
     }'
```

### Azure Integration

**Azure Media Services**:
```bash
# Configure Azure Media Services
curl -X PUT "http://192.168.1.100:8080/api/integrations/azure/media" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "subscription_id": "12345678-1234-1234-1234-123456789012",
       "resource_group": "rotordream-resources",
       "account_name": "rotordreammedia",
       "authentication": {
         "client_id": "87654321-4321-4321-4321-210987654321",
         "client_secret": "your_client_secret",
         "tenant_id": "11111111-1111-1111-1111-111111111111"
       },
       "streaming": {
         "live_event_name": "rotordream-live",
         "streaming_protocol": "RTMP",
         "encoding_preset": "Default720p",
         "archive_enabled": true
       },
       "content_protection": {
         "drm_enabled": false,
         "token_auth": false
       }
     }'
```

**Azure Cognitive Services**:
```bash
# Configure Azure Cognitive Services
curl -X PUT "http://192.168.1.100:8080/api/integrations/azure/cognitive" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "endpoint": "https://eastus.api.cognitive.microsoft.com/",
       "subscription_key": "your_subscription_key",
       "services": {
         "computer_vision": {
           "enabled": true,
           "features": ["objects", "faces", "text", "landmarks"],
           "confidence_threshold": 0.7
         },
         "face_api": {
           "enabled": true,
           "face_attributes": ["age", "gender", "emotion"],
           "face_recognition": true
         },
         "video_indexer": {
           "enabled": false,
           "account_id": "your_account_id",
           "location": "eastus"
         }
       }
     }'
```

### Google Cloud Integration

**Google Cloud Video Intelligence**:
```bash
# Configure Google Cloud Video Intelligence
curl -X PUT "http://192.168.1.100:8080/api/integrations/gcp/video" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "project_id": "rotordream-project",
       "service_account_key": "/etc/rotordream/gcp-service-account.json",
       "analysis_features": [
         "LABEL_DETECTION",
         "FACE_DETECTION",
         "PERSON_DETECTION",
         "OBJECT_TRACKING"
       ],
       "processing": {
         "mode": "streaming",
         "segment_duration": 10,
         "confidence_threshold": 0.8
       },
       "storage": {
         "bucket_name": "rotordream-video-analysis",
         "results_format": "json",
         "include_thumbnails": true
       }
     }'
```

## Analytics and AI Platform Integrations

### NVIDIA DeepStream Integration

**DeepStream Pipeline Configuration**:
```bash
# Configure NVIDIA DeepStream integration
curl -X PUT "http://192.168.1.100:8080/api/integrations/nvidia/deepstream" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "deepstream_version": "6.0",
       "gpu_id": 0,
       "pipeline_config": {
         "input_stream": "rtsp://192.168.1.100:554/live",
         "inference_models": [
           {
             "name": "primary_detector",
             "model_file": "/opt/nvidia/deepstream/samples/models/Primary_Detector/resnet10.caffemodel",
             "config_file": "/opt/nvidia/deepstream/samples/configs/deepstream-app/config_infer_primary.txt",
             "classes": ["Vehicle", "Person", "Bicycle", "RoadSign"]
           }
         ],
         "tracker": {
           "enabled": true,
           "config_file": "/opt/nvidia/deepstream/samples/configs/deepstream-app/config_tracker_NvDCF_perf.yml"
         },
         "output": {
           "display": false,
           "rtsp_out": "rtsp://192.168.1.100:554/deepstream_out",
           "metadata_broker": "kafka://192.168.1.50:9092"
         }
       }
     }'
```

### Intel OpenVINO Integration

**OpenVINO Model Server**:
```bash
# Configure Intel OpenVINO integration
curl -X PUT "http://192.168.1.100:8080/api/integrations/intel/openvino" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "model_server_url": "http://192.168.1.60:9000/v1/models",
       "models": [
         {
           "name": "person-detection",
           "version": "1",
           "input_shape": [1, 3, 416, 416],
           "confidence_threshold": 0.7
         },
         {
           "name": "face-detection",
           "version": "1", 
           "input_shape": [1, 3, 384, 672],
           "confidence_threshold": 0.8
         }
       ],
       "preprocessing": {
         "resize_method": "bilinear",
         "normalization": "standard",
         "color_format": "RGB"
       },
       "postprocessing": {
         "nms_threshold": 0.4,
         "max_detections": 100
       }
     }'
```

### Custom ML Platform Integration

**Generic ML API Integration**:
```python
#!/usr/bin/env python3
# ml_integration.py

import requests
import cv2
import numpy as np
import base64
import json
from datetime import datetime

class MLPlatformIntegration:
    def __init__(self, camera_ip, ml_endpoint, api_key=None):
        self.camera_ip = camera_ip
        self.ml_endpoint = ml_endpoint
        self.api_key = api_key
        
    def capture_frame_for_analysis(self):
        """Capture frame from camera for ML analysis"""
        # Get current frame via API
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        response = requests.get(
            f"http://{self.camera_ip}:8080/api/camera/snapshot",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.content
        return None
    
    def analyze_frame(self, frame_data, analysis_type="object_detection"):
        """Send frame to ML platform for analysis"""
        # Encode frame as base64
        frame_b64 = base64.b64encode(frame_data).decode('utf-8')
        
        analysis_request = {
            "image": frame_b64,
            "analysis_type": analysis_type,
            "timestamp": datetime.utcnow().isoformat(),
            "confidence_threshold": 0.7,
            "max_results": 10
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        response = requests.post(
            f"{self.ml_endpoint}/analyze",
            json=analysis_request,
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def setup_streaming_analysis(self, stream_url, webhook_url):
        """Setup streaming analysis with results webhook"""
        stream_config = {
            "stream_url": stream_url,
            "webhook_url": webhook_url,
            "analysis_settings": {
                "frame_interval": 5,  # Analyze every 5th frame
                "analysis_types": ["object_detection", "face_detection"],
                "batch_size": 10,
                "real_time": True
            },
            "filter_settings": {
                "min_confidence": 0.8,
                "classes_of_interest": ["person", "vehicle", "animal"],
                "roi_enabled": True,
                "roi_coordinates": [0.1, 0.1, 0.9, 0.9]  # x1,y1,x2,y2
            }
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        response = requests.post(
            f"{self.ml_endpoint}/streaming/setup",
            json=stream_config,
            headers=headers
        )
        
        return response.json() if response.status_code == 200 else None

# Example usage
def setup_custom_ai_platform():
    """Setup integration with custom AI platform"""
    ml_integration = MLPlatformIntegration(
        camera_ip="192.168.1.100",
        ml_endpoint="http://ai-platform.company.com/api/v1",
        api_key="your_ml_api_key"
    )
    
    # Setup streaming analysis
    stream_url = "rtsp://192.168.1.100:554/live"
    webhook_url = "http://192.168.1.100:8080/api/ml/results"
    
    result = ml_integration.setup_streaming_analysis(stream_url, webhook_url)
    print("Streaming Analysis Setup:", result)
    
    # Test single frame analysis
    frame = ml_integration.capture_frame_for_analysis()
    if frame:
        analysis = ml_integration.analyze_frame(frame, "object_detection")
        print("Frame Analysis Result:", analysis)

if __name__ == "__main__":
    setup_custom_ai_platform()
```

## Enterprise System Integrations

### Active Directory Integration

**LDAP/AD Authentication**:
```bash
# Configure Active Directory integration
curl -X PUT "http://192.168.1.100:8080/api/integrations/ad" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "server": "dc.company.com",
       "port": 389,
       "use_ssl": false,
       "base_dn": "DC=company,DC=com",
       "bind_dn": "CN=service_account,OU=Service Accounts,DC=company,DC=com",
       "bind_password": "service_password",
       "user_search": {
         "base": "OU=Users,DC=company,DC=com",
         "filter": "(&(objectClass=user)(sAMAccountName={username}))",
         "attributes": ["sAMAccountName", "displayName", "mail", "memberOf"]
       },
       "group_mapping": {
         "Camera_Admins": "administrator",
         "Camera_Operators": "operator", 
         "Camera_Viewers": "viewer"
       },
       "sync_settings": {
         "auto_sync": true,
         "sync_interval": 3600,
         "create_users": true,
         "update_users": true
       }
     }'
```

### SAML SSO Integration

**SAML 2.0 Configuration**:
```bash
# Configure SAML SSO
curl -X PUT "http://192.168.1.100:8080/api/integrations/saml" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "identity_provider": {
         "entity_id": "https://sso.company.com/adfs/services/trust",
         "sso_url": "https://sso.company.com/adfs/ls/",
         "slo_url": "https://sso.company.com/adfs/ls/",
         "certificate": "/etc/rotordream/saml/idp-cert.pem"
       },
       "service_provider": {
         "entity_id": "https://camera.company.com/saml/metadata",
         "acs_url": "https://camera.company.com/saml/acs",
         "sls_url": "https://camera.company.com/saml/sls",
         "certificate": "/etc/rotordream/saml/sp-cert.pem",
         "private_key": "/etc/rotordream/saml/sp-key.pem"
       },
       "attribute_mapping": {
         "username": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name",
         "email": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
         "role": "http://schemas.microsoft.com/ws/2008/06/identity/claims/role"
       },
       "settings": {
         "name_id_format": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
         "authn_requests_signed": true,
         "logout_requests_signed": true,
         "want_assertions_signed": true,
         "want_name_id_encrypted": false
       }
     }'
```

### MQTT Integration

**Message Queue Integration**:
```bash
# Configure MQTT integration
curl -X PUT "http://192.168.1.100:8080/api/integrations/mqtt" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "broker": {
         "host": "mqtt.company.com",
         "port": 1883,
         "use_ssl": false,
         "username": "camera_client",
         "password": "mqtt_password",
         "client_id": "rotordream_camera_001"
       },
       "topics": {
         "status": "cameras/rotordream_001/status",
         "events": "cameras/rotordream_001/events",
         "analytics": "cameras/rotordream_001/analytics",
         "commands": "cameras/rotordream_001/commands"
       },
       "publish_settings": {
         "qos": 1,
         "retain": false,
         "interval": 30
       },
       "subscribe_settings": {
         "command_qos": 2,
         "auto_acknowledge": true
       },
       "message_format": {
         "format": "json",
         "timestamp_format": "iso8601",
         "include_metadata": true
       }
     }'
```

## Monitoring and Alerting Integrations

### Prometheus Integration

**Metrics Exposure**:
```bash
# Configure Prometheus metrics endpoint
curl -X PUT "http://192.168.1.100:8080/api/integrations/prometheus" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "endpoint": "/metrics",
       "port": 9090,
       "metrics": {
         "system_metrics": true,
         "camera_metrics": true,
         "network_metrics": true,
         "application_metrics": true
       },
       "labels": {
         "instance": "rotordream_camera_001",
         "location": "building_a",
         "environment": "production"
       },
       "scrape_interval": 15,
       "authentication": {
         "enabled": false,
         "basic_auth": {
           "username": "prometheus",
           "password": "prometheus123"
         }
       }
     }'

# Example Prometheus configuration
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'rotordream-cameras'
    static_configs:
      - targets: ['192.168.1.100:9090']
    scrape_interval: 15s
    metrics_path: /metrics
```

### Grafana Integration

**Grafana Dashboard Configuration**:
```json
{
  "dashboard": {
    "title": "C Pro Camera Monitoring",
    "tags": ["C Pro", "camera", "monitoring"],
    "timezone": "UTC",
    "panels": [
      {
        "title": "Camera Status",
        "type": "stat",
        "targets": [
          {
            "expr": "camera_status{instance=\"rotordream_camera_001\"}",
            "legendFormat": "Status"
          }
        ]
      },
      {
        "title": "Video Frame Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(camera_frames_total{instance=\"rotordream_camera_001\"}[5m])",
            "legendFormat": "FPS"
          }
        ]
      },
      {
        "title": "System Resources",
        "type": "graph",
        "targets": [
          {
            "expr": "cpu_usage_percent{instance=\"rotordream_camera_001\"}",
            "legendFormat": "CPU"
          },
          {
            "expr": "memory_usage_percent{instance=\"rotordream_camera_001\"}",
            "legendFormat": "Memory"
          }
        ]
      }
    ]
  }
}
```

### ELK Stack Integration

**Elasticsearch Log Shipping**:
```bash
# Configure ELK stack integration
curl -X PUT "http://192.168.1.100:8080/api/integrations/elk" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "enabled": true,
       "elasticsearch": {
         "hosts": ["elasticsearch.company.com:9200"],
         "index_pattern": "rotordream-logs-%{+YYYY.MM.dd}",
         "authentication": {
           "username": "elastic",
           "password": "elastic123"
         }
       },
       "logstash": {
         "host": "logstash.company.com",
         "port": 5044,
         "protocol": "tcp"
       },
       "log_types": {
         "system_logs": true,
         "camera_logs": true,
         "security_logs": true,
         "analytics_logs": true
       },
       "format": {
         "add_timestamp": true,
         "add_hostname": true,
         "add_source": true
       }
     }'
```

## Webhook and API Integrations

### Generic Webhook Integration

**Webhook Configuration**:
```bash
# Configure webhook integrations
curl -X PUT "http://192.168.1.100:8080/api/integrations/webhooks" \
     -H "Authorization: Bearer 1a2B3c4D5e6f7G8h" \
     -H "Content-Type: application/json" \
     -d '{
       "webhooks": [
         {
           "name": "slack_notifications",
           "url": "https://hooks.slack.com/services/YOUR_WORKSPACE_ID/YOUR_CHANNEL_ID/YOUR_WEBHOOK_TOKEN",
           "events": ["motion_detected", "camera_offline", "storage_full"],
           "method": "POST",
           "headers": {
             "Content-Type": "application/json"
           },
           "body_template": {
             "text": "Camera Alert: {{event_type}} - {{description}}",
             "channel": "#security-alerts",
             "username": "C Pro Camera"
           },
           "retry_config": {
             "max_retries": 3,
             "retry_delay": 5,
             "timeout": 30
           }
         },
         {
           "name": "custom_analytics",
           "url": "https://api.company.com/analytics/camera-events",
           "events": ["all"],
           "method": "POST",
           "headers": {
             "Authorization": "Bearer analytics_api_key",
             "Content-Type": "application/json"
           },
           "body_template": {
             "camera_id": "{{camera_id}}",
             "event_type": "{{event_type}}",
             "timestamp": "{{timestamp}}",
             "metadata": "{{metadata}}"
           }
         }
       ]
     }'
```

### REST API Integration Framework

**Generic API Integration**:
```python
#!/usr/bin/env python3
# api_integration_framework.py

import requests
import json
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional

class APIIntegrationFramework:
    def __init__(self, camera_ip: str, camera_api_key: str):
        self.camera_ip = camera_ip
        self.camera_api_key = camera_api_key
        self.base_url = f"http://{camera_ip}:8080/api"
        self.integrations = {}
        
    def register_integration(self, name: str, config: Dict):
        """Register a new API integration"""
        self.integrations[name] = {
            'config': config,
            'active': False,
            'last_sync': None,
            'error_count': 0
        }
        
    async def sync_data_to_external_api(self, integration_name: str, data: Dict):
        """Sync data to external API"""
        if integration_name not in self.integrations:
            raise ValueError(f"Integration {integration_name} not registered")
        
        config = self.integrations[integration_name]['config']
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Add authentication
        if 'api_key' in config:
            headers['Authorization'] = f"Bearer {config['api_key']}"
        elif 'basic_auth' in config:
            auth = aiohttp.BasicAuth(
                config['basic_auth']['username'],
                config['basic_auth']['password']
            )
        
        # Transform data if mapping provided
        if 'field_mapping' in config:
            data = self._map_fields(data, config['field_mapping'])
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config['endpoint'],
                    json=data,
                    headers=headers,
                    timeout=config.get('timeout', 30)
                ) as response:
                    
                    if response.status == 200:
                        self.integrations[integration_name]['last_sync'] = datetime.utcnow()
                        self.integrations[integration_name]['error_count'] = 0
                        return await response.json()
                    else:
                        raise Exception(f"API returned status {response.status}")
                        
        except Exception as e:
            self.integrations[integration_name]['error_count'] += 1
            raise e
    
    def _map_fields(self, data: Dict, mapping: Dict) -> Dict:
        """Map fields according to configuration"""
        mapped_data = {}
        for source_field, target_field in mapping.items():
            if source_field in data:
                mapped_data[target_field] = data[source_field]
        return mapped_data
    
    async def get_camera_data(self, endpoint: str) -> Dict:
        """Get data from camera API"""
        headers = {
            'Authorization': f'Bearer {self.camera_api_key}'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/{endpoint}",
                headers=headers
            ) as response:
                return await response.json()
    
    async def setup_real_time_sync(self, integration_name: str, endpoints: List[str], interval: int = 60):
        """Setup real-time data synchronization"""
        while True:
            try:
                for endpoint in endpoints:
                    data = await self.get_camera_data(endpoint)
                    await self.sync_data_to_external_api(integration_name, data)
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                print(f"Sync error for {integration_name}: {e}")
                await asyncio.sleep(interval)

# Example integrations
async def setup_custom_integrations():
    """Setup custom API integrations"""
    framework = APIIntegrationFramework("192.168.1.100", "your_api_key")
    
    # Register CRM integration
    framework.register_integration("crm_system", {
        'endpoint': 'https://api.crm.company.com/security-events',
        'api_key': 'crm_api_key',
        'timeout': 30,
        'field_mapping': {
            'timestamp': 'event_time',
            'event_type': 'security_event_type',
            'camera_id': 'source_device',
            'metadata': 'additional_data'
        }
    })
    
    # Register facility management system
    framework.register_integration("facility_mgmt", {
        'endpoint': 'https://facility.company.com/api/v1/events',
        'basic_auth': {
            'username': 'facility_user',
            'password': 'facility_pass'
        },
        'field_mapping': {
            'location': 'zone',
            'alert_type': 'incident_type',
            'severity': 'priority_level'
        }
    })
    
    # Start real-time sync
    sync_tasks = [
        framework.setup_real_time_sync("crm_system", ["events", "analytics"], 300),
        framework.setup_real_time_sync("facility_mgmt", ["alerts", "status"], 600)
    ]
    
    await asyncio.gather(*sync_tasks)

if __name__ == "__main__":
    asyncio.run(setup_custom_integrations())
```

## Testing and Validation

### Integration Testing

**Integration Test Suite**:
```python
#!/usr/bin/env python3
# integration_tests.py

import unittest
import requests
import time
from unittest.mock import patch, MagicMock

class IntegrationTestSuite(unittest.TestCase):
    
    def setUp(self):
        self.camera_ip = "192.168.1.100"
        self.api_key = "test_api_key"
        self.base_url = f"http://{self.camera_ip}:8080/api"
        
    def test_vms_integration(self):
        """Test VMS integration configuration"""
        vms_config = {
            "vms_type": "milestone",
            "configuration": {
                "manufacturer": "Rotoclear",
                "model": "RD-CAM-001"
            }
        }
        
        response = requests.post(
            f"{self.base_url}/integrations/vms/configure",
            json=vms_config,
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['success'])
    
    def test_cloud_storage_integration(self):
        """Test cloud storage integration"""
        cloud_config = {
            "provider": "aws_s3",
            "bucket": "test-bucket",
            "credentials": {
                "access_key": "test_key",
                "secret_key": "test_secret"
            }
        }
        
        response = requests.put(
            f"{self.base_url}/integrations/cloud/storage",
            json=cloud_config,
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        
        self.assertEqual(response.status_code, 200)
    
    def test_webhook_delivery(self):
        """Test webhook delivery"""
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            
            webhook_data = {
                "event_type": "motion_detected",
                "timestamp": "2025-01-15T10:30:00Z",
                "camera_id": "camera_001"
            }
            
            response = requests.post(
                f"{self.base_url}/integrations/webhooks/test",
                json=webhook_data,
                headers={'Authorization': f'Bearer {self.api_key}'}
            )
            
            self.assertEqual(response.status_code, 200)
            mock_post.assert_called_once()
    
    def test_analytics_integration(self):
        """Test analytics platform integration"""
        analytics_config = {
            "platform": "custom",
            "endpoint": "https://analytics.company.com/api",
            "api_key": "analytics_key"
        }
        
        response = requests.put(
            f"{self.base_url}/integrations/analytics",
            json=analytics_config,
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
```

## Related Documentation

- [API Reference](../api/http-api.md) - Core API for integrations
- [ONVIF Protocol](./onvif-protocol.md) - ONVIF standard integration
- [Authentication](../configuration/authentication.md) - Integration security
- [Monitoring](../operations/monitoring.md) - Integration monitoring

---

*Third-party integration documentation covering major platforms, protocols, and enterprise systems*
