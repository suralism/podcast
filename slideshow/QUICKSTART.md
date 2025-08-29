# 🎬 Quick Start Guide - Podcast Slideshow Generator

## ✅ What's Included

Your slideshow generator is now ready! Here's what was created:

- `slideshow_generator.py` - Main program
- `requirements.txt` - Dependencies list
- `create_sample_images.py` - Creates test images
- `test_setup.py` - Setup and test script
- `setup.bat` - Windows batch setup script
- `README.md` - Complete documentation

## 🚀 Quick Setup (Choose Your Method)

### Method 1: GUI Version (Easy! 😊)

**Windows (with virtual environment):**
```bash
# If you're using a virtual environment (.venv)
setup_venv.bat

# Then launch GUI
python slideshow_gui.py
# OR
python launcher.py
```

**Windows (global installation):**
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

The GUI will:
- Auto-install dependencies
- Provide easy browse buttons
- Show progress and status
- Create sample images for testing

### Method 2: Command Line (Advanced)

**Step 1:** Install Dependencies
```bash
pip install -r requirements.txt
```

**Step 2:** Create Test Images (Optional)
```bash
python create_sample_images.py
```

**Step 3:** Run the Generator
```bash
python slideshow_generator.py <image_folder> <audio_file> -o <output_file>
```

## 📝 Example Usage

### GUI Method (Recommended for beginners)
1. **Launch:** Double-click `launch_gui.bat` (Windows) or run `python launcher.py`
2. **Browse:** Click "Browse" buttons to select:
   - Image folder (with your 20 images)
   - Audio file (your ~20-minute podcast)
   - Output location for the video
3. **Settings:** Adjust resolution and transition time if needed
4. **Generate:** Click "🎦 Generate Slideshow" and wait!

### Command Line Method
```bash
# Create slideshow with your images and audio
python slideshow_generator.py my_images/ podcast.mp3 -o slideshow.mp4

# With custom settings
python slideshow_generator.py photos/ audio.wav -o video.mp4 --resolution 1280x720 --transition 1.0

# Using sample images (after running create_sample_images.py)
python slideshow_generator.py sample_images/ your_audio.mp3 -o output/test.mp4
```

## 📁 File Organization

```
your-project/
├── images/              # Put your 20 images here
│   ├── photo1.jpg
│   ├── photo2.png
│   └── ...
├── audio/               # Put your podcast audio here
│   └── podcast.mp3      # ~20 minutes
└── output/              # Generated videos appear here
    └── slideshow.mp4
```

## ⚡ Automated Setup (Windows)

Just double-click `setup.bat` and it will:
1. Install all dependencies
2. Create sample images for testing
3. Show you the next steps

## 🎯 For Your 20-Minute Podcast

1. **Prepare 20 images** (JPG, PNG, etc.)
2. **Have your ~20-minute audio file** (MP3, WAV, M4A, etc.)
3. **Run the command:**
   ```bash
   python slideshow_generator.py images/ podcast.mp3 -o my_podcast_slideshow.mp4
   ```

The program will automatically:
- Calculate timing (1 minute per image for 20 images/20 minutes)
- Resize images to fit video dimensions
- Add smooth transitions
- Sync with your audio
- Output high-quality MP4

## 🛠️ Troubleshooting

**"FFmpeg not found"**: Install FFmpeg from https://ffmpeg.org/ or use `choco install ffmpeg`

**Import errors**: Run `pip install -r requirements.txt`

**No images found**: Check your image folder path and file extensions

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. Run `python test_setup.py` to verify installation
3. Try with sample images first: `python create_sample_images.py`

---

**You're all set! 🎉 Create amazing podcast slideshows! 🎙️📺**