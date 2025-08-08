@echo off
echo Building ProxyManager executable...

:: Run PyInstaller with our spec file
pyinstaller proxymanager.spec --clean

echo.
if %ERRORLEVEL% == 0 (
    echo Build completed successfully!
    echo Executable is located in the dist folder.
) else (
    echo Build failed with error code %ERRORLEVEL%
)

pause