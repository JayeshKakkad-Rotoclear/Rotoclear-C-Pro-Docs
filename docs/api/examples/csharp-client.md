# C# Client Examples

**Complete .NET integration examples for desktop applications and services.**

## NuGet Package Dependencies

```xml
<PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
<PackageReference Include="System.Net.Http" Version="4.3.4" />
<PackageReference Include="WebSocketSharp" Version="1.0.3-rc11" />
<PackageReference Include="OpenCvSharp4" Version="4.8.0.20230708" />
<PackageReference Include="OpenCvSharp4.runtime.win" Version="4.8.0.20230708" />
```

## Core Client Implementation

### HTTP API Client
```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.Net.Http.Headers;

namespace RotorDream.Client
{
    public class RotorDreamHttpClient : IDisposable
    {
        private readonly HttpClient _httpClient;
        private readonly string _baseUrl;
        private readonly string _token;
        
        public RotorDreamHttpClient(string baseUrl, string token = null, string username = null, string password = null)
        {
            _baseUrl = baseUrl.TrimEnd('/');
            _token = token;
            
            _httpClient = new HttpClient()
            {
                Timeout = TimeSpan.FromSeconds(30)
            };
            
            // Configure authentication
            if (!string.IsNullOrEmpty(token))
            {
                _httpClient.DefaultRequestHeaders.Authorization = 
                    new AuthenticationHeaderValue("Bearer", token);
            }
            else if (!string.IsNullOrEmpty(username) && !string.IsNullOrEmpty(password))
            {
                var credentials = Convert.ToBase64String(Encoding.ASCII.GetBytes($"{username}:{password}"));
                _httpClient.DefaultRequestHeaders.Authorization = 
                    new AuthenticationHeaderValue("Basic", credentials);
            }
            
            _httpClient.DefaultRequestHeaders.Add("User-Agent", "RotorDream-CSharp-Client/1.0");
        }
        
        private async Task<T> SendRequestAsync<T>(HttpMethod method, string endpoint, object data = null)
        {
            var url = $"{_baseUrl}/{endpoint.TrimStart('/')}";
            var request = new HttpRequestMessage(method, url);
            
            if (data != null)
            {
                var json = JsonConvert.SerializeObject(data);
                request.Content = new StringContent(json, Encoding.UTF8, "application/json");
            }
            
            try
            {
                var response = await _httpClient.SendAsync(request);
                response.EnsureSuccessStatusCode();
                
                var responseContent = await response.Content.ReadAsStringAsync();
                
                if (typeof(T) == typeof(string))
                {
                    return (T)(object)responseContent;
                }
                else if (typeof(T) == typeof(byte[]))
                {
                    return (T)(object)await response.Content.ReadAsByteArrayAsync();
                }
                else
                {
                    return JsonConvert.DeserializeObject<T>(responseContent);
                }
            }
            catch (HttpRequestException ex)
            {
                throw new RotorDreamException($"HTTP request failed: {ex.Message}", ex);
            }
            catch (TaskCanceledException ex)
            {
                throw new RotorDreamException("Request timeout", ex);
            }
        }
        
        // System Information
        public async Task<SystemInfo> GetInfoAsync()
        {
            return await SendRequestAsync<SystemInfo>(HttpMethod.Get, "/api/info");
        }
        
        public async Task<HealthStatus> GetHealthAsync()
        {
            return await SendRequestAsync<HealthStatus>(HttpMethod.Get, "/health");
        }
        
        // Camera Operations
        public async Task<CameraStatus> GetCameraStatusAsync()
        {
            return await SendRequestAsync<CameraStatus>(HttpMethod.Get, "/api/camera/status");
        }
        
        public async Task<byte[]> CaptureImageAsync(int quality = 85)
        {
            var endpoint = quality != 85 ? $"/camera.jpeg?quality={quality}" : "/camera.jpeg";
            return await SendRequestAsync<byte[]>(HttpMethod.Get, endpoint);
        }
        
        public async Task<SnapshotResult> TakeSnapshotAsync(SnapshotOptions options = null)
        {
            return await SendRequestAsync<SnapshotResult>(HttpMethod.Post, "/snapshot", options);
        }
        
        // Recording Operations
        public async Task<RecordingResult> StartRecordingAsync(RecordingOptions options = null)
        {
            return await SendRequestAsync<RecordingResult>(HttpMethod.Post, "/api/recording/start", options);
        }
        
        public async Task<RecordingResult> StopRecordingAsync()
        {
            return await SendRequestAsync<RecordingResult>(HttpMethod.Post, "/api/recording/stop");
        }
        
        public async Task<RecordingStatus> GetRecordingStatusAsync()
        {
            return await SendRequestAsync<RecordingStatus>(HttpMethod.Get, "/api/recording/status");
        }
        
        // File Operations
        public async Task<FileListResult> ListFilesAsync(string path = "/media/data", bool recursive = false, string filter = null)
        {
            var query = $"path={Uri.EscapeDataString(path)}";
            if (recursive) query += "&recursive=true";
            if (!string.IsNullOrEmpty(filter)) query += $"&filter={Uri.EscapeDataString(filter)}";
            
            return await SendRequestAsync<FileListResult>(HttpMethod.Get, $"/files?{query}");
        }
        
        public async Task<byte[]> DownloadFileAsync(string filepath)
        {
            return await SendRequestAsync<byte[]>(HttpMethod.Get, $"/download/{filepath}");
        }
        
        public async Task DownloadFileAsync(string filepath, string localPath)
        {
            var data = await DownloadFileAsync(filepath);
            await File.WriteAllBytesAsync(localPath, data);
        }
        
        public async Task<UploadResult> UploadFileAsync(string localPath, string remotePath = null, bool overwrite = false)
        {
            using var form = new MultipartFormDataContent();
            using var fileStream = File.OpenRead(localPath);
            using var fileContent = new StreamContent(fileStream);
            
            fileContent.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
            form.Add(fileContent, "file", Path.GetFileName(localPath));
            
            if (!string.IsNullOrEmpty(remotePath))
            {
                form.Add(new StringContent(remotePath), "path");
            }
            
            if (overwrite)
            {
                form.Add(new StringContent("true"), "overwrite");
            }
            
            var response = await _httpClient.PostAsync($"{_baseUrl}/upload", form);
            response.EnsureSuccessStatusCode();
            
            var responseContent = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<UploadResult>(responseContent);
        }
        
        public async Task DeleteFileAsync(string filepath)
        {
            await SendRequestAsync<object>(HttpMethod.Delete, $"/files/{filepath}");
        }
        
        // Configuration
        public async Task<Dictionary<string, object>> GetConfigAsync(string section = null)
        {
            var endpoint = string.IsNullOrEmpty(section) ? "/api/config" : $"/api/config/{section}";
            return await SendRequestAsync<Dictionary<string, object>>(HttpMethod.Get, endpoint);
        }
        
        public async Task SetConfigAsync(string section, object config)
        {
            await SendRequestAsync<object>(HttpMethod.Put, $"/api/config/{section}", config);
        }
        
        public void Dispose()
        {
            _httpClient?.Dispose();
        }
    }
    
    // Data Models
    public class SystemInfo
    {
        public string Version { get; set; }
        public string Build { get; set; }
        public int Uptime { get; set; }
        public SystemDetails System { get; set; }
        public CameraInfo Camera { get; set; }
        public NetworkInfo Network { get; set; }
    }
    
    public class SystemDetails
    {
        public double Temperature { get; set; }
        [JsonProperty("cpu_usage")]
        public double CpuUsage { get; set; }
        public MemoryInfo Memory { get; set; }
        public DiskInfo Disk { get; set; }
    }
    
    public class MemoryInfo
    {
        public long Total { get; set; }
        public long Available { get; set; }
        public long Used { get; set; }
    }
    
    public class DiskInfo
    {
        public long Total { get; set; }
        public long Available { get; set; }
        public long Used { get; set; }
    }
    
    public class CameraInfo
    {
        public bool Connected { get; set; }
        public string Resolution { get; set; }
        public int Framerate { get; set; }
        public bool Recording { get; set; }
    }
    
    public class NetworkInfo
    {
        public string Ip { get; set; }
        public string Hostname { get; set; }
        public bool Connected { get; set; }
    }
    
    public class HealthStatus
    {
        public string Status { get; set; }
        public DateTime Timestamp { get; set; }
        public Dictionary<string, string> Checks { get; set; }
    }
    
    public class CameraStatus
    {
        public List<CameraDevice> Cameras { get; set; }
        [JsonProperty("active_camera")]
        public int ActiveCamera { get; set; }
        public bool Streaming { get; set; }
    }
    
    public class CameraDevice
    {
        public int Id { get; set; }
        public bool Connected { get; set; }
        public string Device { get; set; }
        public string Resolution { get; set; }
        public int Framerate { get; set; }
        public string Format { get; set; }
    }
    
    public class RecordingOptions
    {
        public string Filename { get; set; }
        public int? Duration { get; set; }
        public string Quality { get; set; } = "high";
        public string Resolution { get; set; } = "1920x1080";
        public int Framerate { get; set; } = 30;
    }
    
    public class RecordingResult
    {
        public bool Success { get; set; }
        [JsonProperty("recording_id")]
        public string RecordingId { get; set; }
        public string Filename { get; set; }
        public int? Duration { get; set; }
        [JsonProperty("file_size")]
        public long? FileSize { get; set; }
        [JsonProperty("estimated_size")]
        public long? EstimatedSize { get; set; }
    }
    
    public class RecordingStatus
    {
        public bool Recording { get; set; }
        [JsonProperty("recording_id")]
        public string RecordingId { get; set; }
        public string Filename { get; set; }
        public int Duration { get; set; }
        [JsonProperty("estimated_size")]
        public long EstimatedSize { get; set; }
        [JsonProperty("remaining_space")]
        public long RemainingSpace { get; set; }
    }
    
    public class SnapshotOptions
    {
        public string Filename { get; set; }
        public int Quality { get; set; } = 95;
        [JsonProperty("addTimestamp")]
        public bool AddTimestamp { get; set; } = true;
    }
    
    public class SnapshotResult
    {
        public bool Success { get; set; }
        public string Filename { get; set; }
        public string Path { get; set; }
        public long Size { get; set; }
        public DateTime Timestamp { get; set; }
    }
    
    public class FileListResult
    {
        public string Path { get; set; }
        public List<FileInfo> Files { get; set; }
        [JsonProperty("total_size")]
        public long TotalSize { get; set; }
        [JsonProperty("file_count")]
        public int FileCount { get; set; }
        [JsonProperty("directory_count")]
        public int DirectoryCount { get; set; }
    }
    
    public class FileInfo
    {
        public string Name { get; set; }
        public long Size { get; set; }
        public DateTime Modified { get; set; }
        public string Type { get; set; }
        [JsonProperty("mime_type")]
        public string MimeType { get; set; }
    }
    
    public class UploadResult
    {
        public bool Success { get; set; }
        public string Filename { get; set; }
        public string Path { get; set; }
        public long Size { get; set; }
    }
    
    public class RotorDreamException : Exception
    {
        public RotorDreamException(string message) : base(message) { }
        public RotorDreamException(string message, Exception innerException) : base(message, innerException) { }
    }
}
```

### WebSocket Client
```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using WebSocketSharp;
using Newtonsoft.Json;

namespace RotorDream.Client
{
    public class RotorDreamWebSocketClient : IDisposable
    {
        private WebSocket _webSocket;
        private readonly string _wsUrl;
        private readonly string _token;
        private readonly Dictionary<string, List<Action<dynamic>>> _callbacks;
        private bool _isConnected;
        
        public event Action OnConnected;
        public event Action<string> OnDisconnected;
        public event Action<Exception> OnError;
        
        public bool IsConnected => _isConnected;
        
        public RotorDreamWebSocketClient(string wsUrl, string token = null)
        {
            _wsUrl = wsUrl;
            _token = token;
            _callbacks = new Dictionary<string, List<Action<dynamic>>>();
        }
        
        public async Task<bool> ConnectAsync()
        {
            return await Task.Run(() => Connect());
        }
        
        public bool Connect()
        {
            try
            {
                var url = _wsUrl;
                if (!string.IsNullOrEmpty(_token))
                {
                    var separator = url.Contains("?") ? "&" : "?";
                    url += $"{separator}token={_token}";
                }
                
                _webSocket = new WebSocket(url);
                
                _webSocket.OnOpen += (sender, e) =>
                {
                    _isConnected = true;
                    OnConnected?.Invoke();
                };
                
                _webSocket.OnMessage += (sender, e) =>
                {
                    try
                    {
                        var data = JsonConvert.DeserializeObject<dynamic>(e.Data);
                        HandleMessage(data);
                    }
                    catch (Exception ex)
                    {
                        OnError?.Invoke(new Exception($"Failed to parse message: {ex.Message}"));
                    }
                };
                
                _webSocket.OnClose += (sender, e) =>
                {
                    _isConnected = false;
                    OnDisconnected?.Invoke($"Code: {e.Code}, Reason: {e.Reason}");
                };
                
                _webSocket.OnError += (sender, e) =>
                {
                    OnError?.Invoke(new Exception(e.Message));
                };
                
                _webSocket.Connect();
                
                // Wait for connection (with timeout)
                var timeout = DateTime.Now.AddSeconds(10);
                while (!_isConnected && DateTime.Now < timeout)
                {
                    System.Threading.Thread.Sleep(100);
                }
                
                return _isConnected;
            }
            catch (Exception ex)
            {
                OnError?.Invoke(ex);
                return false;
            }
        }
        
        public void Disconnect()
        {
            if (_webSocket != null && _webSocket.IsAlive)
            {
                _webSocket.Close();
            }
            _isConnected = false;
        }
        
        private void HandleMessage(dynamic data)
        {
            try
            {
                string messageType = data.type ?? "unknown";
                
                if (_callbacks.ContainsKey(messageType))
                {
                    foreach (var callback in _callbacks[messageType])
                    {
                        try
                        {
                            callback(data);
                        }
                        catch (Exception ex)
                        {
                            OnError?.Invoke(new Exception($"Error in {messageType} callback: {ex.Message}"));
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                OnError?.Invoke(new Exception($"Error handling message: {ex.Message}"));
            }
        }
        
        public void On(string eventType, Action<dynamic> callback)
        {
            if (!_callbacks.ContainsKey(eventType))
            {
                _callbacks[eventType] = new List<Action<dynamic>>();
            }
            _callbacks[eventType].Add(callback);
        }
        
        public void Off(string eventType, Action<dynamic> callback)
        {
            if (_callbacks.ContainsKey(eventType))
            {
                _callbacks[eventType].Remove(callback);
            }
        }
        
        public void Send(string type, object data = null)
        {
            if (!_isConnected)
            {
                throw new InvalidOperationException("WebSocket not connected");
            }
            
            var message = new Dictionary<string, object> { ["type"] = type };
            if (data != null)
            {
                var dataDict = JsonConvert.DeserializeObject<Dictionary<string, object>>(
                    JsonConvert.SerializeObject(data));
                foreach (var kvp in dataDict)
                {
                    message[kvp.Key] = kvp.Value;
                }
            }
            
            var json = JsonConvert.SerializeObject(message);
            _webSocket.Send(json);
        }
        
        // Convenience methods
        public void Subscribe(string eventName)
        {
            Send("subscribe", new { @event = eventName });
        }
        
        public void GetState()
        {
            Send("get_state");
        }
        
        public void SetParameter(string parameter, object value)
        {
            Send("set_parameter", new { parameter, value });
        }
        
        public void Dispose()
        {
            Disconnect();
            _webSocket?.Close();
        }
    }
}
```

## Usage Examples

### Basic Console Application
```csharp
using System;
using System.IO;
using System.Threading.Tasks;
using RotorDream.Client;

namespace RotorDream.Console
{
    class Program
    {
        private const string BaseUrl = "http://192.168.1.100:8080";
        private const string WsUrl = "ws://192.168.1.100:8080/ws";
        private const string Token = "1a2B3c4D5e6f7G8h";
        
        static async Task Main(string[] args)
        {
            var client = new RotorDreamHttpClient(BaseUrl, Token);
            
            try
            {
                // Test connection
                var health = await client.GetHealthAsync();
                Console.WriteLine($"Connection status: {health.Status}");
                
                // Get system information
                var info = await client.GetInfoAsync();
                Console.WriteLine($"Device version: {info.Version}");
                Console.WriteLine($"Temperature: {info.System.Temperature}°C");
                Console.WriteLine($"CPU usage: {info.System.CpuUsage}%");
                
                // Capture image
                Console.WriteLine("Capturing image...");
                var imageData = await client.CaptureImageAsync(95);
                var imagePath = $"capture_{DateTime.Now:yyyyMMdd_HHmmss}.jpg";
                await File.WriteAllBytesAsync(imagePath, imageData);
                Console.WriteLine($"Image saved: {imagePath}");
                
                // Start recording
                Console.WriteLine("Starting recording...");
                var recording = await client.StartRecordingAsync(new RecordingOptions
                {
                    Filename = "test_recording.avi",
                    Duration = 60,
                    Quality = "high",
                    Resolution = "1920x1080"
                });
                Console.WriteLine($"Recording started: {recording.RecordingId}");
                
                // Monitor recording
                await MonitorRecording(client);
                
                // List and download files
                await ListAndDownloadFiles(client);
                
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
            finally
            {
                client.Dispose();
            }
            
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
        
        static async Task MonitorRecording(RotorDreamHttpClient client)
        {
            Console.WriteLine("Monitoring recording...");
            
            while (true)
            {
                var status = await client.GetRecordingStatusAsync();
                
                if (!status.Recording)
                {
                    Console.WriteLine("Recording completed");
                    break;
                }
                
                Console.WriteLine($"Recording: {status.Duration}s, Size: {status.EstimatedSize / 1024 / 1024}MB");
                await Task.Delay(5000);
            }
        }
        
        static async Task ListAndDownloadFiles(RotorDreamHttpClient client)
        {
            Console.WriteLine("Listing recordings...");
            
            var files = await client.ListFilesAsync("/media/data/recordings", filter: ".avi");
            Console.WriteLine($"Found {files.FileCount} video files:");
            
            foreach (var file in files.Files)
            {
                if (file.Type == "file")
                {
                    Console.WriteLine($"- {file.Name} ({file.Size / 1024 / 1024}MB)");
                    
                    // Download recent files
                    if (file.Modified > DateTime.Now.AddHours(-1))
                    {
                        var localPath = Path.Combine("downloads", file.Name);
                        Directory.CreateDirectory("downloads");
                        
                        await client.DownloadFileAsync($"recordings/{file.Name}", localPath);
                        Console.WriteLine($"Downloaded: {localPath}");
                    }
                }
            }
        }
    }
}
```

### WebSocket Example
```csharp
using System;
using System.Threading.Tasks;
using RotorDream.Client;

namespace RotorDream.WebSocketExample
{
    class WebSocketExample
    {
        static async Task Main(string[] args)
        {
            var wsClient = new RotorDreamWebSocketClient("ws://192.168.1.100:8080/ws", "1a2B3c4D5e6f7G8h");
            
            // Set up event handlers
            wsClient.OnConnected += () =>
            {
                Console.WriteLine("WebSocket connected");
                wsClient.Subscribe("state_changes");
                wsClient.Subscribe("camera_events");
                wsClient.GetState();
            };
            
            wsClient.OnDisconnected += (reason) =>
            {
                Console.WriteLine($"WebSocket disconnected: {reason}");
            };
            
            wsClient.OnError += (error) =>
            {
                Console.WriteLine($"WebSocket error: {error.Message}");
            };
            
            // Handle state updates
            wsClient.On("state_update", (data) =>
            {
                Console.WriteLine($"State update: {data.parameter} = {data.value}");
                
                if (data.parameter == "system.temperature" && (double)data.value > 70)
                {
                    Console.WriteLine("WARNING: High temperature!");
                }
            });
            
            // Handle camera events
            wsClient.On("camera_event", (data) =>
            {
                Console.WriteLine($"Camera event: {data.@event}");
            });
            
            // Connect
            if (await wsClient.ConnectAsync())
            {
                Console.WriteLine("Connected successfully");
                
                // Send some commands
                await Task.Delay(1000);
                wsClient.SetParameter("camera.resolution", "1920x1080");
                wsClient.SetParameter("camera.framerate", 30);
                
                // Keep alive
                Console.WriteLine("Press any key to disconnect...");
                Console.ReadKey();
            }
            else
            {
                Console.WriteLine("Failed to connect");
            }
            
            wsClient.Dispose();
        }
    }
}
```

## Windows Forms Application

### Main Form Implementation
```csharp
using System;
using System.Drawing;
using System.IO;
using System.Threading.Tasks;
using System.Windows.Forms;
using RotorDream.Client;

namespace RotorDream.WinForms
{
    public partial class MainForm : Form
    {
        private RotorDreamHttpClient _client;
        private RotorDreamWebSocketClient _wsClient;
        private Timer _statusTimer;
        private bool _recording = false;
        
        public MainForm()
        {
            InitializeComponent();
            SetupClient();
            SetupUI();
        }
        
        private void SetupClient()
        {
            _client = new RotorDreamHttpClient("http://192.168.1.100:8080", "1a2B3c4D5e6f7G8h");
            _wsClient = new RotorDreamWebSocketClient("ws://192.168.1.100:8080/ws", "1a2B3c4D5e6f7G8h");
            
            _wsClient.OnConnected += () =>
            {
                Invoke(new Action(() =>
                {
                    lblConnectionStatus.Text = "Connected";
                    lblConnectionStatus.ForeColor = Color.Green;
                }));
                
                _wsClient.Subscribe("state_changes");
                _wsClient.Subscribe("camera_events");
            };
            
            _wsClient.OnDisconnected += (reason) =>
            {
                Invoke(new Action(() =>
                {
                    lblConnectionStatus.Text = "Disconnected";
                    lblConnectionStatus.ForeColor = Color.Red;
                }));
            };
            
            _wsClient.On("state_update", (data) =>
            {
                Invoke(new Action(() => HandleStateUpdate(data)));
            });
        }
        
        private void SetupUI()
        {
            // Setup status timer
            _statusTimer = new Timer();
            _statusTimer.Interval = 5000; // 5 seconds
            _statusTimer.Tick += async (sender, e) => await UpdateStatus();
            _statusTimer.Start();
        }
        
        private async void btnConnect_Click(object sender, EventArgs e)
        {
            try
            {
                btnConnect.Enabled = false;
                lblStatus.Text = "Connecting...";
                
                // Test HTTP connection
                var health = await _client.GetHealthAsync();
                
                // Connect WebSocket
                if (await _wsClient.ConnectAsync())
                {
                    lblStatus.Text = "Connected successfully";
                    await UpdateStatus();
                    await LoadFilesList();
                }
                else
                {
                    lblStatus.Text = "WebSocket connection failed";
                }
            }
            catch (Exception ex)
            {
                lblStatus.Text = $"Connection failed: {ex.Message}";
            }
            finally
            {
                btnConnect.Enabled = true;
            }
        }
        
        private async void btnCapture_Click(object sender, EventArgs e)
        {
            try
            {
                btnCapture.Enabled = false;
                lblStatus.Text = "Capturing image...";
                
                var imageData = await _client.CaptureImageAsync(90);
                
                // Display in PictureBox
                using (var ms = new MemoryStream(imageData))
                {
                    picPreview.Image = Image.FromStream(ms);
                }
                
                // Save to file
                var filename = $"capture_{DateTime.Now:yyyyMMdd_HHmmss}.jpg";
                await File.WriteAllBytesAsync(filename, imageData);
                
                lblStatus.Text = $"Image captured: {filename}";
            }
            catch (Exception ex)
            {
                lblStatus.Text = $"Capture failed: {ex.Message}";
            }
            finally
            {
                btnCapture.Enabled = true;
            }
        }
        
        private async void btnStartRecording_Click(object sender, EventArgs e)
        {
            try
            {
                btnStartRecording.Enabled = false;
                
                var options = new RecordingOptions
                {
                    Filename = $"recording_{DateTime.Now:yyyyMMdd_HHmmss}.avi",
                    Quality = "high",
                    Resolution = "1920x1080"
                };
                
                var result = await _client.StartRecordingAsync(options);
                _recording = true;
                
                lblStatus.Text = $"Recording started: {result.Filename}";
                btnStopRecording.Enabled = true;
                
                // Start recording timer
                var recordingTimer = new Timer();
                recordingTimer.Interval = 1000;
                recordingTimer.Tick += async (sender, e) =>
                {
                    var status = await _client.GetRecordingStatusAsync();
                    if (!status.Recording)
                    {
                        recordingTimer.Stop();
                        _recording = false;
                        btnStartRecording.Enabled = true;
                        btnStopRecording.Enabled = false;
                        lblStatus.Text = "Recording completed";
                        await LoadFilesList();
                    }
                    else
                    {
                        lblRecordingStatus.Text = $"Recording: {status.Duration}s";
                    }
                };
                recordingTimer.Start();
            }
            catch (Exception ex)
            {
                lblStatus.Text = $"Recording start failed: {ex.Message}";
                btnStartRecording.Enabled = true;
            }
        }
        
        private async void btnStopRecording_Click(object sender, EventArgs e)
        {
            try
            {
                btnStopRecording.Enabled = false;
                
                var result = await _client.StopRecordingAsync();
                _recording = false;
                
                lblStatus.Text = $"Recording stopped: {result.Filename} ({result.Duration}s)";
                btnStartRecording.Enabled = true;
                lblRecordingStatus.Text = "";
                
                await LoadFilesList();
            }
            catch (Exception ex)
            {
                lblStatus.Text = $"Recording stop failed: {ex.Message}";
            }
        }
        
        private async Task UpdateStatus()
        {
            if (!_wsClient.IsConnected) return;
            
            try
            {
                var info = await _client.GetInfoAsync();
                
                lblVersion.Text = $"Version: {info.Version}";
                lblUptime.Text = $"Uptime: {TimeSpan.FromSeconds(info.Uptime):d\\:hh\\:mm\\:ss}";
                lblTemperature.Text = $"Temperature: {info.System.Temperature}°C";
                lblCPU.Text = $"CPU: {info.System.CpuUsage:F1}%";
                lblMemory.Text = $"Memory: {info.System.Memory.Used / 1024 / 1024}MB / {info.System.Memory.Total / 1024 / 1024}MB";
                
                var cameraStatus = await _client.GetCameraStatusAsync();
                var camera = cameraStatus.Cameras.Count > 0 ? cameraStatus.Cameras[0] : null;
                lblCamera.Text = camera?.Connected == true ? 
                    $"Camera: {camera.Resolution} @ {camera.Framerate}fps" : 
                    "Camera: Disconnected";
            }
            catch (Exception ex)
            {
                lblStatus.Text = $"Status update failed: {ex.Message}";
            }
        }
        
        private async Task LoadFilesList()
        {
            try
            {
                var files = await _client.ListFilesAsync("/media/data/recordings", filter: ".avi");
                
                listFiles.Items.Clear();
                foreach (var file in files.Files)
                {
                    if (file.Type == "file")
                    {
                        var item = new ListViewItem(file.Name);
                        item.SubItems.Add($"{file.Size / 1024 / 1024} MB");
                        item.SubItems.Add(file.Modified.ToString("yyyy-MM-dd HH:mm"));
                        item.Tag = file;
                        listFiles.Items.Add(item);
                    }
                }
            }
            catch (Exception ex)
            {
                lblStatus.Text = $"Failed to load files: {ex.Message}";
            }
        }
        
        private void HandleStateUpdate(dynamic data)
        {
            var parameter = (string)data.parameter;
            var value = data.value;
            
            switch (parameter)
            {
                case "system.temperature":
                    lblTemperature.Text = $"Temperature: {value}°C";
                    if ((double)value > 70)
                    {
                        lblTemperature.ForeColor = Color.Red;
                    }
                    else
                    {
                        lblTemperature.ForeColor = Color.Black;
                    }
                    break;
                    
                case "system.cpu_usage":
                    lblCPU.Text = $"CPU: {value:F1}%";
                    break;
                    
                case "camera.recording":
                    _recording = (bool)value;
                    btnStartRecording.Enabled = !_recording;
                    btnStopRecording.Enabled = _recording;
                    break;
            }
        }
        
        private async void listFiles_DoubleClick(object sender, EventArgs e)
        {
            if (listFiles.SelectedItems.Count > 0)
            {
                var file = (FileInfo)listFiles.SelectedItems[0].Tag;
                
                using (var saveDialog = new SaveFileDialog())
                {
                    saveDialog.FileName = file.Name;
                    saveDialog.Filter = "Video files (*.avi)|*.avi|All files (*.*)|*.*";
                    
                    if (saveDialog.ShowDialog() == DialogResult.OK)
                    {
                        try
                        {
                            lblStatus.Text = $"Downloading {file.Name}...";
                            await _client.DownloadFileAsync($"recordings/{file.Name}", saveDialog.FileName);
                            lblStatus.Text = $"Downloaded: {saveDialog.FileName}";
                        }
                        catch (Exception ex)
                        {
                            lblStatus.Text = $"Download failed: {ex.Message}";
                        }
                    }
                }
            }
        }
        
        protected override void OnFormClosed(FormClosedEventArgs e)
        {
            _statusTimer?.Stop();
            _wsClient?.Dispose();
            _client?.Dispose();
            base.OnFormClosed(e);
        }
    }
}
```

## RTSP Video Integration with OpenCV

### RTSP Video Player
```csharp
using System;
using System.Drawing;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using OpenCvSharp;
using OpenCvSharp.Extensions;

namespace RotorDream.Video
{
    public class RTSPVideoPlayer : UserControl
    {
        private VideoCapture _capture;
        private Thread _captureThread;
        private bool _isCapturing;
        private PictureBox _pictureBox;
        private string _rtspUrl;
        
        public event EventHandler<Mat> FrameReceived;
        public event EventHandler<Exception> ErrorOccurred;
        
        public bool IsPlaying => _isCapturing;
        public string RTSPUrl => _rtspUrl;
        
        public RTSPVideoPlayer()
        {
            InitializeComponent();
        }
        
        private void InitializeComponent()
        {
            _pictureBox = new PictureBox
            {
                Dock = DockStyle.Fill,
                SizeMode = PictureBoxSizeMode.Zoom,
                BackColor = Color.Black
            };
            
            Controls.Add(_pictureBox);
        }
        
        public async Task<bool> StartAsync(string rtspUrl)
        {
            return await Task.Run(() => Start(rtspUrl));
        }
        
        public bool Start(string rtspUrl)
        {
            try
            {
                Stop();
                
                _rtspUrl = rtspUrl;
                _capture = new VideoCapture(rtspUrl);
                
                if (!_capture.IsOpened())
                {
                    throw new Exception("Failed to open RTSP stream");
                }
                
                // Configure capture
                _capture.Set(VideoCaptureProperties.BufferSize, 1);
                _capture.Set(VideoCaptureProperties.Fps, 30);
                
                _isCapturing = true;
                _captureThread = new Thread(CaptureLoop)
                {
                    IsBackground = true,
                    Name = "RTSP Capture Thread"
                };
                _captureThread.Start();
                
                return true;
            }
            catch (Exception ex)
            {
                ErrorOccurred?.Invoke(this, ex);
                return false;
            }
        }
        
        public void Stop()
        {
            _isCapturing = false;
            
            if (_captureThread != null && _captureThread.IsAlive)
            {
                _captureThread.Join(5000);
            }
            
            _capture?.Release();
            _capture?.Dispose();
            _capture = null;
            
            if (InvokeRequired)
            {
                Invoke(new Action(() => _pictureBox.Image = null));
            }
            else
            {
                _pictureBox.Image = null;
            }
        }
        
        private void CaptureLoop()
        {
            var frame = new Mat();
            
            while (_isCapturing)
            {
                try
                {
                    if (_capture.Read(frame) && !frame.Empty())
                    {
                        // Raise frame received event
                        FrameReceived?.Invoke(this, frame.Clone());
                        
                        // Update display
                        if (InvokeRequired)
                        {
                            Invoke(new Action(() => UpdateDisplay(frame)));
                        }
                        else
                        {
                            UpdateDisplay(frame);
                        }
                    }
                    else
                    {
                        Thread.Sleep(33); // ~30fps
                    }
                }
                catch (Exception ex)
                {
                    ErrorOccurred?.Invoke(this, ex);
                    Thread.Sleep(1000); // Wait before retry
                }
            }
        }
        
        private void UpdateDisplay(Mat frame)
        {
            try
            {
                if (_pictureBox.Image != null)
                {
                    _pictureBox.Image.Dispose();
                }
                
                _pictureBox.Image = BitmapConverter.ToBitmap(frame);
            }
            catch (Exception ex)
            {
                ErrorOccurred?.Invoke(this, ex);
            }
        }
        
        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                Stop();
                _pictureBox?.Dispose();
            }
            base.Dispose(disposing);
        }
    }
    
    // Usage in form
    public partial class VideoForm : Form
    {
        private RTSPVideoPlayer _videoPlayer;
        
        public VideoForm()
        {
            InitializeComponent();
            
            _videoPlayer = new RTSPVideoPlayer
            {
                Dock = DockStyle.Fill
            };
            
            _videoPlayer.FrameReceived += (sender, frame) =>
            {
                // Process frame (e.g., motion detection, analysis)
                ProcessFrame(frame);
            };
            
            _videoPlayer.ErrorOccurred += (sender, ex) =>
            {
                MessageBox.Show($"Video error: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            };
            
            panelVideo.Controls.Add(_videoPlayer);
        }
        
        private async void btnPlay_Click(object sender, EventArgs e)
        {
            var rtspUrl = "rtsp://admin:password@192.168.1.100:554/stream0";
            
            if (await _videoPlayer.StartAsync(rtspUrl))
            {
                btnPlay.Enabled = false;
                btnStop.Enabled = true;
                lblStatus.Text = "Playing";
            }
            else
            {
                MessageBox.Show("Failed to start video stream", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
        
        private void btnStop_Click(object sender, EventArgs e)
        {
            _videoPlayer.Stop();
            btnPlay.Enabled = true;
            btnStop.Enabled = false;
            lblStatus.Text = "Stopped";
        }
        
        private void ProcessFrame(Mat frame)
        {
            // Example: Basic motion detection
            // Convert to grayscale, apply Gaussian blur, etc.
            // This runs in background thread, be careful with UI updates
        }
        
        protected override void OnFormClosed(FormClosedEventArgs e)
        {
            _videoPlayer?.Dispose();
            base.OnFormClosed(e);
        }
    }
}
```

## Related Documentation

- [Python Client](python-client.md) - Python integration examples
- [JavaScript Client](javascript-client.md) - Web and Node.js integration
- [HTTP API](../http-api.md) - Complete REST API reference
- [WebSocket API](../websocket-api.md) - Real-time communication protocol

---

*C# examples tested with .NET Framework 4.8+ and .NET 6+. Requires NuGet packages: Newtonsoft.Json, WebSocketSharp, OpenCvSharp4*
