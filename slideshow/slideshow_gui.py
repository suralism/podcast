#!/usr/bin/env python3
"""
Podcast Slideshow Generator - GUI Version
A user-friendly graphical interface for creating slideshow videos.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import threading
from pathlib import Path
import subprocess

# Try to import the completion notifier
try:
    from completion_notifier import notify_completion_with_options
except ImportError:
    # Fallback if notifier not available
    def notify_completion_with_options(title, message, options_message, details=None):
        full_message = message
        if details:
            full_message += f"\n\n{details}"
        full_message += f"\n\n{options_message}"
        return messagebox.askyesno(title, full_message)

# Try to import the slideshow generator
try:
    from slideshow_generator import SlideshowGenerator
except ImportError as e:
    print(f"Error importing slideshow_generator: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    # Don't exit here, let the GUI handle it gracefully


class SlideshowGUI:
    """GUI for the Podcast Slideshow Generator."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Podcast Slideshow Generator")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.image_dir_var = tk.StringVar()
        self.audio_file_var = tk.StringVar()
        self.output_file_var = tk.StringVar()
        self.resolution_var = tk.StringVar(value="1920x1080")
        self.transition_var = tk.DoubleVar(value=0.5)
        self.silent_mode_var = tk.BooleanVar(value=False)
        self.image_duration_var = tk.DoubleVar(value=3.0)
        
        # Status variables
        self.is_generating = False
        self.should_stop = False
        self.generator = None
        self.start_time = None
        self.end_time = None
        
        self.create_widgets()
        self.center_window()
    
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎬 Podcast Slideshow Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Image Directory Section
        ttk.Label(main_frame, text="📁 Image Directory:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        ttk.Entry(main_frame, textvariable=self.image_dir_var, width=50).grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(main_frame, text="Browse", command=self.browse_image_dir).grid(
            row=2, column=2, sticky=tk.W)
        
        # Audio File Section
        ttk.Label(main_frame, text="🎵 Audio File:", font=("Arial", 10, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=(20, 5))
        
        ttk.Entry(main_frame, textvariable=self.audio_file_var, width=50).grid(
            row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(main_frame, text="Browse", command=self.browse_audio_file).grid(
            row=4, column=2, sticky=tk.W)
        
        # Output File Section
        ttk.Label(main_frame, text="💾 Output Video File:", font=("Arial", 10, "bold")).grid(
            row=5, column=0, sticky=tk.W, pady=(20, 5))
        
        ttk.Entry(main_frame, textvariable=self.output_file_var, width=50).grid(
            row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(main_frame, text="Browse", command=self.browse_output_file).grid(
            row=6, column=2, sticky=tk.W)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Settings", padding="15")
        settings_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        settings_frame.columnconfigure(1, weight=1)
        
        # Resolution
        ttk.Label(settings_frame, text="Resolution:").grid(row=0, column=0, sticky=tk.W, pady=5)
        resolution_combo = ttk.Combobox(settings_frame, textvariable=self.resolution_var,
                                       values=["1920x1080", "1280x720", "854x480", "640x360"],
                                       state="readonly", width=15)
        resolution_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Transition Duration
        ttk.Label(settings_frame, text="Transition Duration (seconds):").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        transition_spin = ttk.Spinbox(settings_frame, from_=0.0, to=5.0, increment=0.1,
                                     textvariable=self.transition_var, width=15)
        transition_spin.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Silent Mode Checkbox
        self.silent_checkbox = ttk.Checkbutton(settings_frame, text="Silent Mode (No Audio)",
                                              variable=self.silent_mode_var,
                                              command=self.toggle_silent_mode)
        self.silent_checkbox.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Image Duration (for silent mode)
        ttk.Label(settings_frame, text="Image Duration (seconds, silent mode):").grid(
            row=3, column=0, sticky=tk.W, pady=5)
        self.image_duration_spin = ttk.Spinbox(settings_frame, from_=1.0, to=30.0, increment=0.5,
                                              textvariable=self.image_duration_var, width=15,
                                              state="disabled")
        self.image_duration_spin.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=(30, 0))
        
        # Generate Button
        self.generate_btn = ttk.Button(button_frame, text="🎬 Generate Slideshow", 
                                      command=self.generate_slideshow,
                                      style="Accent.TButton")
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop Button (initially hidden)
        self.stop_btn = ttk.Button(button_frame, text="⏹️ Stop Generation", 
                                  command=self.stop_generation,
                                  state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create Sample Images Button
        ttk.Button(button_frame, text="🖼️ Create Sample Images", 
                  command=self.create_sample_images).pack(side=tk.LEFT, padx=(0, 10))
        
        # Open Output Folder Button
        ttk.Button(button_frame, text="📂 Open Output Folder", 
                  command=self.open_output_folder).pack(side=tk.LEFT)
        
        # Progress Frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready to generate slideshow")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Elapsed Time Label
        self.elapsed_var = tk.StringVar(value="")
        self.elapsed_label = ttk.Label(progress_frame, textvariable=self.elapsed_var, 
                                      font=("Arial", 9), foreground="blue")
        self.elapsed_label.grid(row=2, column=0, sticky=tk.W, pady=(2, 0))
        
        # Completion Status Label (initially hidden)
        self.completion_var = tk.StringVar(value="")
        self.completion_label = ttk.Label(progress_frame, textvariable=self.completion_var, 
                                         font=("Arial", 10, "bold"), foreground="green")
        self.completion_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        
        # Log Text Area
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log", padding="10")
        log_frame.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Configure main_frame to expand
        main_frame.rowconfigure(10, weight=1)
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for log
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Set default output file
        self.output_file_var.set(os.path.join(os.getcwd(), "output", "slideshow.mp4"))
    
    def log_message(self, message):
        """Add message to log area."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def toggle_silent_mode(self):
        """Toggle silent mode controls."""
        if self.silent_mode_var.get():
            # Silent mode enabled
            self.audio_file_var.set("")
            self.image_duration_spin.configure(state="normal")
            # Update labels to indicate optional audio
            for widget in self.root.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'winfo_children'):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, ttk.Label) and "Audio File:" in str(grandchild.cget('text')):
                                    grandchild.configure(text="🎵 Audio File (Optional in Silent Mode):")
        else:
            # Silent mode disabled
            self.image_duration_spin.configure(state="disabled")
            # Restore original audio label
            for widget in self.root.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'winfo_children'):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, ttk.Label) and "Optional" in str(grandchild.cget('text')):
                                    grandchild.configure(text="🎵 Audio File:")
    
    def update_elapsed_time(self):
        """Update the elapsed time display."""
        if self.start_time and self.is_generating:
            import time
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.elapsed_var.set(f"⏱️ Elapsed time: {minutes:02d}:{seconds:02d}")
            
            # Schedule next update if still generating
            if self.is_generating:
                self.root.after(1000, self.update_elapsed_time)
    
    def browse_image_dir(self):
        """Browse for image directory."""
        directory = filedialog.askdirectory(title="Select Image Directory")
        if directory:
            self.image_dir_var.set(directory)
    
    def browse_audio_file(self):
        """Browse for audio file."""
        filetypes = [
            ("Audio files", "*.mp3 *.wav *.m4a *.aac *.ogg *.flac"),
            ("MP3 files", "*.mp3"),
            ("WAV files", "*.wav"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(title="Select Audio File", filetypes=filetypes)
        if filename:
            self.audio_file_var.set(filename)
    
    def browse_output_file(self):
        """Browse for output file location."""
        filetypes = [("MP4 files", "*.mp4"), ("All files", "*.*")]
        filename = filedialog.asksaveasfilename(title="Save Video As", 
                                               defaultextension=".mp4",
                                               filetypes=filetypes)
        if filename:
            self.output_file_var.set(filename)
    
    def create_sample_images(self):
        """Create sample images for testing."""
        def run_creation():
            try:
                self.log_message("Creating sample images...")
                self.status_var.set("Creating sample images...")
                
                # Run the sample image creation script
                result = subprocess.run([sys.executable, "create_sample_images.py"], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log_message("Sample images created successfully!")
                    self.status_var.set("Sample images created successfully")
                    
                    # Set the sample images directory
                    sample_dir = os.path.join(os.getcwd(), "sample_images")
                    if os.path.exists(sample_dir):
                        self.image_dir_var.set(sample_dir)
                        self.log_message(f"Image directory set to: {sample_dir}")
                else:
                    self.log_message(f"Error creating sample images: {result.stderr}")
                    self.status_var.set("Error creating sample images")
                    
            except Exception as e:
                self.log_message(f"Error: {str(e)}")
                self.status_var.set("Error creating sample images")
        
        # Run in separate thread
        threading.Thread(target=run_creation, daemon=True).start()
    
    def open_output_folder(self):
        """Open the output folder in file explorer."""
        output_path = self.output_file_var.get()
        if output_path:
            output_dir = os.path.dirname(output_path)
        else:
            output_dir = os.path.join(os.getcwd(), "output")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Open folder in file explorer
        if sys.platform == "win32":
            os.startfile(output_dir)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", output_dir])
        else:  # Linux
            subprocess.run(["xdg-open", output_dir])
    
    def validate_inputs(self):
        """Validate user inputs."""
        if not self.image_dir_var.get():
            messagebox.showerror("Error", "Please select an image directory")
            return False
        
        if not os.path.exists(self.image_dir_var.get()):
            messagebox.showerror("Error", "Image directory does not exist")
            return False
        
        # Audio validation only if not in silent mode
        if not self.silent_mode_var.get():
            if not self.audio_file_var.get():
                messagebox.showerror("Error", "Please select an audio file or enable Silent Mode")
                return False
            
            if not os.path.exists(self.audio_file_var.get()):
                messagebox.showerror("Error", "Audio file does not exist")
                return False
        
        if not self.output_file_var.get():
            messagebox.showerror("Error", "Please specify an output file")
            return False
        
        return True
    
    def stop_generation(self):
        """Stop the current generation process."""
        if self.is_generating:
            self.should_stop = True
            self.log_message("Stopping generation...")
            self.status_var.set("Stopping...")
    
    def generate_slideshow(self):
        """Generate the slideshow video."""
        if self.is_generating:
            messagebox.showwarning("Warning", "Generation is already in progress")
            return
        
        if not self.validate_inputs():
            return
        
        def run_generation():
            try:
                import time
                self.start_time = time.time()
                self.end_time = None
                self.is_generating = True
                self.should_stop = False
                self.generate_btn.configure(state="disabled")
                self.stop_btn.configure(state="normal")
                self.progress_var.set(0)
                
                # Clear log and status
                self.log_text.delete(1.0, tk.END)
                self.completion_var.set("")  # Clear previous completion status
                self.elapsed_var.set("⏱️ Elapsed time: 00:00")
                
                # Start elapsed time updates
                self.update_elapsed_time()
                
                self.log_message("Starting slideshow generation...")
                self.status_var.set("Initializing...")
                self.root.update_idletasks()
                
                # Parse resolution
                width, height = map(int, self.resolution_var.get().split('x'))
                resolution = (width, height)
                
                # Create generator with progress callback
                self.generator = SlideshowGenerator(output_resolution=resolution)
                
                # Create output directory if needed
                output_dir = os.path.dirname(self.output_file_var.get())
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    self.log_message(f"Created output directory: {output_dir}")
                
                # Update progress
                self.progress_var.set(5)
                self.status_var.set("Checking files...")
                self.root.update_idletasks()
                
                # Log input parameters
                self.log_message(f"Image directory: {self.image_dir_var.get()}")
                if not self.silent_mode_var.get():
                    self.log_message(f"Audio file: {self.audio_file_var.get()}")
                else:
                    self.log_message(f"Silent mode: No audio, {self.image_duration_var.get()}s per image")
                self.log_message(f"Output file: {self.output_file_var.get()}")
                self.log_message(f"Resolution: {self.resolution_var.get()}")
                self.log_message(f"Transition: {self.transition_var.get()}s")
                
                self.progress_var.set(10)
                self.status_var.set("Getting audio duration...")
                self.root.update_idletasks()
                
                # Get audio duration
                try:
                    audio_duration = self.generator.get_audio_duration(self.audio_file_var.get())
                    self.log_message(f"Audio duration: {audio_duration:.1f} seconds ({audio_duration/60:.1f} minutes)")
                except Exception as e:
                    self.log_message(f"Warning: Could not get audio duration - {e}")
                    audio_duration = None
                
                self.progress_var.set(15)
                self.status_var.set("Getting image files...")
                self.root.update_idletasks()
                
                # Get image files
                try:
                    image_files = self.generator.get_image_files(self.image_dir_var.get())
                    self.log_message(f"Found {len(image_files)} images")
                    if audio_duration:
                        time_per_image = audio_duration / len(image_files)
                        self.log_message(f"Each image will display for {time_per_image:.1f} seconds")
                except Exception as e:
                    raise ValueError(f"Error getting image files: {e}")
                
                self.progress_var.set(20)
                self.status_var.set("Processing images and creating video...")
                self.root.update_idletasks()
                
                # Generate slideshow with progress updates
                self.log_message("Creating slideshow video...")
                self.log_message("This may take several minutes depending on the number of images and video length.")
                
                # Call the main generation function with progress callback
                def progress_callback(message, progress):
                    if self.should_stop:
                        raise InterruptedError("Generation was cancelled by user")
                    self.log_message(message)
                    self.progress_var.set(progress)
                    self.status_var.set(message)
                    self.root.update_idletasks()
                
                self.generator.create_slideshow_video(
                    image_dir=self.image_dir_var.get(),
                    audio_path=self.audio_file_var.get() if not self.silent_mode_var.get() else None,
                    output_path=self.output_file_var.get(),
                    transition_duration=self.transition_var.get(),
                    progress_callback=progress_callback,
                    silent_mode=self.silent_mode_var.get(),
                    image_duration=self.image_duration_var.get()
                )
                
                # Final progress updates
                self.progress_var.set(95)
                self.status_var.set("Finalizing video file...")
                self.root.update_idletasks()
                
                # Give time for file operations to complete and flush buffers
                import time
                time.sleep(3)  # Increased wait time for file system sync
                
                # Force final resource cleanup
                import gc
                gc.collect()
                time.sleep(1)  # Additional time for cleanup
                
                # Verify output file exists and is accessible
                max_retries = 5
                file_ready = False
                file_size = 0  # Initialize file_size variable
                for attempt in range(max_retries):
                    try:
                        if os.path.exists(self.output_file_var.get()):
                            # Try to get file size to ensure file is not locked
                            file_size = os.path.getsize(self.output_file_var.get()) / (1024 * 1024)  # MB
                            if file_size > 0:  # Ensure file has content
                                file_ready = True
                                break
                        time.sleep(1)  # Wait before retry
                    except (OSError, PermissionError):
                        time.sleep(1)  # File might be locked, wait and retry
                
                if not file_ready:
                    raise Exception("Output file was not created successfully or is not accessible")
                
                # Calculate total generation time
                import time
                self.end_time = time.time()
                total_time = self.end_time - self.start_time
                total_minutes = int(total_time // 60)
                total_seconds = int(total_time % 60)
                time_str = f"{total_minutes:02d}:{total_seconds:02d}"
                
                # Final completion updates
                self.progress_var.set(100)
                self.status_var.set("🎉 VIDEO RENDERING COMPLETED SUCCESSFULLY!")
                self.elapsed_var.set(f"✅ Total render time: {time_str} ({total_time:.1f} seconds)")
                self.root.update_idletasks()
                
                # Log completion details
                self.log_message("\n" + "=" * 60)
                self.log_message("🎉 VIDEO RENDERING COMPLETED SUCCESSFULLY!")
                self.log_message("=" * 60)
                self.log_message(f"✅ Video file created: {os.path.basename(self.output_file_var.get())}")
                self.log_message(f"📁 Location: {self.output_file_var.get()}")
                self.log_message(f"📊 File size: {file_size:.1f} MB")
                self.log_message(f"⏱️  Render time: {time_str} ({total_time:.1f} seconds)")
                self.log_message(f"⏱️  Ready to play!")
                self.log_message("\n🎬 Your podcast slideshow video is now ready to use!")
                
                # Flash the progress bar to indicate completion
                for i in range(3):
                    self.progress_bar.configure(style="Success.Horizontal.TProgressbar")
                    self.root.update_idletasks()
                    time.sleep(0.3)
                    self.progress_bar.configure(style="TProgressbar")
                    self.root.update_idletasks()
                    time.sleep(0.3)
                
                # Final success style
                self.progress_bar.configure(style="Success.Horizontal.TProgressbar")
                
                # Set persistent completion status
                self.completion_var.set(f"🎉 COMPLETED! Video ready: {os.path.basename(self.output_file_var.get())} ({file_size:.1f} MB) - Time: {time_str}")
                
                # Show completion notification with sound (if available)
                def show_completion_notification():
                    # Use enhanced notification system
                    result = notify_completion_with_options(
                        "🎉 Slideshow Completed Successfully!",
                        f"🎥 Your podcast slideshow video is ready!",
                        "Would you like to open the output folder?",
                        f"📁 File: {os.path.basename(self.output_file_var.get())}\n"
                        f"📊 Size: {file_size:.1f} MB\n"
                        f"⏱️  Render time: {time_str}\n"
                        f"📂 Location: {os.path.dirname(self.output_file_var.get())}\n"
                        f"🎬 The video is ready to play and share!"
                    )
                    
                    if result:  # User clicked Yes
                        self.open_output_folder()
                
                # Delay notification to ensure all UI updates are complete
                self.root.after(1000, show_completion_notification)
                
            except InterruptedError as e:
                import time
                if self.start_time:
                    elapsed_total = time.time() - self.start_time
                    minutes = int(elapsed_total // 60)
                    seconds = int(elapsed_total % 60)
                    self.elapsed_var.set(f"⛔ Cancelled after {minutes:02d}:{seconds:02d}")
                
                self.log_message(f"\n=== GENERATION CANCELLED ===")
                self.log_message(f"Generation was stopped by user")
                self.status_var.set("Generation cancelled")
                self.completion_var.set("⛔ Generation was cancelled by user")
                self.progress_var.set(0)
                messagebox.showinfo("Cancelled", "Generation was cancelled by user")
                
            except Exception as e:
                import time
                if self.start_time:
                    elapsed_total = time.time() - self.start_time
                    minutes = int(elapsed_total // 60)
                    seconds = int(elapsed_total % 60)
                    self.elapsed_var.set(f"❌ Failed after {minutes:02d}:{seconds:02d}")
                
                self.log_message(f"\n=== ERROR OCCURRED ===")
                self.log_message(f"Error: {str(e)}")
                self.status_var.set("Error occurred during generation")
                self.completion_var.set(f"❌ ERROR: {str(e)[:50]}..." if len(str(e)) > 50 else f"❌ ERROR: {str(e)}")
                self.progress_var.set(0)
                messagebox.showerror("Error", f"An error occurred during generation:\n\n{str(e)}")
                
            finally:
                self.is_generating = False
                self.should_stop = False
                self.generate_btn.configure(state="normal")
                self.stop_btn.configure(state="disabled")
                # Force garbage collection to help with file cleanup
                import gc
                gc.collect()
        
        # Run in separate thread to prevent GUI freezing
        threading.Thread(target=run_generation, daemon=True).start()


def main():
    """Main function to run the GUI."""
    # Check if required modules are available
    try:
        import slideshow_generator
    except ImportError:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Dependencies Missing", 
                           "Required dependencies are not installed.\n\n"
                           "Please run: pip install -r requirements.txt")
        return
    
    # Create and run the GUI
    root = tk.Tk()
    app = SlideshowGUI(root)
    
    # Set icon if available (optional)
    try:
        root.iconbitmap("icon.ico")  # Add an icon file if you have one
    except:
        pass
    
    root.mainloop()


if __name__ == "__main__":
    main()