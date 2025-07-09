<div align="center">

# 🌐 InterMux

### Advanced Network Interface Management for Linux

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-orange.svg)](https://www.linux.org/)
[![Root Required](https://img.shields.io/badge/privileges-root%20required-red.svg)](https://en.wikipedia.org/wiki/Superuser)

<p align="center">
  <strong>Bind applications to specific network interfaces with ease</strong>
</p>

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

**InterMux** is a powerful Linux utility that enables you to bind applications to specific network interfaces. Whether you need to route your browser through Wi-Fi while keeping your development server on Ethernet, or isolate applications for security testing, InterMux makes it simple.

### 🎯 Use Cases

- **Multi-WAN Management**: Route different applications through different internet connections
- **Network Testing**: Test applications on specific network interfaces
- **Security Isolation**: Isolate applications in separate network namespaces
- **Bandwidth Management**: Control which apps use which network connections
- **Development**: Test network-dependent applications across different interfaces

## ✨ Features

<table>
<tr>
<td>

### 🖥️ Core Features
- 🔍 **Auto-detection** of all network interfaces
- 🛣️ **Custom routing tables** per interface
- 🔒 **Network namespace isolation**
- 📊 **Real-time interface monitoring**
- 🎛️ **Both CLI and GUI interfaces**

</td>
<td>

### 🌟 Interface Support
- 📶 **Wi-Fi** (wlan*, wl*)
- 🔌 **Ethernet** (eth*, en*)
- 📱 **USB Tethering**
- 🔵 **Bluetooth Tethering**
- 🌐 **Virtual Interfaces**

</td>
</tr>
</table>

## 🚀 Installation

### Prerequisites

```bash
# Required system packages
sudo apt update
sudo apt install -y python3 python3-pip python3-tk iproute2 iptables

# Python dependencies
pip3 install -r requirements.txt
```

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/intermux.git
cd intermux

# Install Python dependencies
pip3 install -r requirements.txt

# Make scripts executable (optional)
chmod +x core/router.py
```

## 📖 Usage

### 🎨 GUI Mode (Recommended)

Launch the modern graphical interface:

```bash
# The GUI will request root privileges via pkexec
python3 gui/app.py
```

<details>
<summary><strong>GUI Features</strong></summary>

- **Interface Selection**: Dropdown menu with all active interfaces
- **Application Binding**: Easy path entry and interface assignment
- **Visual Management**: See all created bindings at a glance
- **One-Click Actions**: Assign, refresh, and clear operations

</details>

### 💻 CLI Mode

#### 1. List Active Interfaces

```bash
python3 core/interface.py
```

Output example:
```
--- Detected Network Interfaces ---

Interface: wlan0
  Status: UP
  Type: Wi-Fi
  MAC Address: AA:BB:CC:DD:EE:FF
  IP Addresses: 192.168.1.100/24
  Metric: 600
  Gateways: 192.168.1.1
  System DNS Servers: 8.8.8.8, 8.8.4.4
```

#### 2. Setup Routing Tables

```bash
sudo python3 core/router.py
```

This creates custom routing tables for each active interface.

#### 3. Bind Applications (via GUI)

Use the GUI to bind applications to specific interfaces. The binding process:
1. Creates a network namespace for the interface
2. Sets up virtual ethernet pairs
3. Configures routing within the namespace
4. Launches the application in the isolated environment

## 🏗️ Architecture

```
intermux/
├── core/                   # Core functionality
│   ├── interface.py       # Network interface detection
│   └── router.py          # Routing table management
├── gui/                    # GUI components
│   ├── app.py             # Main GUI application
│   ├── gui.py             # Legacy GUI interface
│   └── configure.py       # Configuration window
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### 🔧 How It Works

1. **Interface Detection**: Scans system for all network interfaces using `ip` commands
2. **Routing Tables**: Creates custom routing tables in `/etc/iproute2/rt_tables`
3. **Network Namespaces**: Isolates applications using Linux network namespaces
4. **Virtual Interfaces**: Uses veth pairs to connect namespaces to physical interfaces
5. **IP Forwarding**: Configures NAT/masquerading for namespace connectivity

## 🛠️ Advanced Configuration

### Custom Routing Table IDs

Edit `core/router.py` to modify:
```python
BASE_TABLE_ID = 100  # Starting table ID
BASE_PRIORITY = 1000 # Starting priority
```

### Network Namespace Subnet

The default subnet for namespaces is `10.200.1.0/24`. Modify in `gui/configure.py`:
```python
subnet = "10.200.1"  # Change to your preferred subnet
```

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><strong>GUI doesn't launch</strong></summary>

```bash
# Ensure X11 forwarding is enabled
xhost +SI:localuser:root

# Check DISPLAY variable
echo $DISPLAY
```
</details>

<details>
<summary><strong>Permission denied errors</strong></summary>

InterMux requires root privileges for network operations. The GUI uses `pkexec` for privilege escalation.

```bash
# Manual run with sudo
sudo python3 gui/app.py
```
</details>

<details>
<summary><strong>Interface not detected</strong></summary>

```bash
# Check interface status
ip link show

# Bring interface up
sudo ip link set <interface> up
```
</details>

### 📝 Logs and Debugging

Enable verbose logging by modifying `core/interface.py`:
```python
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to all functions
- Include type hints where applicable
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Uses Linux networking stack (iproute2)
- Inspired by the need for better network interface management

## 📞 Support

- 🐛 [Report bugs](https://github.com/yourusername/intermux/issues)
- 💡 [Request features](https://github.com/yourusername/intermux/issues)
- 📧 Contact: your.email@example.com

---

<div align="center">
  <strong>Made with ❤️ for the Linux community</strong>
</div>
