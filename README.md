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
- RFID + Servo: Quét mã RFID sẽ chạy 1 servo 90 độ có biến thời gian quay là const thay đổi được đặt ở đầu. RFID :
[Phần 1](https://www.youtube.com/watch?v=gZ4hLL-SfdA),
[Phần 2](https://www.youtube.com/watch?v=2RNliD0wpN8).
Servo : 
[Link](https://www.youtube.com/watch?v=0sWor4_BW2I&t=734s).
- UART: nếu gửi chữ "1" thì 1 servo sẽ quay 90 độ( nên tạo cùng 1 hàm để sử dụng lại ) còn nếu gửi "2" thì 2 servo sẽ quay 90 độ. Phần này trên youtube dạy lung tung nên hỏi chatgpt cho nhanh. Còn có tài liệu của UART của thầy Mạnh anh để ở file ngoài cùng đó. Về cái UART em cứ hiểu cái serial.print chính là gửi đi rồi nên xem lại thì nó sẽ gửi luôn lại ở phần đọc của serial. TX là Transmission pins còn RX là Reception pins nên ta phải đối ngược 2 cái của 2 thiết bị với nhau còn muốn test hoạt động hay không thì nối 2 cái lại là nó gửi cho chính nó :))
- LCD: hiển thị ra được màn hình lcd1602a cái gì cũng được. Tài liệu anh cũng up trong file luôn. Chú ý phần khai báo, nên dùng loại 4 bit còn sau sau anh đưa cho cái có I2C.
 
### Những thứ cần mua:
- Đế nạp esp32-cam
- OV5640
- RFID - RC522
- SG90