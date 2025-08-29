#!/usr/bin/env python3
"""
Podcast Slideshow Generator
Creates MP4 videos by combining images with audio for podcast episodes.
"""

import os
import sys
import argparse
import math
from pathlib import Path
from typing import List, Tuple
import subprocess
import tempfile
import shutil

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"Missing PIL/Pillow: {e}")
    print("Please install requirements using: pip install -r requirements.txt")
    sys.exit(1)

try:
    import moviepy.editor as mp
except ImportError:
    try:
        # Try alternative import method for different moviepy versions
        import moviepy
        # Import classes directly from moviepy
        from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
        # Create a mock mp module
        class mp:
            AudioFileClip = moviepy.AudioFileClip
            ImageClip = moviepy.ImageClip
            concatenate_videoclips = moviepy.concatenate_videoclips
    except ImportError as e:
        print(f"Missing moviepy: {e}")
        print("Please install moviepy: pip install moviepy")
        sys.exit(1)

try:
    from mutagen import File as AudioFile
except ImportError as e:
    print(f"Missing mutagen: {e}")
    print("Please install mutagen: pip install mutagen")
    sys.exit(1)


class SlideshowGenerator:
    """Generate slideshow videos from images and audio."""
    
    def __init__(self, output_resolution: Tuple[int, int] = (1920, 1080)):
        self.output_resolution = output_resolution
        self.supported_image_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        self.supported_audio_formats = {'.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac'}
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds."""
        try:
            audio_file = AudioFile(audio_path)
            if audio_file is not None and hasattr(audio_file, 'info'):
                return float(audio_file.info.length)
        except Exception:
            pass
        
        # Fallback using moviepy
        try:
            audio = mp.AudioFileClip(audio_path)
            duration = audio.duration
            audio.close()
            return duration
        except Exception as e:
            raise ValueError(f"Could not determine audio duration: {e}")
    
    def get_image_files(self, image_dir: str) -> List[str]:
        """Get all supported image files from directory."""
        image_files = []
        image_path = Path(image_dir)
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image directory not found: {image_dir}")
        
        for file_path in image_path.iterdir():
            if file_path.suffix.lower() in self.supported_image_formats:
                image_files.append(str(file_path))
        
        if not image_files:
            raise ValueError(f"No supported image files found in {image_dir}")
        
        # Sort files naturally
        image_files.sort()
        return image_files
    
    def resize_image_to_fit(self, image_path: str, target_size: Tuple[int, int]) -> Image.Image:
        """Resize image to fit target size while maintaining aspect ratio."""
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate scaling to fit within target size
            img_ratio = img.width / img.height
            target_ratio = target_size[0] / target_size[1]
            
            if img_ratio > target_ratio:
                # Image is wider, scale by width
                new_width = target_size[0]
                new_height = int(target_size[0] / img_ratio)
            else:
                # Image is taller, scale by height
                new_height = target_size[1]
                new_width = int(target_size[1] * img_ratio)
            
            # Resize image
            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create canvas with target size and center the image
            canvas = Image.new('RGB', target_size, (0, 0, 0))
            x_offset = (target_size[0] - new_width) // 2
            y_offset = (target_size[1] - new_height) // 2
            canvas.paste(resized, (x_offset, y_offset))
            
            return canvas
    
    def create_slideshow_video(self, image_dir: str, audio_path: str = None, output_path: str = None, 
                             transition_duration: float = 0.5, progress_callback=None, 
                             silent_mode: bool = False, image_duration: float = 3.0) -> None:
        """Create slideshow video from images and optionally audio.
        
        Args:
            image_dir: Directory containing images
            audio_path: Path to audio file (optional if silent_mode=True)
            output_path: Path for output video
            transition_duration: Duration of transitions in seconds
            progress_callback: Optional callback function for progress updates
            silent_mode: If True, create video without audio
            image_duration: Duration per image in seconds (for silent mode)
        """
        
        import time
        start_time = time.time()
        
        print("Starting slideshow generation...")
        if progress_callback:
            progress_callback("Starting slideshow generation...", 5)
        
        # Validate inputs
        if not silent_mode and not audio_path:
            raise ValueError("Audio path is required when not in silent mode")
        
        if not silent_mode and not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Get audio duration and image files
        if not silent_mode:
            if progress_callback:
                progress_callback("Getting audio duration...", 10)
            audio_duration = self.get_audio_duration(audio_path)
        else:
            if progress_callback:
                progress_callback("Calculating video duration for silent mode...", 10)
            audio_duration = None
        
        if progress_callback:
            progress_callback("Finding image files...", 15)
        image_files = self.get_image_files(image_dir)
        
        print(f"Audio duration: {audio_duration:.2f} seconds ({audio_duration/60:.1f} minutes)" if not silent_mode else f"Silent mode: Using {image_duration}s per image")
        print(f"Found {len(image_files)} images")
        
        # Calculate timing
        num_images = len(image_files)
        if not silent_mode:
            time_per_image = audio_duration / num_images
            total_video_duration = audio_duration
        else:
            time_per_image = image_duration
            total_video_duration = num_images * image_duration
        
        print(f"Each image will be displayed for {time_per_image:.1f} seconds")
        if silent_mode:
            print(f"Total video duration: {total_video_duration:.1f} seconds ({total_video_duration/60:.1f} minutes)")
        
        # Create temporary directory for processed images
        with tempfile.TemporaryDirectory() as temp_dir:
            if progress_callback:
                progress_callback("Processing images...", 20)
            print("Processing images...")
            processed_images = []
            
            for i, img_path in enumerate(image_files):
                progress = 20 + (i / num_images) * 30  # 20-50% for image processing
                if progress_callback:
                    progress_callback(f"Processing image {i+1}/{num_images}: {os.path.basename(img_path)}", progress)
                print(f"Processing image {i+1}/{num_images}: {os.path.basename(img_path)}")
                
                # Resize and save processed image
                processed_img = self.resize_image_to_fit(img_path, self.output_resolution)
                temp_img_path = os.path.join(temp_dir, f"img_{i:04d}.jpg")
                processed_img.save(temp_img_path, "JPEG", quality=95)
                processed_images.append(temp_img_path)
            
            if progress_callback:
                progress_callback("Creating video clips...", 50)
            print("Creating video clips...")
            
            # Create video clips for each image
            clips = []
            for i, img_path in enumerate(processed_images):
                progress = 50 + (i / num_images) * 20  # 50-70% for clip creation
                if progress_callback:
                    progress_callback(f"Creating clip {i+1}/{num_images}", progress)
                
                # Create image clip
                img_clip = mp.ImageClip(img_path, duration=time_per_image)
                
                # Add crossfade transition (except for the first image)
                if i > 0 and transition_duration > 0:
                    img_clip = img_clip.crossfadein(transition_duration)
                
                clips.append(img_clip)
            
            if progress_callback:
                progress_callback("Concatenating video clips...", 70)
            print("Concatenating video clips...")
            
            # Concatenate all clips
            video = mp.concatenate_videoclips(clips, method="compose")
            
            if not silent_mode:
                # Load and attach audio
                if progress_callback:
                    progress_callback("Loading audio...", 75)
                print("Loading audio...")
                audio = mp.AudioFileClip(audio_path)
                
                # Trim video to match audio duration exactly
                if progress_callback:
                    progress_callback("Synchronizing video with audio...", 80)
                if video.duration > audio_duration:
                    video = video.subclip(0, audio_duration)
                elif video.duration < audio_duration:
                    # Loop video if it's shorter than audio
                    loops_needed = math.ceil(audio_duration / video.duration)
                    video = mp.concatenate_videoclips([video] * loops_needed)
                    video = video.subclip(0, audio_duration)
                
                # Set audio
                final_video = video.set_audio(audio)
            else:
                # Silent mode - no audio processing needed
                if progress_callback:
                    progress_callback("Preparing silent video...", 75)
                print("Creating silent video...")
                final_video = video
            
            if progress_callback:
                progress_callback("Rendering final video...", 85)
            print(f"Rendering final video to: {output_path}")
            
            # Write final video
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            print(f"Video rendering completed.")
            
            # Clean up resources immediately
            print("Cleaning up resources...")
            final_video.close()
            if not silent_mode:
                audio.close()
            video.close()
            for clip in clips:
                clip.close()
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Verify file was created
            if os.path.exists(output_path):
                end_time = time.time()
                total_time = end_time - start_time
                minutes = int(total_time // 60)
                seconds = int(total_time % 60)
                
                file_size = os.path.getsize(output_path)
                if progress_callback:
                    progress_callback(f"🎉 SUCCESS! Video created ({file_size / (1024*1024):.1f} MB) - Time: {minutes:02d}:{seconds:02d}", 100)
                print("\n" + "=" * 70)
                print("🎉 SLIDESHOW VIDEO GENERATION COMPLETED SUCCESSFULLY!")
                print("=" * 70)
                print(f"✅ Video file created: {output_path}")
                print(f"📊 File size: {file_size / (1024*1024):.1f} MB")
                print(f"⏱️  Render time: {minutes:02d}:{seconds:02d} ({total_time:.1f} seconds)")
                print(f"🎬 Video is ready to play and share!")
                print("=" * 70)
            else:
                raise Exception("Video file was not created successfully")
            
            print(f"\n🎥 Your podcast slideshow video is now complete and ready to use!")
            print(f"📁 Location: {output_path}")
            print(f"⏱️  Total generation time: {minutes:02d}:{seconds:02d}")


def main():
    """Main function to run the slideshow generator."""
    parser = argparse.ArgumentParser(
        description="Generate podcast slideshow videos from images and audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python slideshow_generator.py images/ podcast.mp3 -o slideshow.mp4
  python slideshow_generator.py photos/ audio.wav -o output.mp4 --resolution 1280x720
  python slideshow_generator.py pics/ sound.m4a -o video.mp4 --transition 1.0
  python slideshow_generator.py images/ --silent -o silent_slideshow.mp4 --image-duration 5.0
  python slideshow_generator.py photos/ --silent --resolution 1280x720 -o quick_slideshow.mp4
        """
    )
    
    parser.add_argument('image_dir', help='Directory containing images')
    parser.add_argument('audio_file', nargs='?', help='Audio file for the podcast (optional if --silent)')
    parser.add_argument('-o', '--output', default='slideshow.mp4', 
                       help='Output video file (default: slideshow.mp4)')
    parser.add_argument('--resolution', default='1920x1080',
                       help='Output resolution (default: 1920x1080)')
    parser.add_argument('--transition', type=float, default=0.5,
                       help='Transition duration in seconds (default: 0.5)')
    parser.add_argument('--silent', action='store_true',
                       help='Create silent slideshow without audio')
    parser.add_argument('--image-duration', type=float, default=3.0,
                       help='Duration per image in seconds for silent mode (default: 3.0)')
    
    args = parser.parse_args()
    
    # Parse resolution
    try:
        width, height = map(int, args.resolution.split('x'))
        resolution = (width, height)
    except ValueError:
        print("Error: Resolution must be in format WIDTHxHEIGHT (e.g., 1920x1080)")
        sys.exit(1)
    
    # Validate inputs
    if not os.path.exists(args.image_dir):
        print(f"Error: Image directory not found: {args.image_dir}")
        sys.exit(1)
    
    if not args.silent and not args.audio_file:
        print("Error: Audio file is required when not using --silent mode")
        sys.exit(1)
    
    if not args.silent and not os.path.exists(args.audio_file):
        print(f"Error: Audio file not found: {args.audio_file}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Create slideshow generator
        generator = SlideshowGenerator(output_resolution=resolution)
        
        # Generate slideshow
        generator.create_slideshow_video(
            image_dir=args.image_dir,
            audio_path=args.audio_file if not args.silent else None,
            output_path=args.output,
            transition_duration=args.transition,
            silent_mode=args.silent,
            image_duration=args.image_duration
        )
        
        print(f"\nSuccess! Slideshow video saved to: {args.output}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()