@echo off
echo Starting Proxy Manager...
cd %~dp0
if exist dist\ProxyManager.exe (
    start "" "dist\ProxyManager.exe"
) else (
    echo Error: ProxyManager.exe not found in the dist folder.
    echo Please build the application first using build_exe.bat
    pause
)