# 📡 Pinger: Terminal Connectivity Tester

> **A simplified, async network tester with a clean table interface.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

I wanted a ping tool that felt more like a modern dashboard and less like a raw log stream. **Pinger** is a Python wrapper around the `ping3` library that formats network responses into a clean, vertically centered table.

It’s built for quick diagnostics when you need to watch connection stability without squinting at scrolling text.

---

## 📸 Demo

<p align="center">
  <img src="./assets/demo.gif" alt="Demo">
</p>

---

## 🎯 What it does

* **Structured Display:** Replaces the standard ping output with an aligned data table.
* **Auto-Centering:** Automatically centers the interface vertically and horizontally in your terminal.
* **Visual Feedback:** Uses ANSI colors to instantly flag **UP** (Green) or **DOWN** (Red) status.
* **Smart Summary:** Calculates packet loss, latency stats (min/max), and average latency after the session.
* **Input Validation:** Prevents invalid IPs or hostnames from crashing the script.

---

## ✨ Why use this?

* **Better Readability:** The standard `ping` command is hard to parse at a glance. This organizes data into columns.
* **Dual Mode:** Run it with flags for speed, or run it empty to get a guided interactive menu.
* **Zero System Dependencies:** It uses raw sockets via Python, so it does not rely on the OS's native `ping` binary.

---

## 🚀 Installation

Pinger requires **Python 3.9+** (for async features).

    # Clone the repository
    git clone https://github.com/oNxZero/pinger.git

    # Enter the directory
    cd pinger

    # Install dependencies
    pip install ping3 colorama

> **⚠️ Important:** Because this tool uses raw ICMP sockets, you must run it with **Administrator** privileges on Windows or using `sudo` on Linux/macOS.

---

## 📖 Usage

### Interactive Mode
Run the script without arguments to enter the wizard. It will center itself on your screen and ask for details.

    # Linux/macOS
    sudo python pinger.py

    # Windows (Run as Admin)
    python pinger.py

### Fast-Start (CLI Flags)
Skip the menu and start pinging immediately.

    # Ping google.com (defaults: 8 pings, 500ms interval)
    sudo python pinger.py google.com

    # Custom: 1.1.1.1, 5 times, 200ms interval, 1000ms timeout
    sudo python pinger.py 1.1.1.1 -c 5 -i 200 -t 1000

### Command Line Help
View all available options:

    $ python pinger.py -h

    Usage:
      pinger HOST [-c COUNT] [-i INTERVAL_MS] [-t TIMEOUT_MS]
      pinger -h | --help

    Flags:
      HOST                IP address or hostname to ping
      -c,  --count COUNT    Number of pings to send (default: 8)
      -i,  --interval MS    Delay between pings in milliseconds (default: 500)
      -t,  --timeout  MS    Timeout per ping in milliseconds (default: 1000)
      -h,  --help           Show this help and exit

---

## 📊 Output Explained

**Live Table:**
| Column | Description |
| :--- | :--- |
| **TRY** | The sequence number of the current packet. |
| **TARGET** | The Hostname or IP being pinged. |
| **PROTOCOL** | The protocol used (ICMP). |
| **LATENCY** | Round-trip time in milliseconds. |
| **BYTES** | Size of the packet sent (default 64). |
| **STATUS** | **UP** (Host reachable) or **Down** (Timeout/Unreachable). |

**Summary Stats:**
After the session, Pinger displays a report:
* **Packets:** Sent, Received, Lost (with Loss %).
* **Latency:** Average, Minimum, and Maximum times.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
