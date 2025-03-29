# MPM (Microcontroller Package Manager)

## Overview
MPM is an open-source package manager designed for microcontroller platforms. It simplifies the process of managing libraries, dependencies, and builds for various microcontroller platforms. MPM is inspired by tools like `npm` for JavaScript but tailored specifically for microcontroller development.

---

## Features

1. **Platform Initialization**
   - Initialize projects for specific microcontroller platforms.
   - Example: `mpm init esp32`
   - Default platform: GCC (for generic C/C++ compilation).

2. **Library Installation**
   - Install libraries by name.
   - Example: `mpm install dht11`
   - Automatically fetches library details from the centralized registry.

3. **Build and Deployment**
   - Build the project using platform-specific or generic GCC tools.
   - Deploy binaries to target devices.
   - Example: `mpm build` and `mpm deploy`.

4. **Simulations**
   - Simulate memory and compute usage.
   - Simulate sensor and I/O device behavior.

5. **Makefile Support**
   - Generate Makefiles for custom build processes.

6. **Platform-Agnostic**
   - Supports all controllers by setting the platform during initialization.
   - Without specifying a platform, defaults to GCC.

7. **Registry-Free Architecture**
   - No local registry is maintained.
   - Libraries are managed directly via the `registry.json` hosted on GitHub.

---

## Workflow

1. **Initialize a New Project**
   ```bash
   mpm init esp32
   ```
   This sets the platform for the project. The default platform is GCC.

2. **Install a Library**
   ```bash
   mpm install dht11
   ```
   This fetches the library details from the remote `registry.json` and integrates it into your project.

3. **Build the Project**
   ```bash
   mpm build
   ```
   Generates platform-specific binaries.

4. **Deploy the Project**
   ```bash
   mpm deploy
   ```
   Deploys the generated binaries to the target microcontroller.

---

## File Structure

```
my_project/
├── dev/               # Development files (source code and headers)
│   ├── src/           # Source code files
│   └── include/       # Header files
├── lib/               # Libraries downloaded via mpm install
├── platform.json      # Project configuration file
├── Makefile           # (Optional) Custom build process
└── build/             # Compiled binaries
```

### `platform.json` Example
```json
{
  "name": "my_project",
  "platform": "esp32",
  "dependencies": {
    "dht11": "2.1.0"
  }
}
```

---

## Contributing

### Submitting a New Library
1. Open an issue in the `mpm` repository.
2. Use the provided issue template to submit your library details:
   - **Library Name**
   - **Version**
   - **Repository URL**
   - **Description**
   - **Supported Platforms**
3. The `registry.json` will be updated upon approval of the issue.

---

## GitHub Repository Structure

### Main Repository (`mpm`)
Houses the core MPM source code and CLI tools.

### Registry Repository (`mpm-registry`)
Contains the `registry.json` file:
```json
{
  "libraries": {
    "dht11": {
      "name": "dht11 Driver",
      "version": "1.0.0",
      "platforms": ["esp32", "arduino"],
      "source": "https://github.com/sparkfun/SparkFun_MPU-6050_Arduino_Library.git",
      "description": "A driver for the dht11 sensor."
    },
    "dht11": {
      "name": "DHT11 Sensor Library",
      "version": "2.1.0",
      "platforms": ["arduino"],
      "source": "https://github.com/adafruit/DHT-sensor-library.git",
      "description": "A library for the DHT11 temperature and humidity sensor."
    }
  }
}
```

---

## Future Plans

1. **GUI-Based Tools**
   - Add a desktop application for visualizing dependencies, managing builds, and deploying firmware.

2. **Enhanced Simulations**
   - Advanced simulators for testing peripherals and performance under various conditions.

3. **Community Contributions**
   - Expand the library registry with contributions from the community.

4. **Integration with CI/CD**
   - Streamline deployment pipelines for microcontroller projects.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

