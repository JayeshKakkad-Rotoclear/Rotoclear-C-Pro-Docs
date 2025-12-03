# JavaScript Client Examples

**Complete JavaScript integration examples for web applications and Node.js.**

## Browser-based Integration

### Basic HTML5 Setup
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RotorDream Camera Interface</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .video-container { position: relative; margin: 20px 0; }
        .controls { margin: 20px 0; }
        .button { padding: 10px 20px; margin: 5px; }
        .status { background: #f0f0f0; padding: 10px; margin: 10px 0; }
        .error { background: #ffe6e6; color: #cc0000; }
        .success { background: #e6ffe6; color: #006600; }
    </style>
</head>
<body>
    <div class="container">
        <h1>RotorDream Camera Control</h1>
        
        <!-- Live video feed -->
        <div class="video-container">
            <video id="videoFeed" width="1920" height="1080" controls autoplay muted>
                Your browser does not support the video tag.
            </video>
            <canvas id="snapshotCanvas" style="display:none;"></canvas>
        </div>
        
        <!-- Controls -->
        <div class="controls">
            <button id="connectBtn" class="button">Connect</button>
            <button id="captureBtn" class="button">Capture Image</button>
            <button id="startRecordingBtn" class="button">Start Recording</button>
            <button id="stopRecordingBtn" class="button">Stop Recording</button>
            <button id="refreshStatusBtn" class="button">Refresh Status</button>
        </div>
        
        <!-- Status display -->
        <div id="statusDisplay" class="status">
            <h3>System Status</h3>
            <pre id="statusContent">Not connected</pre>
        </div>
        
        <!-- File list -->
        <div id="filesList">
            <h3>Recordings</h3>
            <ul id="filesContent"></ul>
        </div>
    </div>

    <script src="rotordream-client.js"></script>
    <script>
        // Initialize client when page loads
        document.addEventListener('DOMContentLoaded', function() {
            const app = new RotorDreamApp();
            app.initialize();
        });
    </script>
</body>
</html>
```

### JavaScript Client Library
```javascript
// rotordream-client.js

class RotorDreamClient {
    constructor(baseUrl, options = {}) {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.token = options.token;
        this.username = options.username;
        this.password = options.password;
        this.timeout = options.timeout || 30000;
        
        // Default headers
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
        
        // Add authentication header
        if (this.token) {
            this.defaultHeaders['Authorization'] = `Bearer ${this.token}`;
        }
    }
    
    async _request(method, endpoint, options = {}) {
        const url = `${this.baseUrl}/${endpoint.replace(/^\//, '')}`;
        
        const config = {
            method: method,
            headers: { ...this.defaultHeaders, ...options.headers },
            signal: AbortSignal.timeout(this.timeout),
            ...options
        };
        
        // Add basic auth if provided
        if (this.username && this.password && !this.token) {
            config.headers['Authorization'] = 'Basic ' + btoa(`${this.username}:${this.password}`);
        }
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            
            // Return appropriate data type
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else if (contentType && contentType.includes('image/')) {
                return await response.blob();
            } else {
                return await response.arrayBuffer();
            }
            
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timeout');
            }
            throw error;
        }
    }
    
    // System information
    async getInfo() {
        return this._request('GET', '/api/info');
    }
    
    async getHealth() {
        return this._request('GET', '/health');
    }
    
    // Camera operations
    async getCameraStatus() {
        return this._request('GET', '/api/camera/status');
    }
    
    async captureImage(quality = 85) {
        const endpoint = quality !== 85 ? `/camera.jpeg?quality=${quality}` : '/camera.jpeg';
        return this._request('GET', endpoint);
    }
    
    async takeSnapshot(options = {}) {
        return this._request('POST', '/snapshot', {
            body: JSON.stringify(options)
        });
    }
    
    // Recording operations
    async startRecording(options = {}) {
        return this._request('POST', '/api/recording/start', {
            body: JSON.stringify(options)
        });
    }
    
    async stopRecording() {
        return this._request('POST', '/api/recording/stop');
    }
    
    async getRecordingStatus() {
        return this._request('GET', '/api/recording/status');
    }
    
    // File operations
    async listFiles(path = '/media/data', options = {}) {
        const params = new URLSearchParams({ path, ...options });
        return this._request('GET', `/files?${params}`);
    }
    
    async downloadFile(filepath) {
        return this._request('GET', `/download/${filepath}`);
    }
    
    async uploadFile(file, path = null, overwrite = false) {
        const formData = new FormData();
        formData.append('file', file);
        if (path) formData.append('path', path);
        if (overwrite) formData.append('overwrite', 'true');
        
        return this._request('POST', '/upload', {
            body: formData,
            headers: {} // Let browser set content-type for FormData
        });
    }
    
    async deleteFile(filepath) {
        return this._request('DELETE', `/files/${filepath}`);
    }
    
    // Configuration
    async getConfig(section = null) {
        const endpoint = section ? `/api/config/${section}` : '/api/config';
        return this._request('GET', endpoint);
    }
    
    async setConfig(section, config) {
        return this._request('PUT', `/api/config/${section}`, {
            body: JSON.stringify(config)
        });
    }
}

class RotorDreamWebSocket {
    constructor(wsUrl, options = {}) {
        this.wsUrl = wsUrl;
        this.token = options.token;
        this.ws = null;
        this.connected = false;
        this.callbacks = {};
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
        this.reconnectInterval = options.reconnectInterval || 3000;
    }
    
    connect() {
        return new Promise((resolve, reject) => {
            try {
                // Add authentication to WebSocket URL
                let url = this.wsUrl;
                if (this.token) {
                    const separator = url.includes('?') ? '&' : '?';
                    url += `${separator}token=${this.token}`;
                }
                
                this.ws = new WebSocket(url);
                
                this.ws.onopen = () => {
                    this.connected = true;
                    this.reconnectAttempts = 0;
                    console.log('WebSocket connected');
                    this._trigger('open');
                    resolve();
                };
                
                this.ws.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        this._handleMessage(data);
                    } catch (error) {
                        console.error('Failed to parse WebSocket message:', error);
                    }
                };
                
                this.ws.onclose = (event) => {
                    this.connected = false;
                    console.log('WebSocket disconnected:', event.code, event.reason);
                    this._trigger('close', { code: event.code, reason: event.reason });
                    
                    // Attempt reconnection
                    if (this.reconnectAttempts < this.maxReconnectAttempts) {
                        setTimeout(() => this._reconnect(), this.reconnectInterval);
                    }
                };
                
                this.ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                    this._trigger('error', error);
                    reject(error);
                };
                
            } catch (error) {
                reject(error);
            }
        });
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.connected = false;
    }
    
    _reconnect() {
        this.reconnectAttempts++;
        console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
        this.connect().catch(() => {
            // Will retry if under max attempts
        });
    }
    
    _handleMessage(data) {
        const messageType = data.type || 'unknown';
        this._trigger(messageType, data);
    }
    
    _trigger(event, data = null) {
        if (this.callbacks[event]) {
            this.callbacks[event].forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in ${event} callback:`, error);
                }
            });
        }
    }
    
    on(event, callback) {
        if (!this.callbacks[event]) {
            this.callbacks[event] = [];
        }
        this.callbacks[event].push(callback);
    }
    
    off(event, callback) {
        if (this.callbacks[event]) {
            const index = this.callbacks[event].indexOf(callback);
            if (index > -1) {
                this.callbacks[event].splice(index, 1);
            }
        }
    }
    
    send(type, data = {}) {
        if (!this.connected) {
            throw new Error('WebSocket not connected');
        }
        
        const message = { type, ...data };
        this.ws.send(JSON.stringify(message));
    }
    
    // Convenience methods
    subscribe(event) {
        this.send('subscribe', { event });
    }
    
    getState() {
        this.send('get_state');
    }
    
    setParameter(parameter, value) {
        this.send('set_parameter', { parameter, value });
    }
}

class RotorDreamApp {
    constructor() {
        this.config = {
            baseUrl: 'http://192.168.1.100:8080',
            wsUrl: 'ws://192.168.1.100:8080/ws',
            token: '1a2B3c4D5e6f7G8h' // Replace with actual token
        };
        
        this.client = new RotorDreamClient(this.config.baseUrl, {
            token: this.config.token
        });
        
        this.ws = new RotorDreamWebSocket(this.config.wsUrl, {
            token: this.config.token
        });
        
        this.recording = false;
        this.connected = false;
    }
    
    initialize() {
        this.setupEventListeners();
        this.setupWebSocket();
        this.updateUI();
    }
    
    setupEventListeners() {
        // Button event listeners
        document.getElementById('connectBtn').addEventListener('click', () => this.connect());
        document.getElementById('captureBtn').addEventListener('click', () => this.captureImage());
        document.getElementById('startRecordingBtn').addEventListener('click', () => this.startRecording());
        document.getElementById('stopRecordingBtn').addEventListener('click', () => this.stopRecording());
        document.getElementById('refreshStatusBtn').addEventListener('click', () => this.refreshStatus());
    }
    
    setupWebSocket() {
        this.ws.on('open', () => {
            console.log('Connected to WebSocket');
            this.ws.subscribe('state_changes');
            this.ws.subscribe('camera_events');
        });
        
        this.ws.on('state_update', (data) => {
            console.log('State update:', data);
            this.updateUI();
        });
        
        this.ws.on('camera_event', (data) => {
            console.log('Camera event:', data);
            if (data.event === 'frame_ready') {
                // Could update video feed here
            }
        });
        
        this.ws.on('error', (error) => {
            this.showStatus('WebSocket error: ' + error.message, 'error');
        });
    }
    
    async connect() {
        try {
            // Test HTTP connection
            const health = await this.client.getHealth();
            this.showStatus('HTTP connection successful', 'success');
            
            // Connect WebSocket
            await this.ws.connect();
            this.connected = true;
            
            // Load initial data
            await this.refreshStatus();
            await this.loadFilesList();
            
            this.updateUI();
            
        } catch (error) {
            this.showStatus('Connection failed: ' + error.message, 'error');
            console.error(error);
        }
    }
    
    async captureImage() {
        try {
            const imageBlob = await this.client.captureImage(90);
            
            // Display captured image
            const imageUrl = URL.createObjectURL(imageBlob);
            
            // Create download link
            const link = document.createElement('a');
            link.href = imageUrl;
            link.download = `capture_${Date.now()}.jpg`;
            link.textContent = 'Download Captured Image';
            
            // Show in UI
            this.showStatus('Image captured successfully', 'success');
            
            // Add to page
            const container = document.getElementById('statusDisplay');
            container.appendChild(link);
            
        } catch (error) {
            this.showStatus('Image capture failed: ' + error.message, 'error');
        }
    }
    
    async startRecording() {
        try {
            const options = {
                filename: `recording_${Date.now()}.avi`,
                quality: 'high',
                resolution: '1920x1080'
            };
            
            const result = await this.client.startRecording(options);
            this.recording = true;
            this.showStatus(`Recording started: ${result.filename}`, 'success');
            this.updateUI();
            
        } catch (error) {
            this.showStatus('Failed to start recording: ' + error.message, 'error');
        }
    }
    
    async stopRecording() {
        try {
            const result = await this.client.stopRecording();
            this.recording = false;
            this.showStatus(`Recording stopped: ${result.filename} (${result.duration}s)`, 'success');
            this.updateUI();
            
            // Refresh file list to show new recording
            setTimeout(() => this.loadFilesList(), 1000);
            
        } catch (error) {
            this.showStatus('Failed to stop recording: ' + error.message, 'error');
        }
    }
    
    async refreshStatus() {
        try {
            const [info, cameraStatus, recordingStatus] = await Promise.all([
                this.client.getInfo(),
                this.client.getCameraStatus(),
                this.client.getRecordingStatus()
            ]);
            
            this.recording = recordingStatus.recording;
            
            const statusText = `
System Information:
- Version: ${info.version}
- Uptime: ${Math.floor(info.uptime / 3600)}h ${Math.floor((info.uptime % 3600) / 60)}m
- Temperature: ${info.system.temperature}°C
- CPU Usage: ${info.system.cpu_usage}%
- Memory: ${Math.floor(info.system.memory.used / 1024 / 1024)}MB / ${Math.floor(info.system.memory.total / 1024 / 1024)}MB

Camera Status:
- Connected: ${cameraStatus.cameras[0]?.connected ? 'Yes' : 'No'}
- Resolution: ${cameraStatus.cameras[0]?.resolution || 'N/A'}
- Frame Rate: ${cameraStatus.cameras[0]?.framerate || 'N/A'} fps

Recording Status:
- Recording: ${recordingStatus.recording ? 'Yes' : 'No'}
${recordingStatus.recording ? `- Duration: ${recordingStatus.duration}s
- File: ${recordingStatus.filename}` : ''}
            `;
            
            document.getElementById('statusContent').textContent = statusText;
            this.updateUI();
            
        } catch (error) {
            this.showStatus('Failed to refresh status: ' + error.message, 'error');
        }
    }
    
    async loadFilesList() {
        try {
            const files = await this.client.listFiles('/media/data/recordings');
            const filesList = document.getElementById('filesContent');
            filesList.innerHTML = '';
            
            files.files.forEach(file => {
                if (file.type === 'file') {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <span>${file.name}</span>
                        <span>(${Math.floor(file.size / 1024 / 1024)}MB)</span>
                        <button onclick="downloadFile('${file.name}')">Download</button>
                        <button onclick="deleteFile('${file.name}')">Delete</button>
                    `;
                    filesList.appendChild(li);
                }
            });
            
        } catch (error) {
            this.showStatus('Failed to load files: ' + error.message, 'error');
        }
    }
    
    showStatus(message, type = 'info') {
        const statusDiv = document.getElementById('statusDisplay');
        statusDiv.className = `status ${type}`;
        
        const messageDiv = document.createElement('div');
        messageDiv.textContent = `${new Date().toLocaleTimeString()}: ${message}`;
        statusDiv.appendChild(messageDiv);
        
        // Auto-clear after 5 seconds for success/error messages
        if (type !== 'info') {
            setTimeout(() => {
                statusDiv.className = 'status';
            }, 5000);
        }
    }
    
    updateUI() {
        // Update button states
        const connectBtn = document.getElementById('connectBtn');
        const captureBtn = document.getElementById('captureBtn');
        const startRecordingBtn = document.getElementById('startRecordingBtn');
        const stopRecordingBtn = document.getElementById('stopRecordingBtn');
        
        connectBtn.textContent = this.connected ? 'Connected' : 'Connect';
        connectBtn.disabled = this.connected;
        
        captureBtn.disabled = !this.connected;
        startRecordingBtn.disabled = !this.connected || this.recording;
        stopRecordingBtn.disabled = !this.connected || !this.recording;
        
        // Update recording indicator
        if (this.recording) {
            startRecordingBtn.textContent = 'Recording...';
            startRecordingBtn.style.background = '#ff4444';
        } else {
            startRecordingBtn.textContent = 'Start Recording';
            startRecordingBtn.style.background = '';
        }
    }
}

// Global functions for file operations
async function downloadFile(filename) {
    try {
        const app = window.rotorDreamApp || new RotorDreamApp();
        const fileData = await app.client.downloadFile(`recordings/${filename}`);
        
        const blob = new Blob([fileData]);
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
    } catch (error) {
        alert('Download failed: ' + error.message);
    }
}

async function deleteFile(filename) {
    if (!confirm(`Delete ${filename}?`)) return;
    
    try {
        const app = window.rotorDreamApp || new RotorDreamApp();
        await app.client.deleteFile(`recordings/${filename}`);
        app.loadFilesList(); // Refresh list
        
    } catch (error) {
        alert('Delete failed: ' + error.message);
    }
}

// Make app globally available
window.RotorDreamApp = RotorDreamApp;
window.RotorDreamClient = RotorDreamClient;
window.RotorDreamWebSocket = RotorDreamWebSocket;
```

## Node.js Integration

### Server-side Node.js Client
```javascript
// rotordream-node-client.js
const axios = require('axios');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');

class RotorDreamNodeClient {
    constructor(baseUrl, options = {}) {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.token = options.token;
        this.username = options.username;
        this.password = options.password;
        
        // Configure axios instance
        this.http = axios.create({
            baseURL: this.baseUrl,
            timeout: options.timeout || 30000,
            headers: {
                'User-Agent': 'RotorDream-Node-Client/1.0'
            }
        });
        
        // Set up authentication
        if (this.token) {
            this.http.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        } else if (this.username && this.password) {
            this.http.defaults.auth = {
                username: this.username,
                password: this.password
            };
        }
        
        // Response interceptor for error handling
        this.http.interceptors.response.use(
            response => response,
            error => {
                if (error.response) {
                    const customError = new Error(`HTTP ${error.response.status}: ${error.response.statusText}`);
                    customError.status = error.response.status;
                    customError.data = error.response.data;
                    throw customError;
                }
                throw error;
            }
        );
    }
    
    // System information
    async getInfo() {
        const response = await this.http.get('/api/info');
        return response.data;
    }
    
    async getHealth() {
        const response = await this.http.get('/health');
        return response.data;
    }
    
    // Camera operations
    async getCameraStatus() {
        const response = await this.http.get('/api/camera/status');
        return response.data;
    }
    
    async captureImage(quality = 85, outputPath = null) {
        const params = quality !== 85 ? { quality } : {};
        const response = await this.http.get('/camera.jpeg', {
            params,
            responseType: 'arraybuffer'
        });
        
        if (outputPath) {
            fs.writeFileSync(outputPath, Buffer.from(response.data));
            return outputPath;
        }
        
        return Buffer.from(response.data);
    }
    
    // Recording operations
    async startRecording(options = {}) {
        const response = await this.http.post('/api/recording/start', options);
        return response.data;
    }
    
    async stopRecording() {
        const response = await this.http.post('/api/recording/stop');
        return response.data;
    }
    
    async getRecordingStatus() {
        const response = await this.http.get('/api/recording/status');
        return response.data;
    }
    
    // File operations
    async listFiles(directory = '/media/data', options = {}) {
        const params = { path: directory, ...options };
        const response = await this.http.get('/files', { params });
        return response.data;
    }
    
    async downloadFile(filepath, localPath = null) {
        const response = await this.http.get(`/download/${filepath}`, {
            responseType: 'stream'
        });
        
        if (localPath) {
            const writer = fs.createWriteStream(localPath);
            response.data.pipe(writer);
            
            return new Promise((resolve, reject) => {
                writer.on('finish', () => resolve(localPath));
                writer.on('error', reject);
            });
        }
        
        return response.data;
    }
    
    async uploadFile(localPath, remotePath = null, overwrite = false) {
        const formData = new FormData();
        formData.append('file', fs.createReadStream(localPath));
        
        if (remotePath) {
            formData.append('path', remotePath);
        }
        
        if (overwrite) {
            formData.append('overwrite', 'true');
        }
        
        const response = await this.http.post('/upload', formData, {
            headers: formData.getHeaders()
        });
        
        return response.data;
    }
    
    async deleteFile(filepath) {
        const response = await this.http.delete(`/files/${filepath}`);
        return response.data;
    }
    
    // Configuration
    async getConfig(section = null) {
        const endpoint = section ? `/api/config/${section}` : '/api/config';
        const response = await this.http.get(endpoint);
        return response.data;
    }
    
    async setConfig(section, config) {
        const response = await this.http.put(`/api/config/${section}`, config);
        return response.data;
    }
}

class RotorDreamNodeWebSocket {
    constructor(wsUrl, options = {}) {
        this.wsUrl = wsUrl;
        this.token = options.token;
        this.ws = null;
        this.connected = false;
        this.callbacks = {};
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
        this.reconnectInterval = options.reconnectInterval || 3000;
    }
    
    connect() {
        return new Promise((resolve, reject) => {
            try {
                // Add authentication to WebSocket URL
                let url = this.wsUrl;
                if (this.token) {
                    const separator = url.includes('?') ? '&' : '?';
                    url += `${separator}token=${this.token}`;
                }
                
                this.ws = new WebSocket(url);
                
                this.ws.on('open', () => {
                    this.connected = true;
                    this.reconnectAttempts = 0;
                    console.log('WebSocket connected');
                    this._trigger('open');
                    resolve();
                });
                
                this.ws.on('message', (data) => {
                    try {
                        const message = JSON.parse(data.toString());
                        this._handleMessage(message);
                    } catch (error) {
                        console.error('Failed to parse WebSocket message:', error);
                    }
                });
                
                this.ws.on('close', (code, reason) => {
                    this.connected = false;
                    console.log('WebSocket disconnected:', code, reason.toString());
                    this._trigger('close', { code, reason: reason.toString() });
                    
                    // Attempt reconnection
                    if (this.reconnectAttempts < this.maxReconnectAttempts) {
                        setTimeout(() => this._reconnect(), this.reconnectInterval);
                    }
                });
                
                this.ws.on('error', (error) => {
                    console.error('WebSocket error:', error);
                    this._trigger('error', error);
                    reject(error);
                });
                
            } catch (error) {
                reject(error);
            }
        });
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.connected = false;
    }
    
    _reconnect() {
        this.reconnectAttempts++;
        console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
        this.connect().catch(() => {
            // Will retry if under max attempts
        });
    }
    
    _handleMessage(data) {
        const messageType = data.type || 'unknown';
        this._trigger(messageType, data);
    }
    
    _trigger(event, data = null) {
        if (this.callbacks[event]) {
            this.callbacks[event].forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in ${event} callback:`, error);
                }
            });
        }
    }
    
    on(event, callback) {
        if (!this.callbacks[event]) {
            this.callbacks[event] = [];
        }
        this.callbacks[event].push(callback);
    }
    
    off(event, callback) {
        if (this.callbacks[event]) {
            const index = this.callbacks[event].indexOf(callback);
            if (index > -1) {
                this.callbacks[event].splice(index, 1);
            }
        }
    }
    
    send(type, data = {}) {
        if (!this.connected) {
            throw new Error('WebSocket not connected');
        }
        
        const message = { type, ...data };
        this.ws.send(JSON.stringify(message));
    }
    
    // Convenience methods
    subscribe(event) {
        this.send('subscribe', { event });
    }
    
    getState() {
        this.send('get_state');
    }
    
    setParameter(parameter, value) {
        this.send('set_parameter', { parameter, value });
    }
}

module.exports = {
    RotorDreamNodeClient,
    RotorDreamNodeWebSocket
};
```

### Node.js Usage Examples
```javascript
// examples/node-example.js
const { RotorDreamNodeClient, RotorDreamNodeWebSocket } = require('./rotordream-node-client');
const fs = require('fs');
const path = require('path');

async function main() {
    const client = new RotorDreamNodeClient('http://192.168.1.100:8080', {
        token: '1a2B3c4D5e6f7G8h'
    });
    
    try {
        // Test connection
        const health = await client.getHealth();
        console.log('Connection successful:', health);
        
        // Get system info
        const info = await client.getInfo();
        console.log('System version:', info.version);
        console.log('Temperature:', info.system.temperature + '°C');
        
        // Capture and save image
        const imagePath = `capture_${Date.now()}.jpg`;
        await client.captureImage(95, imagePath);
        console.log('Image saved:', imagePath);
        
        // Start recording
        const recording = await client.startRecording({
            filename: 'test_recording.avi',
            duration: 60,
            quality: 'high'
        });
        console.log('Recording started:', recording.recording_id);
        
        // Monitor recording status
        const checkStatus = setInterval(async () => {
            const status = await client.getRecordingStatus();
            console.log(`Recording: ${status.duration}s`);
            
            if (!status.recording) {
                clearInterval(checkStatus);
                console.log('Recording completed');
                
                // List and download recordings
                await listAndDownloadRecordings(client);
            }
        }, 5000);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

async function listAndDownloadRecordings(client) {
    try {
        const files = await client.listFiles('/media/data/recordings');
        console.log('Available recordings:');
        
        for (const file of files.files) {
            if (file.type === 'file' && file.name.endsWith('.avi')) {
                console.log(`- ${file.name} (${Math.floor(file.size / 1024 / 1024)}MB)`);
                
                // Download file
                const localPath = path.join('downloads', file.name);
                await client.downloadFile(`recordings/${file.name}`, localPath);
                console.log(`Downloaded: ${localPath}`);
            }
        }
        
    } catch (error) {
        console.error('File operations failed:', error.message);
    }
}

async function webSocketExample() {
    const ws = new RotorDreamNodeWebSocket('ws://192.168.1.100:8080/ws', {
        token: '1a2B3c4D5e6f7G8h'
    });
    
    // Set up event handlers
    ws.on('open', () => {
        console.log('WebSocket connected');
        ws.subscribe('state_changes');
        ws.subscribe('camera_events');
        ws.getState();
    });
    
    ws.on('state_update', (data) => {
        console.log('State update:', data.parameter, '=', data.value);
        
        if (data.parameter === 'system.temperature' && data.value > 70) {
            console.log('WARNING: High temperature!');
        }
    });
    
    ws.on('camera_event', (data) => {
        console.log('Camera event:', data.event);
    });
    
    ws.on('error', (error) => {
        console.error('WebSocket error:', error.message);
    });
    
    ws.on('close', (data) => {
        console.log('WebSocket closed:', data.code, data.reason);
    });
    
    // Connect
    try {
        await ws.connect();
        
        // Send some commands
        setTimeout(() => {
            ws.setParameter('camera.resolution', '1920x1080');
            ws.setParameter('camera.framerate', 30);
        }, 1000);
        
        // Keep alive for 30 seconds
        setTimeout(() => {
            ws.disconnect();
            process.exit(0);
        }, 30000);
        
    } catch (error) {
        console.error('WebSocket connection failed:', error.message);
    }
}

// Express.js REST API proxy example
const express = require('express');
const app = express();

app.use(express.json());
app.use(express.static('public')); // Serve HTML files

const client = new RotorDreamNodeClient('http://192.168.1.100:8080', {
    token: '1a2B3c4D5e6f7G8h'
});

// Proxy endpoints
app.get('/api/camera/image', async (req, res) => {
    try {
        const imageBuffer = await client.captureImage(90);
        res.setHeader('Content-Type', 'image/jpeg');
        res.send(imageBuffer);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/system/status', async (req, res) => {
    try {
        const [info, cameraStatus] = await Promise.all([
            client.getInfo(),
            client.getCameraStatus()
        ]);
        res.json({ system: info, camera: cameraStatus });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/recording/start', async (req, res) => {
    try {
        const result = await client.startRecording(req.body);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/recording/stop', async (req, res) => {
    try {
        const result = await client.stopRecording();
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Proxy server running on port ${PORT}`);
});

// Run examples
if (require.main === module) {
    // Uncomment to run specific examples
    // main();
    // webSocketExample();
}
```

### Real-time Dashboard Example
```javascript
// dashboard/dashboard.js
class RotorDreamDashboard {
    constructor() {
        this.client = new RotorDreamClient('http://192.168.1.100:8080', {
            token: '1a2B3c4D5e6f7G8h'
        });
        
        this.ws = new RotorDreamWebSocket('ws://192.168.1.100:8080/ws', {
            token: '1a2B3c4D5e6f7G8h'
        });
        
        this.charts = {};
        this.lastUpdate = Date.now();
        
        this.initializeCharts();
        this.setupWebSocket();
        this.startPolling();
    }
    
    initializeCharts() {
        // Temperature chart
        this.charts.temperature = new Chart(document.getElementById('temperatureChart'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Temperature (°C)',
                    data: [],
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 30,
                        max: 80
                    }
                },
                animation: false
            }
        });
        
        // CPU usage chart
        this.charts.cpu = new Chart(document.getElementById('cpuChart'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'CPU Usage (%)',
                    data: [],
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                animation: false
            }
        });
    }
    
    setupWebSocket() {
        this.ws.on('open', () => {
            console.log('Dashboard connected');
            this.ws.subscribe('state_changes');
            this.updateStatus('Connected', 'success');
        });
        
        this.ws.on('state_update', (data) => {
            this.handleStateUpdate(data);
        });
        
        this.ws.on('close', () => {
            this.updateStatus('Disconnected', 'error');
        });
        
        this.ws.connect();
    }
    
    handleStateUpdate(data) {
        const now = new Date();
        const timeLabel = now.toLocaleTimeString();
        
        if (data.parameter === 'system.temperature') {
            this.addDataPoint(this.charts.temperature, timeLabel, data.value);
            document.getElementById('currentTemp').textContent = data.value + '°C';
        }
        
        if (data.parameter === 'system.cpu_usage') {
            this.addDataPoint(this.charts.cpu, timeLabel, data.value);
            document.getElementById('currentCPU').textContent = data.value + '%';
        }
        
        this.lastUpdate = Date.now();
    }
    
    addDataPoint(chart, label, value) {
        chart.data.labels.push(label);
        chart.data.datasets[0].data.push(value);
        
        // Keep only last 20 points
        if (chart.data.labels.length > 20) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }
        
        chart.update('none');
    }
    
    async startPolling() {
        setInterval(async () => {
            try {
                const info = await this.client.getInfo();
                
                // Update displays
                document.getElementById('systemVersion').textContent = info.version;
                document.getElementById('systemUptime').textContent = this.formatUptime(info.uptime);
                
                // Update memory usage
                const memoryUsage = (info.system.memory.used / info.system.memory.total * 100).toFixed(1);
                document.getElementById('memoryUsage').textContent = memoryUsage + '%';
                
                // Update disk usage
                const diskUsage = (info.system.disk.used / info.system.disk.total * 100).toFixed(1);
                document.getElementById('diskUsage').textContent = diskUsage + '%';
                
                // Check camera status
                const cameraStatus = await this.client.getCameraStatus();
                const cameraConnected = cameraStatus.cameras[0]?.connected || false;
                document.getElementById('cameraStatus').textContent = cameraConnected ? 'Connected' : 'Disconnected';
                document.getElementById('cameraStatus').className = cameraConnected ? 'status-good' : 'status-bad';
                
            } catch (error) {
                console.error('Polling error:', error);
                this.updateStatus('Error: ' + error.message, 'error');
            }
        }, 5000);
    }
    
    formatUptime(seconds) {
        const days = Math.floor(seconds / 86400);
        const hours = Math.floor((seconds % 86400) / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        
        if (days > 0) {
            return `${days}d ${hours}h ${minutes}m`;
        } else if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else {
            return `${minutes}m`;
        }
    }
    
    updateStatus(message, type) {
        const statusElement = document.getElementById('connectionStatus');
        statusElement.textContent = message;
        statusElement.className = `status-${type}`;
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new RotorDreamDashboard();
    window.dashboard = dashboard;
});
```

## Related Documentation

- [Python Client](python-client.md) - Server-side Python integration
- [C# Client](csharp-client.md) - .NET application integration
- [WebSocket API](../websocket-api.md) - Real-time communication protocol
- [HTTP API](../http-api.md) - Complete REST API reference

---

*JavaScript examples tested with modern browsers (ES6+) and Node.js 16+. Requires axios, ws, and form-data packages for Node.js*
