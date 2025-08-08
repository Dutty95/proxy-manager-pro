# ProxyManager Executable Build Instructions

## Overview
This document provides instructions for building the ProxyManager application into a standalone executable file that can be run on Windows without requiring Python to be installed.

## Prerequisites
- Python 3.x installed
- Required Python packages:
  - PyInstaller
  - Pillow (PIL)
  - geoip2
  - tkinter (usually comes with Python)

## Building the Executable

### Automatic Build (Recommended)
1. Simply run the `build_exe.bat` file by double-clicking it
2. Wait for the build process to complete
3. The executable will be created in the `dist` folder

### Manual Build
1. Open a command prompt in the project directory
2. Run: `pyinstaller proxymanager.spec --clean`
3. The executable will be created in the `dist` folder

## Running the Application
1. Navigate to the `dist` folder
2. Double-click on `ProxyManager.exe` to launch the application

## Troubleshooting

### Missing DLLs
If you encounter missing DLL errors when running the executable, you may need to install the Visual C++ Redistributable for Visual Studio 2015-2022.

### Missing Data Files
If the application complains about missing data files, ensure that the `data` directory was properly included during the build process. You can manually copy the `data` folder to the same directory as the executable if needed.

### GeoIP Database
The application will work without the GeoIP database, but for full functionality, you should obtain a GeoLite2 City database file and place it in the `data` directory.

## Distribution
To distribute the application:
1. Copy the entire `dist/ProxyManager` directory
2. Share it with users who need to run the application

## Notes
- The executable includes all necessary dependencies
- No installation is required - it's a portable application
- The application will create necessary folders and files when run for the first time