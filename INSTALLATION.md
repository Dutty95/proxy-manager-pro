# ProxyManager Installation Guide

## Installation Options

### Option 1: Run the Executable (Windows Only)

1. Navigate to the `dist` folder
2. Double-click on `ProxyManager.exe` to launch the application
3. No installation required - the application will run directly

### Option 2: Run from Source Code

#### Prerequisites
- Python 3.x installed
- Required packages installed (see below)

#### Installing Required Packages
```
pip install pillow geoip2
```

#### Running the Application
```
python -m ui.dashboard
```

## First-Time Setup

1. When you first run the application, you'll need to select a proxy file
2. Click the "Browse" button and select your proxy list file
3. Click "Validate Proxies" to check which proxies are working
4. Select an application from the dropdown to route through a proxy
5. Choose a proxy type (SOCKS4, SOCKS5, or HTTP)
6. Optionally filter proxies by country
7. Click "Start Routing" to launch the selected application through the proxy

## Troubleshooting

### Missing GeoIP Database
The application will work without the GeoIP database, but for full functionality:
1. Download the GeoLite2 City database from MaxMind (requires free account)
2. Place the `.mmdb` file in the `data` directory
3. Rename it to `GeoLite2-City.mmdb`

### Proxy Validation Failures
If many proxies fail validation:
1. Check your internet connection
2. Ensure your proxy list is up-to-date
3. Try different proxy types (SOCKS4, SOCKS5, HTTP)

### Application Routing Issues
If the application doesn't route through the proxy:
1. Make sure the application supports proxy routing
2. Check that the proxy is working (validated)
3. Try a different proxy type

## Support

For additional help or to report issues, please contact the developer.