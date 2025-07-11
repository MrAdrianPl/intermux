<div align="center">

# 🌐 InterMux

### Advanced Network Interface Management for Linux

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/license/mit)
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

- **Multi-WAN Management**: Route different applications through different internet connections — boost speed, balance load, or bypass network-specific restrictions
- **Network Testing**: Test applications on specific network interfaces
- **Security Isolation**: Isolate applications in separate network namespaces
- **Bandwidth Management**: Control which apps use which network connections
- **Development**: Test network-dependent applications across different interfaces


## 💡 Why I Made It

I was downloading a large file via torrent, and while waiting, I opened YouTube to pass the time.
But the videos were stuck on low quality, buffering like crazy — even though my connection showed 300 Mbps.

Turns out, the torrent was consuming all the bandwidth, and YouTube was left starving.
That’s when I had the idea: “What if I could assign different apps to different networks?”

After some research, I found that while Linux supports advanced networking, there wasn’t a simple tool to do what I needed — especially one that was GUI-friendly and straightforward.

So I built InterMux:
A utility that lets me bind any app to a specific interface with ease — no messy configs, no guesswork, just full control.

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

# Python Virtual environment
python -m venv venv
source venv/bin/activate

# Python dependencies in the venv
pip3 install -r requirements.txt
```

- Note for Ubuntu 24.04+ users: Some Python modules (like brotli) may require system-level installation.

```bash
# If pip fails
sudo apt install python3-brotli
```

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/intermux.git
cd intermux


# Python Virtual environment
python -m venv venv
source venv/bin/activate

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

The CLI provides full functionality for managing network interface bindings from the command line:

#### 1. List Active Interfaces

```bash
sudo python3 cli.py list
```

Output example:
```
--- Active Network Interfaces ---

Interface: wlan0
  Status: UP
  Type: Wi-Fi
  IP Addresses: 192.168.1.100/24, fe80::1234:5678:9abc:def0/64
  Gateways: 192.168.1.1

Interface: enp7s0f4u1
  Status: UP
  Type: Ethernet
  IP Addresses: 10.252.21.95/24
  Gateways: 10.252.21.177
```

#### 2. Assign Application to Interface

```bash
sudo python3 cli.py assign --app /usr/lib/firefox/firefox --iface wlan0
```

This command:
1. Creates a network namespace for the interface
2. Sets up virtual ethernet pairs (veth0/veth1)
3. Configures routing within the namespace
4. Launches the application in the isolated environment

#### 3. Clear All Assigned Paths

```bash
sudo python3 cli.py clear
```

Removes all custom routing tables and clears assigned paths.

#### 4. Reset Everything

```bash
sudo python3 cli.py reset
```

Completely resets the system by:
- Removing all veth interfaces
- Deleting network namespaces
- Clearing custom routing tables
- Restoring system to defaults

#### CLI Help

```bash
python3 cli.py --help
python3 cli.py <command> --help  # For command-specific help
```

## 🎥 Tutorial Video

![Screencast_20250710_223520_gfnqkq](https://github.com/user-attachments/assets/c018bddd-7f32-4471-a3f1-da75d4463c3c)


## 🏗️ Architecture

```
intermux/
├── core/                   # Core functionality
│   ├── interface.py       # Network interface detection
│   └── router.py          # Routing table management
├── gui/                    # GUI components
│   ├── app.py             # Main GUI application
│   ├── gui.py             # Legacy GUI interface
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

## ⚠️ Known Limitations

### Browser Compatibility

- ✅ **Firefox**: Fully supported (`/usr/lib/firefox/firefox`)
- ❌ **Chromium**: Currently not supported due to sandboxing conflicts
- ✅ **Other Applications**: Most GUI and CLI applications work correctly

### System Requirements

- Root privileges required for network namespace operations
- Linux kernel with network namespace support
- iproute2 package for network management

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

- 🐛 [Report bugs](https://github.com/Rishi-Bhati/intermux/issues)
- 💡 [Request features](https://github.com/Rishi-Bhati/intermux/issues)

---

<div align="center">
  <strong>Made with ❤️ for the Linux community</strong>
</div>
</create_file>
