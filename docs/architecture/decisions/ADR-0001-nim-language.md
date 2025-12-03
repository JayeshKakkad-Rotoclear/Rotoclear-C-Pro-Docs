# ADR-0001: Nim Programming Language Selection

**Status**: Accepted  
**Date**: 2024-01-15  
**Deciders**: Engineering Team  

## Context

We needed to select a programming language for the C Pro embedded camera server that would provide:

- Low-level hardware access (V4L2, GPIO, I2C)
- High performance for real-time video processing
- Memory safety and reliability for medical devices
- Cross-compilation for ARM64 embedded targets
- Small binary size for resource-constrained devices

## Decision

We chose **Nim** as the primary programming language for the C Pro camera server.

## Rationale

### Performance Benefits
- **Compiled to C**: Nim compiles to optimized C code, providing near-C performance
- **Zero-cost Abstractions**: High-level constructs with no runtime overhead
- **Manual Memory Management**: Precise control over memory allocation with ORC GC
- **Small Binaries**: Typical binary size <10MB for complete application

### Cross-compilation Support
```bash
# Cross-compile for ARM64 from x86
nim c --cpu:arm64 --os:linux -d:release rotordream.nim
```

### Hardware Integration
- **C Interop**: Seamless integration with existing C libraries (GStreamer, V4L2)
- **Low-level Access**: Direct memory manipulation and hardware control
- **No Runtime**: Minimal runtime dependencies for embedded deployment

### Development Experience
- **Type Safety**: Strong static typing with inference
- **Metaprogramming**: Powerful macro system for code generation
- **Modern Syntax**: Python-like readability with C-like performance

## Code Example

```nim
# Clean integration with C libraries
proc v4l2_open(device: cstring, flags: cint): cint {.importc, header: "<fcntl.h>".}

# Type-safe, high-performance video processing
proc processFrame(buffer: ptr UncheckedArray[byte], size: int): seq[byte] =
  result = newSeq[byte](size)
  copyMem(result[0].addr, buffer, size)
```

## Alternatives Considered

### C/C++
- **Pros**: Maximum performance, hardware access
- **Cons**: Memory safety issues, complex build system, slower development

### Rust
- **Pros**: Memory safety, performance, growing embedded ecosystem
- **Cons**: Steep learning curve, larger binaries, limited ARM64 ecosystem (2024)

### Go
- **Pros**: Simple syntax, good networking support
- **Cons**: Garbage collector unsuitable for real-time, larger binaries

### Python/Node.js
- **Pros**: Rapid development, extensive libraries
- **Cons**: Performance limitations, runtime dependencies

## Consequences

### Positive
- **Performance**: Real-time video processing at 30fps+
- **Reliability**: Type safety reduces runtime errors
- **Deployment**: Single binary deployment, no runtime dependencies
- **Integration**: Seamless C library integration for hardware access

### Negative
- **Learning Curve**: Team had to learn Nim language and ecosystem
- **Ecosystem**: Smaller package ecosystem compared to mainstream languages
- **Debugging**: Limited tooling compared to C/C++/Python

### Neutral
- **Build System**: Nim's build system works well but required configuration tuning
- **Documentation**: Good core documentation, but community packages vary

## Implementation Notes

### Build Configuration
From `rotordream.nimble`:
```nim
requires "nim >= 2.2.2"
requires "corun >= 0.7.10"
requires "xxtea"
requires "checksums >= 0.2.1"
```

### Cross-compilation Setup
From `tools/buildRelease.nim`:
```nim
when defined(embeddedSystem):
  switch("cpu", "arm64")
  switch("os", "linux")
  switch("define", "directCompile=true")
```

## Monitoring

We track the following metrics to validate this decision:
- **Binary Size**: Target <10MB for release builds
- **Memory Usage**: <100MB RAM for typical operation
- **Performance**: 30fps video processing on ARM64 hardware
- **Development Velocity**: Feature delivery time vs. C++ baseline

## Review Date

This decision will be reviewed in Q4 2025 based on:
- Team productivity and satisfaction
- Performance benchmarks vs. requirements
- Nim ecosystem maturity and support
- Availability of alternative technologies
