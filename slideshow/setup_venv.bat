@echo off
echo Podcast Slideshow Generator - Virtual Environment Setup
echo ======================================================
echo.

echo Installing dependencies in virtual environment...
pip install --target .venv/Lib/site-packages -r requirements.txt --upgrade

echo.
echo Testing moviepy import...
python -c "import moviepy; print('MoviePy base module: OK')"

echo.
echo Testing slideshow generator...
python slideshow_generator.py --help

echo.
echo Setup completed! You can now use:
echo   python slideshow_gui.py          (for GUI)
echo   python slideshow_generator.py    (for command line)
echo.
pause