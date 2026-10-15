@echo off
title ESP32 Thonny Fix
setlocal

rem ==========================================================
rem  ESP32 "Device is busy" fix for Thonny on Windows
rem
rem  NOTE: This launcher is intentionally ASCII-only.
rem  cmd.exe decodes .bat files using the console code page at
rem  start-up, so Korean text here would break on some PCs.
rem  All user-facing Korean messages are printed by the Python
rem  script instead, which writes to the Windows console with
rem  the wide-char API and is therefore code-page independent.
rem ==========================================================

set "PY="
if not defined PY if exist "%ProgramFiles%\Thonny\python.exe" set "PY=%ProgramFiles%\Thonny\python.exe"
if not defined PY if exist "%ProgramFiles(x86)%\Thonny\python.exe" set "PY=%ProgramFiles(x86)%\Thonny\python.exe"
if not defined PY if exist "%LOCALAPPDATA%\Programs\Thonny\python.exe" set "PY=%LOCALAPPDATA%\Programs\Thonny\python.exe"

if not defined PY goto no_thonny

"%PY%" "%~dp0esp32_fix.py"
echo.
pause
exit /b 0

:no_thonny
echo.
echo   [!] Thonny not found. / Thonny installation was not found.
echo       Please install Thonny first.
echo.
pause
exit /b 1