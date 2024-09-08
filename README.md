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

# Hang's Job

This project involves working with Arduino and ESP32 to control servos via UART signals and display messages on an LCD. The servos' positions will be saved in EEPROM to retain the state during power interruptions.

## Overview

The goal of this project is to:
- Upload specific code files to GitHub.
- Control one or two servos based on UART input.
- Display messages on an LCD.
- Save and retrieve servo angles from EEPROM after power interruptions.
- Ensure that servo positions reset after 15 seconds unless blocked by an infrared sensor.

## Tasks

1. **Uploading Files to GitHub**:
    - Ensure familiarity with GitHub and how to upload files using GitHub Desktop or the Git command line.
    - Upload two files named `r3.ino` and `esp32.ino` into a folder called `Arduino` in the root directory of the repository.

2. **File Requirements**:
    - **`r3.ino`**:
        - Read UART signals, specifically the characters `1` and `2`.
        - If the UART signal is `1`, rotate one servo by 90 degrees.
        - If the UART signal is `2`, rotate two servos by 90 degrees.
        - The servo speed should be adjustable via a variable at the beginning of the file.
        - After 15 seconds, the servo(s) should return to 0 degrees unless blocked by an infrared sensor. This feature can be implemented using a timer.
        - Display the following messages on the LCD1602A (with I2C interface):
            - "Open the left door" when one servo is active.
            - "Open 2 doors" when both servos are active.
        - Save the angles of both servos to EEPROM so that if power is lost and restored, the servos will continue from their last positions.

    - **`esp32.ino`**:
        - Create a function to send UART signals with the characters `1` and `2`.

## Useful Resources

- [GitHub Tutorial](https://www.youtube.com/playlist?list=PLQH9LiOP43c33JLu6VYLFyLNS4xCM7RwM) — A helpful playlist for getting started with GitHub and recommending use GitHub Desktop.
- [Arduino Components and Libraries](https://youtube.com/playlist?list=PLQH9LiOP43c0PZqBtf1zBjtphZnkln0AN&si=o8JU_rhS4OZeefNO) — Understand how to use Arduino components and libraries.
- [UART](https://www.programmingboss.com/2021/04/esp32-arduino-serial-communication-with-code.html#gsc.tab=0) - This is almost done, just find a way to send it back.
## Timeline

![Timeline](Images/timeline_with_H.png)

In this section, we will document the progress and task completion status for Hang:
- [x] This is an example
- [ ] Learn how to upload files to GitHub.
- [ ] Upload `r3.ino` and `esp32.ino` to the `Arduino` folder in the root directory.
- [ ] Implement UART signal handling in `r3.ino`.
- [ ] Implement servo control based on UART input.
- [ ] Add LCD1602A display logic.
- [ ] Save servo positions to EEPROM.
- [ ] Implement infrared sensor check for resetting servo position.
- [ ] Create UART signal sending function in `esp32.ino`.

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

- **Your Name**: [quangvinh07032003@gmail.com](mailto:quangvinh07032003@gmail.com)
- **GitHub**: [Zinjpq](https://github.com/Zinjpq)

---