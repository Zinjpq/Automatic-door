# Automatic Door System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.1.0-brightgreen.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

Welcome to the Automatic Door System project! This project integrates **ESP32-CAM**, **Tkinter**, and **OpenCV** to create an automated door system that recognizes license plates and controls door access.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Hardware Support](#hardware-support)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Hang's Job](#hangs-job)

## Overview

This project aims to build a smart automatic door system capable of recognizing license plates using **ESP32-CAM** and **OpenCV**. The system provides a **Tkinter-based** desktop application for monitoring and controlling door access.

This README is a work in progress, and the project is still under active development. Stay tuned for updates!

## Features

- **License Plate Recognition**: Automatically detects and identifies vehicle license plates using ESP32-CAM and OpenCV.
- **Local Desktop Application**: Uses a Tkinter-based GUI for easy monitoring and control.
- **Secure Access**: The door only opens for recognized license plates, ensuring security.
- **Customizable Actions**: Configurable actions such as door open/close timings and security features.
- **Real-time Monitoring**: View access logs and system status via the desktop app.

## Installation

### Prerequisites

Make sure you have the following installed:

- **Python** (for OpenCV and Tkinter)
- **ESP32-CAM module**
- **RFID module** (optional, for RFID-based access)

### Steps

1. **Download the latest release**:
    Go to the [Releases](https://github.com/Zinjpq/AutomaticDoorSystem/releases) page and download the latest version of the application.

2. **Extract the files**:
    Extract the downloaded ZIP file to a folder on your system.

3. **Run the application**:
    Navigate to the extracted folder and run:
    ```bash
    python app.py
    ```

4. **Setup ESP32-CAM**:
    Flash the appropriate firmware on the ESP32-CAM following [this guide](link-to-guide).

## Usage

To run the project, follow these steps:

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the Tkinter application:
    ```bash
    python app.py
    ```

3. Connect the ESP32-CAM to the system and ensure it's broadcasting video and capturing images for license plate recognition.

4. Use the GUI to monitor and control the door.

### Example Commands

- **To recognize a license plate**:
    ```bash
    python recognize_plate.py --image path/to/image
    ```

## Hardware Support

This project supports multiple microcontrollers for door control and automation:

- **Arduino**
- **Raspberry Pi**
- **STM32**

The corresponding schematics can be found in the `simulations/schematics/` directory.

## Screenshots

Include screenshots here to give users a visual understanding of the project in action (e.g., system dashboard, license plate recognition, door control).

## Hang's Job

This project involves working with Arduino, Raspberry Pi, and STM32 to control servos via UART signals and display messages on an LCD. The servos' positions will be saved in EEPROM to retain the state during power interruptions.

## Overview

The goal of this project is to:
- Upload specific code files to GitHub.
- Control one or two servos based on UART input.
- Display messages on an LCD.
- Save and retrieve servo angles from EEPROM after power interruptions.
- Ensure that servo positions reset after 15 seconds unless blocked by an infrared sensor.

## Tasks

1. **Uploading Files to GitHub**:
    - Upload `r3.ino`, `raspi.py`, and `stm32.c` into a folder called `Firmware` in the root directory.

2. **File Requirements**:
    - **`r3.ino`** (Arduino):
        - Read UART signals (`1` and `2`).
        - Control servos based on UART input.
        - Display messages on the LCD1602A (with I2C interface).
        - Save servo positions to EEPROM.
    
    - **`raspi.py`** (Raspberry Pi):
        - Handle UART communication and control GPIO pins.
        - Integrate with the main system to manage door control.

    - **`stm32.c`** (STM32):
        - Implement UART signal handling and servo control logic.

## Timeline

![Timeline](Images/timeline_with_H.png)

Task completion status for Hang:
- [x] Learn how to upload files to GitHub.
- [x] Upload `r3.ino`, `raspi.py`, and `stm32.c` to the `Firmware` folder.
- [ ] Implement UART signal handling in `r3.ino`, `raspi.py`, and `stm32.c`.
- [ ] Implement servo control based on UART input.
- [x] Add LCD1602A display logic.
- [x] Save servo positions to EEPROM.
- [x] Implement infrared sensor check for resetting servo position.
- [ ] Create UART signal sending function in `esp32.ino`.
- [ ] Check all above.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please reach out to:

- **Your Name**: [quangvinh07032003@gmail.com](mailto:quangvinh07032003@gmail.com)
- **GitHub**: [Zinjpq](https://github.com/Zinjpq)
