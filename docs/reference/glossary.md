# Glossary

**Comprehensive glossary of terms, acronyms, and technical definitions used in the C Pro camera system documentation and implementation.**

## A

**API (Application Programming Interface)**  
A set of protocols, routines, and tools for building software applications. C Pro provides REST APIs, WebSocket APIs, and ONVIF APIs for system integration.

**AES (Advanced Encryption Standard)**  
A symmetric encryption algorithm used to secure data transmission and storage in the C Pro system.

**Authentication**  
The process of verifying the identity of a user or system component before granting access to resources.

**Authorization**  
The process of determining what resources a user or system component is allowed to access after authentication.

**Asyncio**  
An asynchronous programming framework that allows concurrent execution of tasks without blocking the main thread.

## B

**Bitrate**  
The amount of data processed per unit of time in video streaming, typically measured in bits per second (bps).

**Buffer**  
A temporary storage area used to hold data while it's being transferred between different parts of the system.

**Bandwidth**  
The maximum rate of data transfer across a network connection, typically measured in bits per second (bps).

## C

**Codec**  
A software component that encodes and decodes digital video and audio data. Common codecs include H.264, H.265, and MJPEG.

**Concurrency**  
The ability to handle multiple operations simultaneously without blocking other operations.

**Configuration Management**  
The process of systematically handling changes to system configuration to maintain integrity over time.

**Container**  
A lightweight, standalone package that includes everything needed to run an application: code, runtime, system tools, libraries, and settings.

**CRUD (Create, Read, Update, Delete)**  
The four basic operations that can be performed on data storage systems.

## D

**Database**  
A structured collection of data stored electronically in a computer system, used by C Pro to store configuration, user data, and recording metadata.

**Docker**  
A containerization platform that packages applications and their dependencies into portable containers.

**DNS (Domain Name System)**  
A hierarchical system that translates human-readable domain names into IP addresses.

**DRM (Digital Rights Management)**  
Technologies used to control access to copyrighted digital content.

## E

**Encryption**  
The process of converting data into a coded format to prevent unauthorized access.

**Endpoint**  
A specific URL where an API can be accessed by a client application.

**Event-Driven Architecture**  
A software architecture pattern where components communicate through events rather than direct method calls.

**Edge Computing**  
Computing that occurs at or near the physical location where data is collected and analyzed.

## F

**FFmpeg**  
A comprehensive multimedia framework capable of decoding, encoding, transcoding, muxing, demuxing, streaming, filtering and playing video and audio content.

**Frame Rate (FPS - Frames Per Second)**  
The frequency at which consecutive images (frames) are captured or displayed in video content.

**Firewall**  
A network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules.

## G

**GStreamer**  
An open-source multimedia framework that allows construction of graphs of media-handling components, used extensively in C Pro for video processing.

**GPU (Graphics Processing Unit)**  
A specialized processor designed to accelerate graphics rendering and parallel processing tasks.

**GUID (Globally Unique Identifier)**  
A 128-bit number used to identify information in computer systems, ensuring uniqueness across all systems.

## H

**H.264 (Advanced Video Coding)**  
A video compression standard that provides high-quality video at lower bitrates than previous standards.

**H.265 (High Efficiency Video Coding)**  
A video compression standard that offers improved compression efficiency over H.264.

**HTTP (Hypertext Transfer Protocol)**  
The foundation of data communication on the World Wide Web, used for C Pro's REST API.

**HTTPS (HTTP Secure)**  
An extension of HTTP that uses encryption to secure communication between client and server.

**Health Check**  
A mechanism to verify that a service or component is running correctly and responding to requests.

## I

**IP (Internet Protocol)**  
A set of rules governing the format of data sent via the internet or local network.

**IP Camera**  
A digital video camera that can send and receive data via a computer network and the internet.

**IoT (Internet of Things)**  
A network of physical devices embedded with sensors, software, and connectivity to exchange data.

**ISO (International Organization for Standardization)**  
An international standard-setting body that develops and publishes technical standards.

## J

**JSON (JavaScript Object Notation)**  
A lightweight data-interchange format that is easy for humans to read and write.

**JWT (JSON Web Token)**  
A compact, URL-safe means of representing claims to be transferred between two parties, used for authentication in C Pro.

**JPEG (Joint Photographic Experts Group)**  
A lossy compression method for digital images, commonly used for snapshot images.

## K

**Kernel**  
The core component of an operating system that manages system resources and hardware communication.

**Kubernetes**  
An open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.

**Key Frame (I-Frame)**  
A complete image frame in video compression that can be decoded independently without reference to other frames.

## L

**LDAP (Lightweight Directory Access Protocol)**  
An application protocol for accessing and maintaining distributed directory information services.

**Load Balancing**  
The process of distributing incoming network traffic across multiple servers to ensure no single server becomes overwhelmed.

**Logging**  
The practice of recording events, errors, and system activities for monitoring, debugging, and auditing purposes.

**Latency**  
The time delay between a request and response in a system, critical for real-time video streaming.

## M

**Microservice**  
An architectural approach where applications are built as a collection of small, independent services.

**MJPEG (Motion JPEG)**  
A video compression format where each frame is compressed separately as a JPEG image.

**Monitoring**  
The practice of continuously observing system performance, health, and behavior.

**MQTT (Message Queuing Telemetry Transport)**  
A lightweight messaging protocol designed for small sensors and mobile devices optimized for high-latency networks.

## N

**NAT (Network Address Translation)**  
A method of remapping IP address space by modifying network address information in packet headers.

**Nim**  
A systems programming language that combines successful concepts from mature languages like Python, Ada and Modula, used to implement C Pro.

**NTP (Network Time Protocol)**  
A networking protocol for clock synchronization between computer systems over packet-switched networks.

**NVR (Network Video Recorder)**  
A computer system that records video in a digital format to a disk drive, USB flash drive, SD memory card or other mass storage device.

## O

**OAuth**  
An open standard for access delegation, commonly used for token-based authentication and authorization.

**ONVIF (Open Network Video Interface Forum)**  
A global standard for IP-based physical security products, ensuring interoperability between different manufacturers.

**ORM (Object-Relational Mapping)**  
A programming technique for converting data between incompatible type systems using object-oriented programming languages.

**Observable Pattern**  
A software design pattern where an object maintains a list of dependents and notifies them of state changes.

## P

**P-Frame (Predicted Frame)**  
A video frame that contains only the changes from the previous frame, reducing data size.

**Payload**  
The actual data transmitted in a network packet, excluding headers and metadata.

**Pipeline**  
A series of data processing elements connected in series, where the output of one element is the input of the next.

**PTZ (Pan-Tilt-Zoom)**  
Camera functionality that allows remote control of the camera's orientation and zoom level.

**Prometheus**  
An open-source monitoring system with a dimensional data model and flexible query language.

## Q

**Quality of Service (QoS)**  
A set of technologies that work on a network to guarantee its ability to dependably run high-priority applications and traffic.

**Query**  
A request for information from a database or system, typically using a structured query language.

**Queue**  
A data structure that follows the first-in, first-out (FIFO) principle for managing tasks or messages.

## R

**REST (Representational State Transfer)**  
An architectural style for designing networked applications, used extensively in C Pro's API design.

**RTSP (Real Time Streaming Protocol)**  
A network control protocol designed for use in entertainment and communications systems to control streaming media servers.

**RTP (Real-time Transport Protocol)**  
A network protocol for delivering audio and video over IP networks.

**Resolution**  
The number of pixels in each dimension that can be displayed in a video image (e.g., 1920x1080).

**Redis**  
An in-memory data structure store used as a database, cache, and message broker.

## S

**SAML (Security Assertion Markup Language)**  
An open standard for exchanging authentication and authorization data between parties.

**SDK (Software Development Kit)**  
A collection of software development tools for creating applications for a specific platform.

**SSL/TLS (Secure Sockets Layer/Transport Layer Security)**  
Cryptographic protocols designed to provide communications security over a computer network.

**SOAP (Simple Object Access Protocol)**  
A messaging protocol specification for exchanging structured information using XML, used in ONVIF implementations.

**Streaming**  
The continuous transmission of audio or video files from a server to a client.

## T

**TCP (Transmission Control Protocol)**  
A connection-oriented protocol that provides reliable, ordered, and error-checked delivery of data.

**Thread**  
A separate flow of execution within a program, allowing concurrent operations.

**Thumbnail**  
A reduced-size version of an image or video frame used for quick preview purposes.

**Token**  
A piece of data that represents the right to access a resource or perform an operation.

**Transcoding**  
The process of converting video or audio from one format to another.

## U

**UDP (User Datagram Protocol)**  
A connectionless protocol that allows data to be sent without establishing a connection.

**URI (Uniform Resource Identifier)**  
A string of characters that unambiguously identifies a particular resource.

**URL (Uniform Resource Locator)**  
A reference to a web resource that specifies its location on a computer network.

**UUID (Universally Unique Identifier)**  
A 128-bit number used to identify information in computer systems.

**UPnP (Universal Plug and Play)**  
A set of networking protocols that allows devices to discover each other and establish functional network services.

## V

**V4L2 (Video4Linux2)**  
A Linux kernel framework that provides APIs for video capture and output devices.

**VMS (Video Management System)**  
Software that provides a centralized platform for managing multiple video feeds and recording devices.

**VPN (Virtual Private Network)**  
A secure connection between two or more devices over the internet that creates a private network.

**Validation**  
The process of checking that a system meets specified requirements and functions correctly.

**Video Analytics**  
The technology of analyzing video content to detect and determine temporal and spatial events.

## W

**Webhook**  
A user-defined HTTP callback that is triggered by specific events in a system.

**WebSocket**  
A communication protocol that provides full-duplex communication channels over a single TCP connection.

**WSDL (Web Services Description Language)**  
An XML-based interface description language used for describing web services.

**WS-Discovery**  
A protocol that defines a multicast discovery protocol to locate services on a local network.

## X

**XML (eXtensible Markup Language)**  
A markup language that defines rules for encoding documents in a format that is both human-readable and machine-readable.

**XSS (Cross-Site Scripting)**  
A type of security vulnerability typically found in web applications.

## Y

**YAML (YAML Ain't Markup Language)**  
A human-readable data serialization standard commonly used for configuration files.

## Z

**Zone**  
A defined area within a camera's field of view that can be configured for specific monitoring or analysis rules.

**Zoom**  
The ability to magnify a portion of the video image, either optically (optical zoom) or digitally (digital zoom).

---

## Technical Acronyms Reference

| Acronym | Full Form | Context |
|---------|-----------|---------|
| ADR | Architecture Decision Record | Documentation |
| AES | Advanced Encryption Standard | Security |
| API | Application Programming Interface | Integration |
| ASCII | American Standard Code for Information Interchange | Encoding |
| CRUD | Create, Read, Update, Delete | Database Operations |
| DNS | Domain Name System | Networking |
| FPS | Frames Per Second | Video |
| GPU | Graphics Processing Unit | Hardware |
| GUID | Globally Unique Identifier | Data |
| HTML | HyperText Markup Language | Web |
| HTTP | HyperText Transfer Protocol | Web |
| HTTPS | HTTP Secure | Security |
| IP | Internet Protocol | Networking |
| JSON | JavaScript Object Notation | Data Format |
| JWT | JSON Web Token | Authentication |
| LDAP | Lightweight Directory Access Protocol | Authentication |
| MJPEG | Motion JPEG | Video Compression |
| MQTT | Message Queuing Telemetry Transport | Messaging |
| NAT | Network Address Translation | Networking |
| NTP | Network Time Protocol | Time Synchronization |
| NVR | Network Video Recorder | Video Storage |
| ONVIF | Open Network Video Interface Forum | Standard |
| ORM | Object-Relational Mapping | Database |
| PTZ | Pan-Tilt-Zoom | Camera Control |
| QoS | Quality of Service | Networking |
| REST | Representational State Transfer | API Architecture |
| RGB | Red, Green, Blue | Color Model |
| RTSP | Real Time Streaming Protocol | Streaming |
| RTP | Real-time Transport Protocol | Streaming |
| SAML | Security Assertion Markup Language | Authentication |
| SDK | Software Development Kit | Development |
| SOAP | Simple Object Access Protocol | Web Services |
| SQL | Structured Query Language | Database |
| SSL | Secure Sockets Layer | Security |
| TCP | Transmission Control Protocol | Networking |
| TLS | Transport Layer Security | Security |
| UDP | User Datagram Protocol | Networking |
| UI | User Interface | Interface |
| UPnP | Universal Plug and Play | Networking |
| URI | Uniform Resource Identifier | Web |
| URL | Uniform Resource Locator | Web |
| UUID | Universally Unique Identifier | Data |
| V4L2 | Video4Linux2 | Linux Video API |
| VMS | Video Management System | Video Management |
| VPN | Virtual Private Network | Security |
| WSDL | Web Services Description Language | Web Services |
| XML | eXtensible Markup Language | Data Format |
| XSS | Cross-Site Scripting | Security Vulnerability |
| YAML | YAML Ain't Markup Language | Configuration |

---

## Units and Measurements

| Unit | Description | Common Values |
|------|-------------|---------------|
| bps | Bits per second | 1 Kbps = 1,000 bps |
| Bps | Bytes per second | 1 KBps = 1,024 bytes/sec |
| fps | Frames per second | 15, 25, 30, 60 fps |
| Hz | Hertz (frequency) | 50 Hz, 60 Hz |
| KB | Kilobyte | 1 KB = 1,024 bytes |
| MB | Megabyte | 1 MB = 1,024 KB |
| GB | Gigabyte | 1 GB = 1,024 MB |
| TB | Terabyte | 1 TB = 1,024 GB |
| ms | Millisecond | 1/1,000 second |
| μs | Microsecond | 1/1,000,000 second |
| px | Pixel | Picture element |
| dB | Decibel | Audio/signal level |
| °C | Degrees Celsius | Temperature |
| V | Volt | Electrical potential |
| A | Ampere | Electrical current |
| W | Watt | Power consumption |

---

## Status Codes Reference

### HTTP Status Codes
| Code | Meaning | Usage in C Pro |
|------|---------|-------------------|
| 200 | OK | Successful request |
| 201 | Created | Resource created successfully |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

### RTSP Status Codes
| Code | Meaning | Usage |
|------|---------|--------|
| 200 | OK | Request successful |
| 400 | Bad Request | Malformed request |
| 401 | Unauthorized | Authentication required |
| 404 | Not Found | Stream not found |
| 451 | Parameter Not Understood | Invalid parameter |
| 453 | Not Enough Bandwidth | Insufficient bandwidth |
| 461 | Unsupported Transport | Transport not supported |

### Camera Status Codes
| Status | Description | Actions Available |
|--------|-------------|------------------|
| `disconnected` | Camera not connected | Connect, Configure |
| `ready` | Camera ready for operation | Start, Configure |
| `streaming` | Camera actively streaming | Stop, Snapshot, Record |
| `recording` | Camera recording video | Stop Recording |
| `error` | Camera in error state | Reset, Diagnose |
| `maintenance` | Camera in maintenance mode | Exit Maintenance |

---

*Comprehensive glossary providing definitions and context for all technical terms used in the C Pro system*
