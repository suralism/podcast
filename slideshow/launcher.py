#!/usr/bin/env python3
"""
Launcher for Podcast Slideshow Generator GUI
This script ensures dependencies are installed before launching the GUI.
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required dependencies."""
    try:
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies")
        return False

def check_dependencies():
    """Check if all required dependencies are available."""
    required_modules = ['tkinter', 'PIL', 'moviepy', 'mutagen']
    missing = []
    
    for module in required_modules:
        try:
            if module == 'tkinter':
                import tkinter
            elif module == 'PIL':
                import PIL
            elif module == 'moviepy':
                import moviepy
            elif module == 'mutagen':
                import mutagen
        except ImportError:
            missing.append(module)
    
    return missing

def launch_gui():
    """Launch the GUI application."""
    try:
        import slideshow_gui
        slideshow_gui.main()
    except ImportError as e:
        print(f"Error importing GUI module: {e}")
        return False
    except Exception as e:
        print(f"Error launching GUI: {e}")
        return False
    return True

def main():
    """Main launcher function."""
    print("🎬 Podcast Slideshow Generator - GUI Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check if we're in the right directory
    if not os.path.exists('slideshow_gui.py'):
        print("Error: slideshow_gui.py not found")
        print("Make sure you're running this from the correct directory")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        if os.path.exists('requirements.txt'):
            response = input("Install dependencies now? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                if not install_dependencies():
                    input("Press Enter to exit...")
                    sys.exit(1)
                
                # Check again after installation
                missing = check_dependencies()
                if missing:
                    print(f"Still missing dependencies: {', '.join(missing)}")
                    input("Press Enter to exit...")
                    sys.exit(1)
            else:
                print("Cannot launch GUI without required dependencies")
                input("Press Enter to exit...")
                sys.exit(1)
        else:
            print("requirements.txt not found")
            input("Press Enter to exit...")
            sys.exit(1)
    
    # Launch GUI
    print("Launching GUI...")
    if not launch_gui():
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()