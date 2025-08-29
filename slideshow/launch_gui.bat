@echo off
title Podcast Slideshow Generator
echo Starting Podcast Slideshow Generator GUI...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "slideshow_gui.py" (
    echo Error: slideshow_gui.py not found
    echo Make sure you are running this from the correct directory
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo Error: requirements.txt not found
    pause
    exit /b 1
)

REM Try to run the GUI
echo Launching GUI...
python slideshow_gui.py

REM If there's an error, try to install dependencies first
if %errorlevel% neq 0 (
    echo.
    echo It looks like there might be missing dependencies.
    echo Attempting to install requirements...
    echo.
    pip install -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo.
        echo Error: Failed to install dependencies
        echo Please run manually: pip install -r requirements.txt
        pause
        exit /b 1
    )
    
    echo.
    echo Dependencies installed. Launching GUI again...
    python slideshow_gui.py
)

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo An error occurred. Check the messages above.
    pause
)