# Glossary

**Technical terms and acronyms used in the Rotoclear Camera Server documentation.**

## Project-Specific Terms

**Rotoclear C Pro:** Industrial imaging device with rotating disc mechanism for enhanced image quality.

**Camera Head:** Physical camera module that can be attached to the Rotoclear system. Supports multiple sensors.

**Disc Rotation:** Mechanical rotation of the imaging disc at configurable RPM for image enhancement.

**Factory Configuration:** JSON-based configuration file that defines core system behavior and hardware settings.

**License Configuration:** Feature licensing system that enables/disables specific capabilities based on deployment variant.

**Observable State:** Reactive state management pattern where state changes trigger notifications to subscribers.

**Version Flavor:** Deployment variant identifier (DEV, DEMO, EDU, VB, DMG) that determines configuration and features.

## Technical Acronyms

**API:** Application Programming Interface - standardized interface for software communication.

**ARM64:** 64-bit ARM processor architecture used in embedded Rotoclear devices.

**AVI:** Audio Video Interleave - video file format used for recordings.

**C4:** Context, Container, Component, Class - architectural documentation framework.

**DMG:** Specific deployment variant/configuration of the Rotoclear system.

**EDU:** Educational deployment variant with specific feature set for educational institutions.

**FPGA:** Field-Programmable Gate Array - reconfigurable hardware component.

**GStreamer:** Multimedia framework for handling video/audio streams and processing.

**HTTP/HTTPS:** HyperText Transfer Protocol (Secure) - web communication protocols.

**JPEG:** Joint Photographic Experts Group - compressed image format.

**JSON:** JavaScript Object Notation - human-readable data interchange format.

**ONVIF:** Open Network Video Interface Forum - standardized protocol for IP cameras.

**ORC:** Nim's reference counting garbage collector optimized for real-time systems.

**PIP:** Picture-in-Picture - display mode showing multiple camera feeds simultaneously.

**RPM:** Revolutions Per Minute - measurement unit for disc rotation speed.

**RTSP:** Real Time Streaming Protocol - network protocol for media streaming.

**SSH:** Secure Shell - encrypted network protocol for remote device access.

**SSL/TLS:** Secure Sockets Layer/Transport Layer Security - encryption protocols for secure communication.

**V4L2:** Video4Linux version 2 - Linux kernel interface for video capture devices.

**WebRTC:** Web Real-Time Communication - browser-based real-time video/audio communication.

**WebSocket:** Full-duplex communication protocol over TCP for real-time web applications.

## Development Terms

**ADR:** Architecture Decision Record - document capturing important architectural decisions.

**CI/CD:** Continuous Integration/Continuous Deployment - automated build and deployment processes.

**Cross-compilation:** Building software for a different target platform than the development platform.

**DoD:** Definition of Done - criteria that must be met for work to be considered complete.

**DoR:** Definition of Ready - criteria that must be met before work can begin.

**Embedded System:** Computer system with dedicated function within larger mechanical/electrical system.

**Hot Reload:** Development feature allowing code changes without full application restart.

**Mock:** Simulated object/service used for testing instead of real dependencies.

**ORM:** Object-Relational Mapping - technique for database interaction using object-oriented paradigms.

**SDK:** Software Development Kit - collection of tools for developing applications.

**SLA:** Service Level Agreement - commitment between service provider and client.

**Unit Test:** Automated test verifying individual software components in isolation.

**WIP:** Work In Progress - tasks currently being worked on but not yet complete.

## Network and Protocol Terms

**Basic Auth:** Simple HTTP authentication scheme using username and password.

**DHCP:** Dynamic Host Configuration Protocol - automatic IP address assignment.

**DNS:** Domain Name System - hierarchical naming system for network resources.

**Gateway:** Network device connecting different networks (e.g., local network to internet).

**IP Address:** Internet Protocol address - unique identifier for network devices.

**MAC Address:** Media Access Control address - unique hardware identifier for network interfaces.

**Netmask:** Network mask defining which portion of IP address represents network vs. host.

**Port:** Communication endpoint for network services (e.g., port 80 for HTTP).

**SMB/CIFS:** Server Message Block/Common Internet File System - network file sharing protocol.

**TCP/UDP:** Transmission Control Protocol/User Datagram Protocol - core internet protocols.

**URL/URI:** Uniform Resource Locator/Identifier - web address format.

## Camera and Media Terms

**Codec:** Compression/decompression algorithm for video/audio data.

**Exposure:** Amount of light reaching camera sensor, affecting image brightness.

**FPS:** Frames Per Second - video frame rate measurement.

**Gain:** Camera sensor amplification, similar to ISO in photography.

**Pipeline:** Series of connected processing stages for media data (GStreamer concept).

**Resolution:** Image dimensions in pixels (width × height).

**Sensor:** Light-sensitive electronic component that captures images.

**Timestamp:** Date/time information embedded in images or videos.

**White Balance:** Color correction adjusting for different lighting conditions.

## System Administration Terms

**Daemon:** Background service running continuously on Unix-like systems.

**Log Rotation:** Automatic management of log files to prevent disk space issues.

**Process ID (PID):** Unique identifier for running system processes.

**Service:** System background process managed by service manager (systemd).

**Syslog:** Standard logging system for Unix-like operating systems.

**Systemctl:** Command-line utility for controlling systemd services.

**Uptime:** Time duration system has been running since last boot.

## Build and Deployment Terms

**Artifact:** File or package produced by build process (e.g., compiled binary).

**Build Cache:** Stored intermediate build results to speed up subsequent builds.

**Cross-platform:** Software designed to work on multiple operating systems or architectures.

**Link-time Optimization (LTO):** Compiler optimization performed during linking phase.

**Makefile:** Build automation script defining compilation rules and dependencies.

**Package Manager:** Tool for installing, updating, and managing software packages.

**Release Build:** Optimized build configuration for production deployment.

**Staging Environment:** Pre-production environment for testing before live deployment.

**Target Platform:** Specific hardware/software environment where application will run.

## Security Terms

**API Token:** Authentication credential for programmatic API access.

**Certificate:** Digital document verifying identity for secure communications.

**Encryption:** Process of encoding data to prevent unauthorized access.

**Firewall:** Network security system controlling incoming/outgoing traffic.

**Hash:** Fixed-size string produced by cryptographic hash function.

**Permissions:** Access control mechanism defining what actions users/processes can perform.

**Private Key:** Secret cryptographic key used for decryption and digital signing.

**Public Key:** Publicly shareable cryptographic key used for encryption and verification.

**Salt:** Random data added to passwords before hashing for security.

**Two-Factor Authentication (2FA):** Security method requiring two different authentication factors.

## Quality Assurance Terms

**Acceptance Test:** Testing to verify system meets business requirements.

**Assertion:** Statement in test code verifying expected behavior or outcome.

**Code Coverage:** Measurement of how much code is executed during testing.

**Integration Test:** Testing interaction between different system components.

**Load Test:** Testing system behavior under expected operational conditions.

**Regression Test:** Testing to ensure new changes don't break existing functionality.

**Smoke Test:** Basic testing to verify fundamental functionality works.

**Stress Test:** Testing system behavior under extreme or peak load conditions.

**Test Fixture:** Fixed state used as baseline for running tests.

**Test Suite:** Collection of test cases designed to test software program.

---
