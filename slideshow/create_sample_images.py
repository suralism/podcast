#!/usr/bin/env python3
"""
Sample Image Generator
Creates sample images for testing the slideshow generator.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_images(output_dir="sample_images", count=20):
    """Create sample images with numbers and colors."""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Image dimensions
    width, height = 1920, 1080
    
    # Colors for variety
    colors = [
        (255, 99, 132),   # Red
        (54, 162, 235),   # Blue
        (255, 205, 86),   # Yellow
        (75, 192, 192),   # Teal
        (153, 102, 255),  # Purple
        (255, 159, 64),   # Orange
        (199, 199, 199),  # Grey
        (83, 102, 255),   # Indigo
        (255, 99, 255),   # Pink
        (99, 255, 132),   # Green
    ]
    
    print(f"Creating {count} sample images in {output_dir}/")
    
    for i in range(count):
        # Create image with colored background
        color = colors[i % len(colors)]
        img = Image.new('RGB', (width, height), color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 120)
            small_font = ImageFont.truetype("arial.ttf", 60)
        except OSError:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 120)
                small_font = ImageFont.truetype("DejaVuSans.ttf", 60)
            except OSError:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
        
        # Draw slide number
        text = f"Slide {i+1:02d}"
        
        # Get text size and center it
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2 - 50
        
        # Draw white text with black outline
        outline_range = 3
        for dx in range(-outline_range, outline_range + 1):
            for dy in range(-outline_range, outline_range + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0))
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        
        # Add subtitle
        subtitle = f"Sample image for podcast slideshow"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=small_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (width - subtitle_width) // 2
        subtitle_y = y + text_height + 20
        
        # Draw subtitle with outline
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx != 0 or dy != 0:
                    draw.text((subtitle_x + dx, subtitle_y + dy), subtitle, font=small_font, fill=(0, 0, 0))
        draw.text((subtitle_x, subtitle_y), subtitle, font=small_font, fill=(255, 255, 255))
        
        # Save image
        filename = f"sample_{i+1:03d}.jpg"
        filepath = os.path.join(output_dir, filename)
        img.save(filepath, "JPEG", quality=95)
        print(f"Created: {filename}")

if __name__ == "__main__":
    create_sample_images()
    print("\nSample images created successfully!")
    print("You can now test the slideshow generator with these images.")