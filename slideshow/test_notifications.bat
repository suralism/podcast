@echo off
echo Testing Enhanced Completion Notification System
echo =============================================
echo.

echo Testing basic notification functionality...
python completion_notifier.py

echo.
echo Testing GUI with sample data...
echo Make sure sample images exist:
if not exist "sample_images\*.jpg" (
    echo Creating sample images...
    python create_sample_images.py
)

echo.
echo Checking for sample audio...
if not exist "sample_audio" mkdir sample_audio

echo.
echo You can now test the enhanced slideshow generator:
echo   1. Run: python slideshow_gui.py
echo   2. Use sample_images folder for images
echo   3. Add an audio file to sample_audio folder
echo   4. Generate slideshow and observe completion notifications
echo.
echo Features to test:
echo   - Progress bar with detailed status updates
echo   - Visual completion indicator
echo   - Sound notification (Windows)
echo   - Persistent completion status message
echo   - Enhanced completion dialog
echo.
pause