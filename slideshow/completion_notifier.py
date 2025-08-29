#!/usr/bin/env python3
"""
Completion Notification Helper
Provides visual and audio feedback for completed operations.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox
import threading
import time

class CompletionNotifier:
    """Helper class for completion notifications."""
    
    def __init__(self):
        self.sound_available = self._check_sound_support()
    
    def _check_sound_support(self):
        """Check if system sound is available."""
        try:
            if sys.platform == "win32":
                import winsound
                return True
            else:
                # For Linux/Mac, you could use other sound libraries
                return False
        except ImportError:
            return False
    
    def play_completion_sound(self):
        """Play system completion sound."""
        if not self.sound_available:
            return
        
        try:
            if sys.platform == "win32":
                import winsound
                # Play multiple beeps for success
                for _ in range(3):
                    winsound.MessageBeep(winsound.MB_OK)
                    time.sleep(0.1)
        except Exception:
            pass  # Ignore sound errors
    
    def flash_window(self, window):
        """Flash the window to get user attention."""
        try:
            if sys.platform == "win32":
                # Flash window on Windows
                import ctypes
                ctypes.windll.user32.FlashWindow(window.winfo_id(), True)
                time.sleep(0.5)
                ctypes.windll.user32.FlashWindow(window.winfo_id(), True)
        except Exception:
            pass  # Ignore if flashing not available
    
    def show_completion_notification(self, title, message, details=None):
        """Show a prominent completion notification."""
        # Prepare the message
        full_message = message
        if details:
            full_message += f"\\n\\n{details}"
        
        # Play sound in background
        if self.sound_available:
            threading.Thread(target=self.play_completion_sound, daemon=True).start()
        
        # Show dialog
        return messagebox.showinfo(title, full_message)
    
    def show_completion_with_options(self, title, message, options_message, details=None):
        """Show completion notification with yes/no options."""
        # Prepare the message
        full_message = message
        if details:
            full_message += f"\\n\\n{details}"
        full_message += f"\\n\\n{options_message}"
        
        # Play sound in background
        if self.sound_available:
            threading.Thread(target=self.play_completion_sound, daemon=True).start()
        
        # Show dialog with options
        return messagebox.askyesno(title, full_message)

# Global instance
notifier = CompletionNotifier()

def notify_completion(title, message, details=None):
    """Quick function to show completion notification."""
    return notifier.show_completion_notification(title, message, details)

def notify_completion_with_options(title, message, options_message, details=None):
    """Quick function to show completion notification with options."""
    return notifier.show_completion_with_options(title, message, options_message, details)

if __name__ == "__main__":
    # Test the notification system
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    print("Testing completion notification...")
    
    # Test basic notification
    notify_completion(
        "🎉 Test Complete!",
        "This is a test of the completion notification system.",
        "Details: All systems working correctly!"
    )
    
    # Test notification with options
    result = notify_completion_with_options(
        "🎉 Generation Complete!",
        "Your slideshow video has been created successfully!",
        "Would you like to open the output folder?",
        "File: test_video.mp4\\nSize: 15.3 MB"
    )
    
    print(f"User chose: {'Yes' if result else 'No'}")
    
    root.destroy()