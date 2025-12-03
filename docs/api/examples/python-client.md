# Python Client Examples

**Complete Python integration examples for camera control and data access.**

## Installation and Setup

### Requirements
```bash
pip install requests websocket-client opencv-python pillow numpy
```

### Basic Configuration
```python
import requests
import json
import cv2
import websocket
from PIL import Image
import io
import base64
import threading
import time

# Camera device configuration
CAMERA_IP = "192.168.1.100"
HTTP_PORT = 8080
HTTPS_PORT = 8081
WS_PORT = 8080
RTSP_PORT = 554

# Authentication
API_TOKEN = "1a2B3c4D5e6f7G8h"
USERNAME = "admin"
PASSWORD = "password"

# Base URLs
BASE_URL = f"http://{CAMERA_IP}:{HTTP_PORT}"
SECURE_URL = f"https://{CAMERA_IP}:{HTTPS_PORT}"
WS_URL = f"ws://{CAMERA_IP}:{WS_PORT}/ws"
RTSP_URL = f"rtsp://{USERNAME}:{PASSWORD}@{CAMERA_IP}:{RTSP_PORT}/stream0"
```

## HTTP API Client

### Basic API Client Class
```python
class RotorDreamClient:
    def __init__(self, base_url, token=None, username=None, password=None):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.session = requests.Session()
        
        # Configure authentication
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        elif username and password:
            self.session.auth = (username, password)
        
        # Configure session
        self.session.headers.update({
            "User-Agent": "RotorDream-Python-Client/1.0",
            "Accept": "application/json"
        })
        
    def _request(self, method, endpoint, **kwargs):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            # Return JSON if possible, otherwise raw content
            if 'application/json' in response.headers.get('content-type', ''):
                return response.json()
            return response.content
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise
    
    def get_info(self):
        """Get system information"""
        return self._request("GET", "/api/info")
    
    def get_camera_status(self):
        """Get camera hardware status"""
        return self._request("GET", "/api/camera/status")
    
    def capture_image(self, quality=85):
        """Capture current camera frame"""
        params = {"quality": quality} if quality != 85 else {}
        return self._request("GET", "/camera.jpeg", params=params)
    
    def start_recording(self, filename=None, duration=None, quality="high"):
        """Start video recording"""
        data = {
            "filename": filename or f"recording_{int(time.time())}.avi",
            "quality": quality
        }
        if duration:
            data["duration"] = duration
        
        return self._request("POST", "/api/recording/start", json=data)
    
    def stop_recording(self):
        """Stop current recording"""
        return self._request("POST", "/api/recording/stop")
    
    def get_recording_status(self):
        """Get recording status"""
        return self._request("GET", "/api/recording/status")
    
    def list_files(self, path="/media/data", recursive=False, filter_ext=None):
        """List files in directory"""
        params = {"path": path}
        if recursive:
            params["recursive"] = "true"
        if filter_ext:
            params["filter"] = filter_ext
        
        return self._request("GET", "/files", params=params)
    
    def download_file(self, filepath, local_path=None):
        """Download file from device"""
        content = self._request("GET", f"/download/{filepath}")
        
        if local_path:
            with open(local_path, 'wb') as f:
                f.write(content)
            return local_path
        return content
    
    def upload_file(self, file_path, remote_path=None, overwrite=False):
        """Upload file to device"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {}
            
            if remote_path:
                data['path'] = remote_path
            if overwrite:
                data['overwrite'] = 'true'
            
            return self._request("POST", "/upload", files=files, data=data)
    
    def delete_file(self, filepath):
        """Delete file from device"""
        return self._request("DELETE", f"/files/{filepath}")
```

### Usage Examples
```python
# Initialize client
client = RotorDreamClient(BASE_URL, token=API_TOKEN)

# Get system information
try:
    info = client.get_info()
    print(f"Device version: {info['version']}")
    print(f"Uptime: {info['uptime']} seconds")
    print(f"Temperature: {info['system']['temperature']}°C")
except Exception as e:
    print(f"Failed to get info: {e}")

# Capture image and save locally
try:
    image_data = client.capture_image(quality=95)
    with open("current_frame.jpg", "wb") as f:
        f.write(image_data)
    print("Image captured successfully")
except Exception as e:
    print(f"Failed to capture image: {e}")

# Start recording
try:
    recording_info = client.start_recording(
        filename="experiment_001.avi",
        duration=300,  # 5 minutes
        quality="high"
    )
    print(f"Recording started: {recording_info['recording_id']}")
    
    # Monitor recording status
    while True:
        status = client.get_recording_status()
        if not status['recording']:
            break
        print(f"Recording... Duration: {status['duration']}s")
        time.sleep(5)
        
except Exception as e:
    print(f"Recording failed: {e}")

# List and download files
try:
    files = client.list_files("/media/data/recordings", filter_ext=".avi")
    print(f"Found {len(files['files'])} video files")
    
    for file_info in files['files']:
        if file_info['type'] == 'file':
            print(f"- {file_info['name']} ({file_info['size']} bytes)")
            
            # Download the file
            local_filename = f"downloads/{file_info['name']}"
            client.download_file(f"recordings/{file_info['name']}", local_filename)
            print(f"Downloaded to {local_filename}")
            
except Exception as e:
    print(f"File operations failed: {e}")
```

## WebSocket Real-time Client

### WebSocket Client Class
```python
import websocket
import json
import threading

class RotorDreamWebSocketClient:
    def __init__(self, ws_url, token=None):
        self.ws_url = ws_url
        self.token = token
        self.ws = None
        self.connected = False
        self.callbacks = {}
        
    def connect(self):
        """Connect to WebSocket server"""
        headers = []
        if self.token:
            headers.append(f"Authorization: Bearer {self.token}")
            
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            header=headers,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        
        # Start in separate thread
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()
        
        # Wait for connection
        for _ in range(50):  # 5 second timeout
            if self.connected:
                break
            time.sleep(0.1)
        
        return self.connected
    
    def disconnect(self):
        """Disconnect from WebSocket server"""
        if self.ws:
            self.ws.close()
            
    def _on_open(self, ws):
        """WebSocket connection opened"""
        self.connected = True
        print("WebSocket connected")
        
    def _on_message(self, ws, message):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            message_type = data.get('type', 'unknown')
            
            # Call registered callback
            if message_type in self.callbacks:
                self.callbacks[message_type](data)
            else:
                print(f"Unhandled message type: {message_type}")
                print(f"Data: {data}")
                
        except json.JSONDecodeError:
            print(f"Invalid JSON message: {message}")
    
    def _on_error(self, ws, error):
        """Handle WebSocket error"""
        print(f"WebSocket error: {error}")
        
    def _on_close(self, ws, close_status_code, close_msg):
        """WebSocket connection closed"""
        self.connected = False
        print("WebSocket disconnected")
    
    def send_message(self, message_type, data=None):
        """Send message to server"""
        if not self.connected:
            raise Exception("WebSocket not connected")
            
        message = {"type": message_type}
        if data:
            message.update(data)
            
        self.ws.send(json.dumps(message))
    
    def subscribe_to_state(self, callback):
        """Subscribe to state updates"""
        self.callbacks['state_update'] = callback
        self.send_message('subscribe', {'event': 'state_changes'})
    
    def subscribe_to_camera_events(self, callback):
        """Subscribe to camera events"""
        self.callbacks['camera_event'] = callback
        self.send_message('subscribe', {'event': 'camera_events'})
    
    def get_current_state(self):
        """Request current system state"""
        self.send_message('get_state')
    
    def set_parameter(self, parameter, value):
        """Set system parameter"""
        self.send_message('set_parameter', {
            'parameter': parameter,
            'value': value
        })
```

### WebSocket Usage Examples
```python
# WebSocket event handlers
def on_state_update(data):
    """Handle state change notifications"""
    print(f"State updated: {data['parameter']} = {data['value']}")
    
    # React to specific state changes
    if data['parameter'] == 'camera.recording':
        if data['value']:
            print("Recording started!")
        else:
            print("Recording stopped!")
    
    elif data['parameter'] == 'system.temperature':
        temp = data['value']
        if temp > 70:
            print(f"WARNING: High temperature: {temp}°C")

def on_camera_event(data):
    """Handle camera events"""
    event_type = data.get('event')
    
    if event_type == 'frame_ready':
        print("New frame available")
    elif event_type == 'camera_disconnected':
        print("Camera disconnected!")
    elif event_type == 'camera_connected':
        print("Camera connected")

# Connect and subscribe
ws_client = RotorDreamWebSocketClient(WS_URL, token=API_TOKEN)

if ws_client.connect():
    # Subscribe to events
    ws_client.subscribe_to_state(on_state_update)
    ws_client.subscribe_to_camera_events(on_camera_event)
    
    # Get current state
    ws_client.get_current_state()
    
    # Set some parameters
    ws_client.set_parameter('camera.resolution', '1920x1080')
    ws_client.set_parameter('camera.framerate', 30)
    
    # Keep running to receive events
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        ws_client.disconnect()
else:
    print("Failed to connect to WebSocket")
```

## RTSP Video Streaming

### OpenCV RTSP Client
```python
import cv2
import numpy as np
import threading
import queue

class RTSPVideoStream:
    def __init__(self, rtsp_url, buffer_size=1):
        self.rtsp_url = rtsp_url
        self.buffer_size = buffer_size
        self.cap = None
        self.frame_queue = queue.Queue(maxsize=buffer_size)
        self.running = False
        self.thread = None
        
    def start(self):
        """Start video capture thread"""
        self.cap = cv2.VideoCapture(self.rtsp_url)
        
        # Configure capture
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, self.buffer_size)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        if not self.cap.isOpened():
            raise Exception(f"Failed to open RTSP stream: {self.rtsp_url}")
        
        self.running = True
        self.thread = threading.Thread(target=self._capture_frames)
        self.thread.daemon = True
        self.thread.start()
        
        return True
    
    def stop(self):
        """Stop video capture"""
        self.running = False
        if self.thread:
            self.thread.join()
        if self.cap:
            self.cap.release()
    
    def _capture_frames(self):
        """Capture frames in background thread"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break
            
            # Add to queue, dropping old frames if full
            try:
                self.frame_queue.put_nowait(frame)
            except queue.Full:
                try:
                    self.frame_queue.get_nowait()  # Remove old frame
                    self.frame_queue.put_nowait(frame)  # Add new frame
                except queue.Empty:
                    pass
    
    def get_frame(self, timeout=1.0):
        """Get latest frame"""
        try:
            return self.frame_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def get_properties(self):
        """Get stream properties"""
        if not self.cap:
            return None
        
        return {
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': self.cap.get(cv2.CAP_PROP_FPS),
            'fourcc': int(self.cap.get(cv2.CAP_PROP_FOURCC))
        }

# Usage example
def rtsp_stream_example():
    """Example of RTSP stream processing"""
    stream = RTSPVideoStream(RTSP_URL)
    
    try:
        if stream.start():
            props = stream.get_properties()
            print(f"Stream properties: {props}")
            
            frame_count = 0
            start_time = time.time()
            
            while True:
                frame = stream.get_frame()
                if frame is None:
                    continue
                
                frame_count += 1
                
                # Process frame (example: edge detection)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 50, 150)
                
                # Display frames
                cv2.imshow('Original', frame)
                cv2.imshow('Edges', edges)
                
                # Calculate FPS
                if frame_count % 30 == 0:
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed
                    print(f"Processing FPS: {fps:.2f}")
                
                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
    except Exception as e:
        print(f"RTSP stream error: {e}")
    finally:
        stream.stop()
        cv2.destroyAllWindows()

# Run the example
if __name__ == "__main__":
    rtsp_stream_example()
```

## Advanced Integration Examples

### Automated Monitoring System
```python
import schedule
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class CameraMonitoringSystem:
    def __init__(self, client, ws_client=None):
        self.client = client
        self.ws_client = ws_client
        self.alerts_enabled = True
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': 'alerts@company.com',
            'password': 'app_password',
            'recipients': ['admin@company.com']
        }
    
    def check_system_health(self):
        """Check system health and send alerts if needed"""
        try:
            info = self.client.get_info()
            temp = info['system']['temperature']
            cpu = info['system']['cpu_usage']
            disk_free = info['system']['disk']['available']
            
            # Check temperature
            if temp > 70:
                self.send_alert(f"High temperature: {temp}°C", include_image=True)
            
            # Check CPU usage
            if cpu > 90:
                self.send_alert(f"High CPU usage: {cpu}%")
            
            # Check disk space (less than 1GB)
            if disk_free < 1024 * 1024 * 1024:
                self.send_alert(f"Low disk space: {disk_free / (1024**3):.1f}GB remaining")
            
            print(f"Health check: Temp={temp}°C, CPU={cpu}%, Disk={disk_free/(1024**3):.1f}GB")
            
        except Exception as e:
            self.send_alert(f"Health check failed: {e}")
    
    def capture_and_analyze(self):
        """Capture image and perform basic analysis"""
        try:
            # Capture image
            image_data = self.client.capture_image(quality=95)
            
            # Convert to OpenCV format
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Basic analysis (brightness, motion detection, etc.)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            
            # Check if image is too dark (possible camera issue)
            if brightness < 10:
                self.send_alert("Camera image too dark - possible hardware issue", 
                              include_image=True)
            
            # Save timestamped image
            timestamp = int(time.time())
            filename = f"captures/capture_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            
            return {
                'brightness': brightness,
                'filename': filename,
                'timestamp': timestamp
            }
            
        except Exception as e:
            print(f"Capture analysis failed: {e}")
            return None
    
    def send_alert(self, message, include_image=False):
        """Send email alert"""
        if not self.alerts_enabled:
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['username']
            msg['To'] = ', '.join(self.email_config['recipients'])
            msg['Subject'] = f"Camera Alert: {message}"
            
            # Add text
            body = f"""
            Camera Alert Notification
            
            Message: {message}
            Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
            Device IP: {CAMERA_IP}
            
            Please check the camera system.
            """
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach image if requested
            if include_image:
                try:
                    image_data = self.client.capture_image()
                    img = MIMEImage(image_data)
                    img.add_header('Content-Disposition', 'attachment', filename='alert_image.jpg')
                    msg.attach(img)
                except:
                    pass  # Continue without image if capture fails
            
            # Send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            server.send_message(msg)
            server.quit()
            
            print(f"Alert sent: {message}")
            
        except Exception as e:
            print(f"Failed to send alert: {e}")
    
    def run_monitoring(self):
        """Start monitoring system"""
        # Schedule regular checks
        schedule.every(5).minutes.do(self.check_system_health)
        schedule.every(1).hours.do(self.capture_and_analyze)
        
        print("Starting monitoring system...")
        while True:
            schedule.run_pending()
            time.sleep(60)

# Initialize monitoring
client = RotorDreamClient(BASE_URL, token=API_TOKEN)
monitor = CameraMonitoringSystem(client)

# Start monitoring (run in background)
# monitor.run_monitoring()
```

### Time-lapse Creation
```python
def create_timelapse(duration_hours=24, interval_seconds=300, output_file="timelapse.mp4"):
    """Create time-lapse video from captured frames"""
    
    client = RotorDreamClient(BASE_URL, token=API_TOKEN)
    frames_dir = "timelapse_frames"
    os.makedirs(frames_dir, exist_ok=True)
    
    total_frames = int((duration_hours * 3600) / interval_seconds)
    frame_count = 0
    
    print(f"Creating time-lapse: {total_frames} frames over {duration_hours} hours")
    
    try:
        for i in range(total_frames):
            # Capture frame
            image_data = client.capture_image(quality=90)
            
            # Save frame
            frame_path = os.path.join(frames_dir, f"frame_{i:06d}.jpg")
            with open(frame_path, "wb") as f:
                f.write(image_data)
            
            frame_count += 1
            print(f"Captured frame {frame_count}/{total_frames}")
            
            # Wait for next interval
            if i < total_frames - 1:
                time.sleep(interval_seconds)
        
        # Create video from frames using ffmpeg
        cmd = [
            "ffmpeg", "-y",
            "-framerate", "30",
            "-i", os.path.join(frames_dir, "frame_%06d.jpg"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "23",
            output_file
        ]
        
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Time-lapse created: {output_file}")
        else:
            print(f"FFmpeg error: {result.stderr}")
    
    except KeyboardInterrupt:
        print(f"Time-lapse interrupted. Created {frame_count} frames.")
    except Exception as e:
        print(f"Time-lapse creation failed: {e}")

# Create 24-hour time-lapse with 5-minute intervals
# create_timelapse(duration_hours=24, interval_seconds=300)
```

## Error Handling and Debugging

### Comprehensive Error Handling
```python
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('camera_client.log'),
        logging.StreamHandler()
    ]
)

class RobustRotorDreamClient(RotorDreamClient):
    def __init__(self, base_url, token=None, username=None, password=None):
        super().__init__(base_url, token, username, password)
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _request(self, method, endpoint, **kwargs):
        """Enhanced request with better error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            self.logger.debug(f"Making {method} request to {url}")
            response = self.session.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            
            if 'application/json' in response.headers.get('content-type', ''):
                return response.json()
            return response.content
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout for {url}")
            raise
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connection error for {url}")
            raise
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error {e.response.status_code} for {url}")
            if e.response.status_code == 401:
                self.logger.error("Authentication failed - check credentials")
            elif e.response.status_code == 403:
                self.logger.error("Access forbidden - check permissions")
            elif e.response.status_code == 404:
                self.logger.error("Endpoint not found")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error for {url}: {e}")
            raise

# Test connection and diagnostics
def test_connection():
    """Test connection and diagnose issues"""
    client = RobustRotorDreamClient(BASE_URL, token=API_TOKEN)
    
    # Test basic connectivity
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Health check: {response.status_code}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False
    
    # Test authentication
    try:
        info = client.get_info()
        print(f"Authentication successful. Device version: {info['version']}")
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False
    
    # Test camera
    try:
        status = client.get_camera_status()
        print(f"Camera status: {status}")
    except Exception as e:
        print(f"Camera check failed: {e}")
    
    return True

if __name__ == "__main__":
    print("Testing camera connection...")
    if test_connection():
        print("✓ Connection test passed")
    else:
        print("✗ Connection test failed")
```

## Related Documentation

- [JavaScript Client](javascript-client.md) - Web browser integration
- [C# Client](csharp-client.md) - .NET application integration  
- [HTTP API](../http-api.md) - Complete REST API reference
- [WebSocket API](../websocket-api.md) - Real-time communication protocol

---

*Python examples tested with Python 3.8+ and libraries: requests 2.28+, opencv-python 4.6+, websocket-client 1.4+*
