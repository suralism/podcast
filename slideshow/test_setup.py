#!/usr/bin/env python3
"""
Test Script for Slideshow Generator
This script tests the basic functionality of the slideshow generator.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ['PIL', 'moviepy', 'mutagen']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'moviepy':
                import moviepy
            elif package == 'mutagen':
                import mutagen
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install dependencies.")
        return False

def create_test_images():
    """Create test images for slideshow."""
    print("Creating test images...")
    try:
        subprocess.check_call([sys.executable, 'create_sample_images.py'])
        print("Test images created successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to create test images.")
        return False

def main():
    """Main test function."""
    print("Podcast Slideshow Generator - Test Script")
    print("=" * 45)
    
    # Check if dependencies are installed
    missing = check_dependencies()
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("Installing dependencies...")
        if not install_dependencies():
            sys.exit(1)
    else:
        print("All dependencies are installed!")
    
    # Create test images
    if not os.path.exists('sample_images') or len(os.listdir('sample_images')) == 0:
        if not create_test_images():
            sys.exit(1)
    else:
        print("Test images already exist!")
    
    print("\nSetup completed successfully!")
    print("\nTo create a slideshow:")
    print("1. Add an audio file (MP3, WAV, etc.) to the sample_audio folder")
    print("2. Run the following command:")
    print("   python slideshow_generator.py sample_images sample_audio/your_audio_file.mp3 -o output/slideshow.mp4")
    print("\nExample:")
    print("   python slideshow_generator.py sample_images sample_audio/podcast.mp3 -o output/my_slideshow.mp4")

if __name__ == "__main__":
    main()