#!/usr/bin/env python3
"""
Test script for the enhanced slideshow generator with progress callbacks.
"""

import os
import sys
from slideshow_generator import SlideshowGenerator

def test_progress_callback():
    """Test the slideshow generator with progress callbacks."""
    
    def progress_callback(message, progress):
        print(f"[{progress:5.1f}%] {message}")
    
    # Check if sample files exist
    if not os.path.exists('sample_images'):
        print("Error: sample_images directory not found")
        print("Run: python create_sample_images.py first")
        return False
    
    # Count images
    image_files = [f for f in os.listdir('sample_images') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if len(image_files) < 5:
        print("Error: Need at least 5 sample images")
        print("Run: python create_sample_images.py first")
        return False
    
    print(f"Found {len(image_files)} sample images")
    
    # Create a test audio file (silent) if none exists
    audio_file = None
    audio_dir = 'sample_audio'
    if os.path.exists(audio_dir):
        audio_files = [f for f in os.listdir(audio_dir) if f.lower().endswith(('.mp3', '.wav', '.m4a', '.aac'))]
        if audio_files:
            audio_file = os.path.join(audio_dir, audio_files[0])
    
    if not audio_file:
        print("No audio file found in sample_audio directory")
        print("Please add an audio file to sample_audio/ directory for testing")
        return False
    
    print(f"Using audio file: {audio_file}")
    
    # Test the generator
    try:
        generator = SlideshowGenerator(output_resolution=(1280, 720))
        
        output_file = "output/test_progress.mp4"
        os.makedirs("output", exist_ok=True)
        
        print("\\nStarting slideshow generation with progress tracking...")
        print("=" * 60)
        
        generator.create_slideshow_video(
            image_dir='sample_images',
            audio_path=audio_file,
            output_path=output_file,
            transition_duration=0.5,
            progress_callback=progress_callback
        )
        
        print("=" * 60)
        print("Test completed successfully!")
        
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"Output file: {output_file}")
            print(f"File size: {file_size:.1f} MB")
            return True
        else:
            print("Error: Output file was not created")
            return False
            
    except Exception as e:
        print(f"Error during generation: {e}")
        return False

if __name__ == "__main__":
    success = test_progress_callback()
    if success:
        print("\\n✅ Progress callback test passed!")
    else:
        print("\\n❌ Progress callback test failed!")
        sys.exit(1)