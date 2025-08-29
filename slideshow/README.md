# Podcast Slideshow Generator

A Python tool to create MP4 slideshow videos by combining images with podcast audio files. Perfect for creating visual content for audio podcasts, presentations, or educational content.

## Features

- ✅ **Easy-to-use GUI interface** with browse buttons and progress tracking
- ✅ **Command-line interface** for advanced users and automation
- ✅ Combines multiple images with audio to create MP4 videos
- ✅ Automatically calculates timing based on audio duration
- ✅ Supports various image formats (JPG, PNG, BMP, TIFF, WebP)
- ✅ Supports various audio formats (MP3, WAV, M4A, AAC, OGG, FLAC)
- ✅ Automatic image resizing and aspect ratio preservation
- ✅ Smooth crossfade transitions between images
- ✅ Customizable output resolution
- ✅ High-quality video output with H.264 encoding

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg (required by moviepy)

### Install FFmpeg

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract and add to your system PATH
3. Or install via chocolatey: `choco install ffmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### GUI Method (Recommended)

**Windows:**
```bash
# Double-click the batch file
launch_gui.bat
```

**All Platforms:**
```bash
python launcher.py
# OR directly:
python slideshow_gui.py
```

The GUI provides:
- 📁 Easy browse buttons for selecting files and folders
- ⚙️ Visual settings controls (resolution, transition duration)
- 📊 Real-time progress bar and status updates
- 📝 Activity log showing detailed progress
- 🖼️ Button to create sample images for testing
- 📂 Quick access to open output folder

### Command Line Method (Advanced)

#### Basic Usage

```bash
python slideshow_generator.py <image_directory> <audio_file> -o <output_file>
```

#### Examples

**Create a slideshow with default settings:**
```bash
python slideshow_generator.py images/ podcast.mp3 -o my_slideshow.mp4
```

**Custom resolution and transition:**
```bash
python slideshow_generator.py photos/ audio.wav -o slideshow.mp4 --resolution 1280x720 --transition 1.0
```

**Using different audio format:**
```bash
python slideshow_generator.py pictures/ episode.m4a -o output.mp4
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `image_dir` | Directory containing images (required) | - |
| `audio_file` | Audio file for the podcast (required) | - |
| `-o, --output` | Output video file | `slideshow.mp4` |
| `--resolution` | Output resolution (WxH) | `1920x1080` |
| `--transition` | Transition duration in seconds | `0.5` |

### Supported Formats

**Images:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

**Audio:**
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- AAC (.aac)
- OGG (.ogg)
- FLAC (.flac)

## File Organization

```
your-project/
├── images/                 # Put your images here
│   ├── image001.jpg
│   ├── image002.png
│   └── ...
├── audio/                  # Put your audio files here
│   └── podcast_episode.mp3
└── output/                 # Generated videos will be here
    └── slideshow.mp4
```

## How It Works

1. **Image Processing**: The program scans the image directory and sorts files naturally
2. **Timing Calculation**: Divides audio duration by number of images to calculate display time per image
3. **Image Resizing**: Automatically resizes images to fit the target resolution while maintaining aspect ratio
4. **Video Creation**: Creates video clips for each image with crossfade transitions
5. **Audio Sync**: Synchronizes the video with the audio track
6. **Output**: Renders the final MP4 file with H.264 video and AAC audio encoding

## Tips for Best Results

### Image Preparation
- Use high-quality images (at least 1080p for best results)
- Keep aspect ratios consistent for smoother transitions
- Name files in order (e.g., 001.jpg, 002.jpg) for proper sequencing
- Recommended: 16:9 aspect ratio images for standard video output

### Audio Preparation
- Use good quality audio files (at least 128kbps)
- Ensure audio levels are consistent
- Consider using audio editing software to normalize volume

### Performance Tips
- For large image collections, consider using lower resolution output first to test
- SSD storage will significantly improve processing speed
- Close other applications to free up memory during processing

## Example Workflow

1. **Prepare your content:**
   ```
   mkdir my_podcast_episode
   cd my_podcast_episode
   mkdir images audio output
   ```

2. **Add your files:**
   - Copy 15-25 images to the `images/` folder
   - Copy your podcast audio to the `audio/` folder

3. **Generate the slideshow:**
   ```bash
   python slideshow_generator.py images/ audio/episode.mp3 -o output/slideshow.mp4
   ```

4. **Review and share:**
   - The output video will be in the `output/` folder
   - Upload to YouTube, social media, or your preferred platform

## Troubleshooting

### Common Issues

**"FFmpeg not found" error:**
- Install FFmpeg and ensure it's in your system PATH
- Restart your terminal/command prompt after installation

**"No images found" error:**
- Check that image files are in the correct directory
- Ensure image files have supported extensions
- Verify file permissions

**Poor video quality:**
- Use higher resolution images
- Try different output resolution settings
- Ensure input images are not heavily compressed

**Audio sync issues:**
- Verify audio file is not corrupted
- Try converting audio to a different format first
- Check that audio duration is detected correctly

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify your image and audio files are in supported formats
3. Try with a smaller test set first
4. Check the console output for detailed error messages

## Advanced Usage

### Batch Processing Script

Create a batch script to process multiple episodes:

```python
import os
import subprocess

episodes = [
    ("episode1_images/", "episode1.mp3", "episode1_slideshow.mp4"),
    ("episode2_images/", "episode2.mp3", "episode2_slideshow.mp4"),
    # Add more episodes...
]

for img_dir, audio_file, output_file in episodes:
    cmd = [
        "python", "slideshow_generator.py",
        img_dir, audio_file,
        "-o", output_file,
        "--resolution", "1920x1080"
    ]
    subprocess.run(cmd)
```

## Requirements

See `requirements.txt` for the complete list of Python dependencies.

## License

This project is provided as-is for educational and personal use.

---

**Happy slideshow creating! 🎬🎙️**