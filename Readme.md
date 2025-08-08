# Proxy Manager Pro

A lightweight and powerful GUI-based proxy manager that validates, rotates, and tunnels traffic through SOCKS4, SOCKS5, and HTTP proxies. Built with Python and Tkinter, featuring an enhanced modern UI and executable distribution.

---

## 🌟 Features

- ✅ Load and categorize proxies by type (SOCKS4, SOCKS5, HTTP)
- ⚡ Validate proxies and measure speed/latency
- 🔁 Automatically rotate slow proxies
- 🌐 Route app/browser traffic through selected proxies
- 📋 Live log view for scanning, rotation, and routing activity
- 📊 Select and monitor individual proxies with real-time performance info
- 🎯 GUI for easy interaction (Start/Stop, Proxy selection, App launch)

---

## 📁 Folder Structure

```

Proxyapp/
│
├── main.py               # App entry point
├── dashboard.py          # GUI interface
├── proxy\_checker.py      # Validates proxies
├── proxy\_rotator.py      # Rotates based on latency
├── proxy\_router.py       # Launches browser/app via proxy
├── proxy\_utils.py        # Utility functions
├── proxy\_loader.py       # Loads proxy files
├── proxy\_tunnel.py       # Tunneling logic
├── logger.py             # Logging
│
├── data/
│   └── validated/        # Categorized proxies
│   └── proxies.txt       # Raw input file
│
├── logs/                 # App logs
├── ui/                   # UI elements (if any)
└── requirements.txt      # Python dependencies

````

---

## 🚀 How to Run

### Option 1: Using the Executable (Windows)

1. Run `run_proxy_manager.bat` or navigate to the `dist` folder and run `ProxyManager.exe`

### Option 2: From Source Code

1. Clone/download the project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m ui.dashboard
```

For detailed installation and usage instructions, see [INSTALLATION.md](INSTALLATION.md).

---

## 📦 Build Executable (.EXE)

To create a `.exe` version:

1. Run the included build script:

```bash
.\build_exe.bat
```

2. Or manually build using PyInstaller with the spec file:

```bash
pyinstaller proxymanager.spec
```

> After building, find the `.exe` file in the `dist/` folder.



---

## 👨‍💻 Author

Built by \[Your Name]. Feel free to contribute or raise issues.

GitHub Repo: [https://github.com/Dutty95/proxy-manager-pro](https://github.com/Dutty95/proxy-manager-pro)

---

## 📄 License

This project is licensed under the MIT License.

```

---

## ✅ To-Do Summary Before GitHub Upload

| Task | Status |
|------|--------|
| requirements.txt | ✅ Generated manually or via `pip freeze` |
| README.md | ✅ You now have one |
| .exe Build | ✅ Almost done, ready for testing |
| GitHub Repo | 🕐 To be created |
| Test on another machine | 🔜 Before release |

