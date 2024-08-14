# Automatic door using Esp32-Cam, Web Nestjs and OpenCV

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.1.0-brightgreen.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This project I'm working on is still in the process of being completed so please wait a few more months. And this readme version is also a work in progress. 

This is an automatic door model using esp32-cam to automatically recognize license plates and send the necessary data to the web server.

## Features

- Feature 1
- Feature 2
- Feature 3

Describe the major features of your project.

## Installation

### Prerequisites

- List any dependencies or system requirements here.

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/project-name.git
    ```
2. Navigate to the project directory:
    ```bash
    cd project-name
    ```
3. Install the necessary dependencies:
    ```bash
    npm install
    # or
    pip install -r requirements.txt
    ```
4. (Optional) Provide any additional setup steps here.

## Usage

Explain how to use the project. You can provide code snippets or command examples here:

```bash
npm i requirements.txt

cd main

pnpm i # install all files from vercel

pnpm run dev # Run webserver

```
## Việc của Hằng
- RFID: Quét mã RFID sẽ chạy 1 servo 90 độ có biến thời gian quay là const thay đổi được đặt ở đầu.
- UART: nếu gửi chữ "1" thì 1 servo sẽ quay 90 độ( nên tạo cùng 1 hàm để sử dụng lại ) còn nếu gửi "2" thì 2 servo sẽ quay 90 độ. 
- LCD: hiển thị ra được màn hình lcd1602a cái gì cũng được 
- Về cái UART em cứ hiểu cái serial.print chính là gửi đi rồi nên xem lại thì nó sẽ gửi luôn lại ở phần đọc của serial.
 
### Những thứ cần mua:
- Đế nạp esp32-cam
- OV2640 5MP
- RFID - RC522
- SG90