# 🌊 MSR: Monitoring Submarine Robot

![Project Status](https://img.shields.io/badge/Status-Prototype-orange)
![AI Model](https://img.shields.io/badge/AI-YOLOv11-blue)
![Platform](https://img.shields.io/badge/Platform-NVIDIA%20Jetson%20%7C%20Arduino-green)

> **A Graduation Project for Intelligent Systems Engineering.**
> *Designed to monitor and protect coral reefs in the Gulf of Aqaba, Jordan.*

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [System Architecture](#-system-architecture)
- [Hardware Specifications](#-hardware-specifications)
- [Tech Stack](#-tech-stack)
- [Team & Supervisor](#-team--supervisor)

---

## 💡 About the Project

**MSR** is a specialized Remotely Operated Vehicle (ROV) built to address the environmental challenges facing the Red Sea's coral reefs. Traditional monitoring is expensive and labor-intensive; MSR automates this process using **Computer Vision** and **Deep Learning**.

The system is designed to navigate underwater, stream live video, and utilize a custom-trained **YOLOv11** model to detect and classify coral health in real-time.

---

## 🏗 System Architecture

We utilized a **"Split-Brain" Distributed Architecture** to overcome hardware constraints. Instead of running heavy inference on the edge device, we split the workload:

1.  **The Edge (ROV):** -   **Controller:** NVIDIA Jetson Nano & Arduino.
    -   **Role:** Handles motor control (PWM), reads sensor data, and streams raw video feed via tether.
2.  **The Core (Surface Station/Laptop):**
    -   **Processor:** High-performance GPU.
    -   **Role:** Receives the video stream and runs the **YOLOv11** Deep Learning model for real-time object detection and coral classification.

> **Why this design?** This allows us to use the lightweight Jetson Nano for robust control while leveraging the superior processing power of a laptop for high-FPS AI analysis.

---

## ⚙ Hardware Specifications

| Component | Specification |
| :--- | :--- |
| **Chassis Weight** | 4.7 kg |
| **Dimensions** | ~40 cm Length |
| **Propulsion** | 3x Brushless Motors + ESCs |
| **Microcontroller** | Arduino (Motor/Sensor Interface) |
| **Onboard Computer** | NVIDIA Jetson Nano |
| **Camera** | [Insert Camera Model, e.g., IMX219] |

---

## 🛠 Tech Stack

**Software & AI**
* ![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
* **YOLOv11** (Ultralytics) for Object Detection
* **OpenCV** for Image Processing
* **Visual Studio** (Development Environment)

**Embedded & Electronics**
* ![C++](https://img.shields.io/badge/C++-Embedded-blue?logo=c%2B%2B&logoColor=white)
* **Arduino IDE**
* **I2C / PWM Communication**


---

## 📸 Gallery / Demo

*![WhatsApp Image 2026-02-06 at 9 09 34 PM](https://github.com/user-attachments/assets/029310d9-44c1-456d-80fa-341f83530001)


*
