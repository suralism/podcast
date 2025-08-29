@echo off
echo Podcast Slideshow Generator - Setup and Test
echo ============================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Creating sample images...
python create_sample_images.py
if %errorlevel% neq 0 (
    echo Error: Failed to create sample images
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo To test the slideshow generator:
echo 1. Add an audio file to the sample_audio folder
echo 2. Run: python slideshow_generator.py sample_images sample_audio\your_audio.mp3 -o output\test_slideshow.mp4
echo.
echo Example with a short audio file:
echo python slideshow_generator.py sample_images sample_audio\podcast.mp3 -o output\slideshow.mp4
echo.
pause