# Quadruped Robot Servo Controller

This project is a GUI application to control a quadruped robot’s servos using Python and Tkinter. It allows users to save and load various robot states and communicate with a Raspberry Pi Pico over serial. This project also includes the necessary code for the Raspberry Pi Pico to receive commands and control the servos accordingly.

## Project Overview

The GUI allows you to:
- Manually adjust the hip and knee angles of each of the four legs of the quadruped.
- Save custom configurations (or "states") of the quadruped’s positions.
- Load saved configurations for predefined or custom actions.
- Send commands to a Raspberry Pi Pico to update the quadruped’s positions over a serial connection.

The code on the Pico listens for commands from the GUI and sets the angles of each servo accordingly.

## Prerequisites

1. **Python 3.x** with the following packages:
    - `tkinter` for GUI interface
    - `json` for saving/loading states
    - `pyserial` for serial communication
2. **Raspberry Pi Pico** with MicroPython firmware installed.

## Installation and Setup

1. Clone this repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Install required packages:
    ```bash
    pip install pyserial
    ```

3. Run the main GUI application:
    ```bash
    python QuadrupedGUI.py
    ```

4. For the Pico:
    - Copy the `main.py` and `boot.py` files within the "Pico" folder to the Pico. The `boot.py` will ensure the program runs on startup, while `main.py` handles servo control.
    - Install the program using a MicroPython-capable IDE (e.g., Thonny).

5. Connect the Pico to the system and identify its serial port (usually found in device manager or `ls /dev/tty*` on Linux). Adjust the port in the `SerialCommunicator` class if needed.

## Project Structure

```plaintext
.
├── QuadrupedGUI.py        # Main GUI application
├── Pico/
│   ├── boot.py              # Runs on Pico boot, imports main.py
│   ├── main.py              # Handles servo control on the Pico
└── README.md              # Project documentation
