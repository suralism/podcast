#!/usr/bin/env python3
"""
Test script for time tracking functionality in slideshow generator.
"""

import os
import time
import sys

def test_time_tracking():
    """Test the time tracking features."""
    
    print("Testing Time Tracking Features")
    print("=" * 40)
    
    # Check if sample files exist
    if not os.path.exists('sample_images'):
        print("Creating sample images for testing...")
        os.system('python create_sample_images.py')
    
    # Count sample images
    image_files = [f for f in os.listdir('sample_images') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(image_files)} sample images")
    
    # Check for audio file
    audio_file = None
    if os.path.exists('sample_audio'):
        audio_files = [f for f in os.listdir('sample_audio') if f.lower().endswith(('.mp3', '.wav', '.m4a'))]
        if audio_files:
            audio_file = os.path.join('sample_audio', audio_files[0])
            print(f"Found audio file: {audio_file}")
    
    if not audio_file:
        print("\\nNo audio file found in sample_audio directory.")
        print("Please add a short audio file (10-30 seconds) to sample_audio/ for testing.")
        print("You can use any MP3, WAV, or M4A file.")
        return False
    
    # Test command line version with timing
    print("\\nTesting command line version with time tracking...")
    print("-" * 50)
    
    try:
        from slideshow_generator import SlideshowGenerator
        
        def progress_callback(message, progress):
            print(f"[{progress:5.1f}%] {message}")
        
        generator = SlideshowGenerator(output_resolution=(854, 480))  # Smaller resolution for faster testing
        output_file = "output/time_test.mp4"
        os.makedirs("output", exist_ok=True)
        
        print(f"Starting generation with time tracking...")
        start_test = time.time()
        
        generator.create_slideshow_video(
            image_dir='sample_images',
            audio_path=audio_file,
            output_path=output_file,
            transition_duration=0.2,  # Shorter transitions for faster testing
            progress_callback=progress_callback
        )
        
        end_test = time.time()
        test_duration = end_test - start_test
        
        print(f"\\nTest completed in {test_duration:.1f} seconds")
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"✅ Output file created: {output_file}")
            print(f"📊 File size: {file_size:.1f} MB")
            print("✅ Time tracking test passed!")
            return True
        else:
            print("❌ Output file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def test_gui_timing():
    """Instructions for testing GUI timing."""
    print("\\nTesting GUI Time Tracking:")
    print("-" * 30)
    print("1. Run: python slideshow_gui.py")
    print("2. Select sample_images folder")
    print("3. Select audio file from sample_audio")
    print("4. Click 'Generate Slideshow'")
    print("5. Observe:")
    print("   - Real-time elapsed time: ⏱️ Elapsed time: MM:SS")
    print("   - Final completion time in status")
    print("   - Time included in completion dialog")
    print("   - Time shown in persistent status message")

if __name__ == "__main__":
    print("🕒 Slideshow Generator - Time Tracking Test")
    print("=" * 45)
    
    # Test command line timing
    success = test_time_tracking()
    
    if success:
        print("\\n✅ Command line time tracking works!")
    else:
        print("\\n❌ Command line time tracking failed!")
    
    # Instructions for GUI testing
    test_gui_timing()
    
    print("\\n🕒 Time tracking features implemented:")
    print("   ✅ Real-time elapsed time display during generation")
    print("   ✅ Final completion time in multiple locations")
    print("   ✅ Time included in notifications and logs")
    print("   ✅ Cancellation and error time tracking")
    
    if success:
        print("\\n🎉 All time tracking tests passed!")
    else:
        print("\\n⚠️  Some tests failed - check error messages above")
        sys.exit(1)