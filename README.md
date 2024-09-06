# Automatic Door System using ESP32-CAM, NestJS, and OpenCV

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.1.0-brightgreen.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

Welcome to the Automatic Door System project! This project integrates **ESP32-CAM**, **NestJS**, and **OpenCV** to create an automated door system that recognizes license plates and controls door access.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Hang's Job](#hangs-job)

## Overview

This project aims to build a smart automatic door system capable of recognizing license plates using **ESP32-CAM** and **OpenCV**. The system sends relevant data to a **NestJS**-powered web server, which processes the information and manages door control actions.

This README is a work in progress, and the project is still under active development. Stay tuned for updates!

## Features

- **License Plate Recognition**: Automatically detects and identifies vehicle license plates using the ESP32-CAM and OpenCV.
- **Remote Control**: Control the door remotely through a web server powered by NestJS.
- **Secure Access**: The door only opens for recognized license plates, providing secure access.
- **Customizable Actions**: Configurable actions such as door open/close timings and security features.
- **Real-time Monitoring**: Monitor access logs in real-time via the web interface.

## Installation

### Prerequisites

Make sure you have the following installed:

- **Node.js** (v14 or higher)
- **Python** (for OpenCV integration)
- **ESP32-CAM module**
- **RFID module** (optional, for RFID-based access)

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/project-name.git
    ```
2. **Navigate to the project directory**:
    ```bash
    cd project-name
    ```
3. **Install dependencies**:
    For the web server:
    ```bash
    npm install
    ```
    For the OpenCV setup:
    ```bash
    pip install -r requirements.txt
    ```
4. **Setup ESP32-CAM**:
    Flash the appropriate firmware on the ESP32-CAM following [this guide](link-to-guide).

5. **Start the web server**:
    ```bash
    npm run start
    ```

## Usage

To run the project, follow these steps:

1. Install dependencies:
    ```bash
    npm install
    ```

2. Start the web server:
    ```bash
    npm run dev
    ```

3. Connect the ESP32-CAM to the system and ensure it's broadcasting video and capturing images for license plate recognition.

4. Access the web interface at `http://localhost:3000` to monitor and control the door.

### Example Commands

- **To recognize a license plate**:
    ```bash
    python recognize_plate.py --image path/to/image
    ```

## Screenshots

Include screenshots here to give users a visual understanding of the project in action. (e.g., system dashboard, license plate recognition, door control).

## Hang's Job

This section outlines the implementation details for the hardware and peripheral components. Here’s a breakdown:

### RFID + Servo Integration
- **RFID Module**: Scanning an RFID tag will trigger the servo to rotate by 90 degrees.
  - [RFID Setup Part 1](https://www.youtube.com/watch?v=gZ4hLL-SfdA)
  - [RFID Setup Part 2](https://www.youtube.com/watch?v=2RNliD0wpN8)

- **Servo Motor Control**: The servo rotates by 90 degrees when a signal is received.
  - [Servo Setup](https://www.youtube.com/watch?v=0sWor4_BW2I&t=734s)

### UART Communication
- Sending a signal `"1"` will rotate one servo by 90 degrees, and signal `"2"` will rotate two servos by 90 degrees.
- Use `serial.print` to transmit data via UART. The **TX** pin is for transmission, and the **RX** pin is for receiving. For testing, loop the TX and RX pins together.

### LCD Display
- Use the **LCD1602A** display to show status messages like “Door 1 Open” or “Door 2 Open.”
- Ensure correct initialization (4-bit mode recommended).

### Proximity Sensor
- Detect objects in front of the door. If an obstacle is present, the door will not close. After 4 seconds without obstacles, the door will close.

### Combined System Flow
- The system will receive signals from **ESP32-CAM** over UART.
- `"1"` opens one door; `"2"` opens both doors. LCD displays the action.
- Proximity sensors prevent the door from closing if an obstacle is detected.

**Deadline**: September 21, 2024, 22:00.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please reach out to:

- **Your Name**: [email@example.com](mailto:email@example.com)
- **GitHub**: [Your GitHub Profile](https://github.com/your-username)

---

### Useful Resources
- [GitHub Tutorial](https://www.youtube.com/playlist?list=PLQH9LiOP43c33JLu6VYLFyLNS4xCM7RwM) — A helpful playlist for getting started with GitHub and using GitHub Desktop.
