import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import configparser
import sys

class ImageRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Renamer Tool")
        self.root.geometry("900x700")
        
        # Initialize variables
        self.image_files = []           # Current directory listing
        self.display_order = []         # Fixed order of images
        self.filename_map = {}          # Maps display indexes to current filenames
        self.current_index = 0
        self.image_dir = ""
        self.names = []
        self.original_names = []
        self.default_dir = ""
        self.used_names = set()
        self.name_buttons = {}          # Dictionary to store references to buttons
        
        # Load configuration
        self.load_config()
        
        # Create GUI elements
        self.create_widgets()
        
        # Try to automatically load the namelist
        self.auto_load_namelist()
        
    def load_config(self):
        """Load configuration from config.ini file"""
        # Get the directory of the script or executable
        if getattr(sys, 'frozen', False):
            # If running as compiled executable
            app_dir = os.path.dirname(sys.executable)
        else:
            # If running as script
            app_dir = os.path.dirname(os.path.abspath(__file__))
            
        config_path = os.path.join(app_dir, 'config.ini')
        
        if os.path.exists(config_path):
            try:
                config = configparser.ConfigParser()
                config.read(config_path)
                
                if 'Settings' in config and 'default_image_directory' in config['Settings']:
                    self.default_dir = config['Settings']['default_image_directory']
                    
                if 'Settings' in config and 'default_namelist' in config['Settings']:
                    default_namelist = config['Settings']['default_namelist']
                    default_namelist_path = os.path.join(app_dir, default_namelist)
                    if os.path.exists(default_namelist_path):
                        self.namelist_path = default_namelist_path
                    else:
                        self.namelist_path = os.path.join(app_dir, 'namelist.txt')
                else:
                    self.namelist_path = os.path.join(app_dir, 'namelist.txt')
            except Exception as e:
                print(f"Error loading config: {str(e)}")
                self.namelist_path = os.path.join(app_dir, 'namelist.txt')
                
    def auto_load_namelist(self):
        """Try to automatically load namelist.txt from program directory"""
        if os.path.exists(self.namelist_path):
            if self.load_name_list_from_file(self.namelist_path):
                # Update button text if successful
                if self.names:
                    self.load_names_btn.config(text="Reload Name List")
    
    def create_widgets(self):
        # Top frame for controls
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Button to select directory
        select_btn = tk.Button(top_frame, text="Select Image Directory", command=self.select_directory)
        select_btn.pack(side=tk.LEFT, padx=5)
        
        # Display current directory
        self.dir_label = tk.Label(top_frame, text="No directory selected")
        self.dir_label.pack(side=tk.LEFT, padx=10)
        
        # Button to load name list
        self.load_names_btn = tk.Button(top_frame, text="Load Name List", command=self.select_name_list)
        self.load_names_btn.pack(side=tk.RIGHT, padx=5)
        
        # Current filename label
        self.filename_frame = tk.Frame(self.root)
        self.filename_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.filename_label = tk.Label(self.filename_frame, text="Current File Name is: None", font=("Arial", 10, "bold"))
        self.filename_label.pack(pady=5)
        
        # Main frame for image display and navigation
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left navigation button (previous)
        self.prev_btn = tk.Button(self.main_frame, text="◀", font=("Arial", 16),
                                command=self.previous_image)
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        
        # Image display label (center)
        self.image_label = tk.Label(self.main_frame)
        self.image_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right navigation button (next)
        self.next_btn = tk.Button(self.main_frame, text="▶", font=("Arial", 16),
                                command=self.skip_image)
        self.next_btn.pack(side=tk.RIGHT, padx=10)
        
        # Bottom frame for name selection
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Frame for name buttons (will be populated dynamically)
        self.name_buttons_frame = tk.Frame(self.bottom_frame)
        self.name_buttons_frame.pack(fill=tk.X, pady=5)
        
        # Skip button
        self.skip_btn = tk.Button(self.bottom_frame, text="Don't Rename", command=self.skip_image)
        self.skip_btn.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready. Select a directory and load a name list to begin.")
        self.status_label.pack(side=tk.BOTTOM, pady=5)
    
    def select_directory(self):
        """Open dialog to select directory containing images"""
        initial_dir = self.default_dir if os.path.exists(self.default_dir) else os.path.expanduser("~")
        
        self.image_dir = filedialog.askdirectory(
            title="Select Directory with Images",
            initialdir=initial_dir
        )
        
        if self.image_dir:
            self.dir_label.config(text=self.image_dir)
            self.load_images()
    
    def refresh_directory(self):
        """Refresh the list of image files from the directory"""
        if not self.image_dir:
            return False
            
        # Get the extensions from the original loading function
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
        
        # Refresh the list of files
        try:
            self.image_files = [f for f in os.listdir(self.image_dir) 
                               if os.path.isfile(os.path.join(self.image_dir, f)) 
                               and f.lower().endswith(image_extensions)]
            
            # Update filename map with current filenames
            self.update_filename_map()
            
            return True
        except Exception as e:
            print(f"Error refreshing directory: {str(e)}")
            return False
    
    def update_filename_map(self):
        """Update the filename map to reflect current filenames while preserving order"""
        if not self.display_order:
            return
            
        # Build a set of files in the directory for faster lookup
        files_set = set(self.image_files)
        
        # Update the filename map with current files
        for i, old_filename in enumerate(self.display_order):
            # If the old filename exists in the directory, keep it
            if old_filename in files_set:
                self.filename_map[i] = old_filename
            # Otherwise, look for renamed versions in the directory
            elif i in self.filename_map and self.filename_map[i] in files_set:
                # Current mapping is still valid
                continue
            else:
                # If we can't find the file, mark it as None
                self.filename_map[i] = None
    
    def load_images(self):
        """Load all image files from the selected directory"""
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
        self.image_files = [f for f in os.listdir(self.image_dir) 
                           if os.path.isfile(os.path.join(self.image_dir, f)) 
                           and f.lower().endswith(image_extensions)]
        
        if not self.image_files:
            messagebox.showinfo("No Images", "No image files found in the selected directory.")
            return
        
        # Save the original display order
        self.display_order = self.image_files.copy()
        
        # Initialize the filename map
        self.filename_map = {i: filename for i, filename in enumerate(self.display_order)}
        
        self.current_index = 0
        
        # Reset used names when loading new images
        self.used_names = set()
        
        # Reset button appearances
        self.reset_button_appearances()
        
        # Scan for existing filenames that match names in the list
        self.scan_existing_names()
        
        status_text = f"Found {len(self.image_files)} images."
        
        if not self.names:
            status_text += " Load a name list to begin."
        else:
            self.display_current_image()
            
        self.status_label.config(text=status_text)
    
    def scan_existing_names(self):
        """Scan directory for filenames that match names in the list"""
        if not self.image_dir or not self.names:
            return
            
        # Get all files in the directory
        all_files = os.listdir(self.image_dir)
        
        # Check each name in our list
        for name in self.original_names:
            # Look for files that start with this name followed by an extension
            for file in all_files:
                file_base = os.path.splitext(file)[0]
                # Check if file starts with name exactly, or name followed by underscore and digits
                if file_base == name or (file_base.startswith(name + "_") and file_base[len(name)+1:].isdigit()):
                    self.used_names.add(name)
                    break
        
        # Update button appearances
        self.update_button_appearances()
    
    def select_name_list(self):
        """Open dialog to select a name list file"""
        # Get the directory of the script or executable
        if getattr(sys, 'frozen', False):
            # If running as compiled executable
            app_dir = os.path.dirname(sys.executable)
        else:
            # If running as script
            app_dir = os.path.dirname(os.path.abspath(__file__))
            
        file_path = filedialog.askopenfilename(
            title="Select Name List File",
            initialdir=app_dir,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            self.load_name_list_from_file(file_path)
            
    def load_name_list_from_file(self, file_path):
        """Load a name list from a specific file path"""
        try:
            with open(file_path, 'r') as file:
                # Read names and strip whitespace
                self.names = [line.strip() for line in file if line.strip()]
                self.original_names = self.names.copy()
                
            if not self.names:
                messagebox.showwarning("Empty File", "The selected file doesn't contain any names.")
                return False
                
            # Reset used names when loading a new list
            self.used_names = set()
            
            # Create or update buttons
            self.create_name_buttons()
            
            # If images are loaded, scan for existing name matches
            if self.image_dir and self.image_files:
                self.scan_existing_names()
                self.display_current_image()
                
            self.status_label.config(text=f"Loaded {len(self.names)} names.")
            return True
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load name list: {str(e)}")
            return False
    
    def create_name_buttons(self):
        """Create all name buttons once and store references"""
        # Clear existing buttons
        for widget in self.name_buttons_frame.winfo_children():
            widget.destroy()
            
        # Clear button references
        self.name_buttons = {}
        
        # Create new buttons for each name
        column = 0
        row = 0
        button_width = 20  # Increased button width
        max_columns = 4    # Reduced columns to accommodate wider buttons
        
        # Sort names alphabetically
        sorted_names = sorted(self.original_names)
        
        for name in sorted_names:
            # Create a frame to hold each button to ensure it displays properly
            btn_frame = tk.Frame(self.name_buttons_frame)
            btn_frame.grid(row=row, column=column, padx=5, pady=5)
            
            # Create button
            btn = tk.Button(btn_frame, text=name, width=button_width,
                          command=lambda n=name: self.rename_image(n))
            btn.pack(fill=tk.BOTH, expand=True)
            
            # Store reference to button
            self.name_buttons[name] = btn
            
            column += 1
            if column >= max_columns:
                column = 0
                row += 1
                
    def reset_button_appearances(self):
        """Reset all buttons to default appearance"""
        for name, btn in self.name_buttons.items():
            btn.config(bg="SystemButtonFace", fg="black")  # Default colors
    
    def update_button_appearances(self):
        """Update button appearances based on used names"""
        for name in self.used_names:
            if name in self.name_buttons:
                self.name_buttons[name].config(bg="red", fg="white")
    
    def get_current_filename(self):
        """Get the current filename based on display order index"""
        if self.current_index in self.filename_map and self.filename_map[self.current_index] is not None:
            return self.filename_map[self.current_index]
        else:
            return None
    
    def display_current_image(self):
        """Display the current image"""
        if not self.display_order or self.current_index >= len(self.display_order):
            messagebox.showinfo("Complete", "All images have been processed.")
            return
        
        # Get current filename
        current_filename = self.get_current_filename()
        
        if not current_filename:
            messagebox.showinfo("Error", f"Unable to find image at position {self.current_index + 1}.")
            return
        
        # Update filename label
        self.filename_label.config(text=f"Current File Name is: {current_filename}")
        
        # Display the current image
        image_path = os.path.join(self.image_dir, current_filename)
        self.display_image(image_path)
        
        # Update status
        self.status_label.config(
            text=f"Image {self.current_index + 1} of {len(self.display_order)}: {current_filename}"
        )
        
        # Update nav button states
        self.update_nav_buttons()
    
    def update_nav_buttons(self):
        """Update navigation button states based on current position"""
        # Enable/disable previous button
        if self.current_index <= 0:
            self.prev_btn.config(state=tk.DISABLED)
        else:
            self.prev_btn.config(state=tk.NORMAL)
        
        # Enable/disable next button
        if self.current_index >= len(self.display_order) - 1:
            self.next_btn.config(state=tk.DISABLED)
        else:
            self.next_btn.config(state=tk.NORMAL)
    
    def display_image(self, image_path):
        """Load and display an image in the GUI"""
        try:
            # Check if file exists first
            if not os.path.exists(image_path):
                self.image_label.config(image=None)
                self.image_label.config(text=f"Error: File not found\n{image_path}")
                return
                
            # Open the image file
            img = Image.open(image_path)
            
            # Calculate the resize ratio to fit the window
            window_width = self.main_frame.winfo_width() - 100  # Account for nav buttons
            window_height = self.main_frame.winfo_height() - 20
            
            if window_width <= 1 or window_height <= 1:  # Window not properly sized yet
                window_width = 700  # Reduced to account for nav buttons
                window_height = 500
                
            img_width, img_height = img.size
            scale_width = window_width / img_width
            scale_height = window_height / img_height
            scale = min(scale_width, scale_height)
            
            # Resize the image
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage for display
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference
            
        except Exception as e:
            self.image_label.config(image=None)
            self.image_label.config(text=f"Error loading image: {str(e)}")
    
    def rename_image(self, name):
        """Rename the current image with the selected name"""
        if not self.display_order or self.current_index >= len(self.display_order):
            return
            
        # Get current filename
        current_file = self.get_current_filename()
        if not current_file:
            messagebox.showerror("Error", "Could not find the current file.")
            return
            
        file_ext = os.path.splitext(current_file)[1]
        new_name = f"{name}{file_ext}"
        
        source_path = os.path.join(self.image_dir, current_file)
        dest_path = os.path.join(self.image_dir, new_name)
        
        # Check if destination file already exists
        if os.path.exists(dest_path):
            # Add a number to make the filename unique
            count = 1
            while os.path.exists(os.path.join(self.image_dir, f"{name}_{count}{file_ext}")):
                count += 1
            new_name = f"{name}_{count}{file_ext}"
            dest_path = os.path.join(self.image_dir, new_name)
        
        try:
            # Rename the file
            os.rename(source_path, dest_path)
            
            # Mark the name as used
            self.used_names.add(name)
            
            # Update the button appearance
            if name in self.name_buttons:
                self.name_buttons[name].config(bg="red", fg="white")
            
            # Update the filename map
            self.filename_map[self.current_index] = new_name
            
            # Refresh the directory to keep internal structures in sync
            self.refresh_directory()
            
            # Go to next image
            self.current_index += 1
            
            # Display next image or show completion message
            if self.current_index < len(self.display_order):
                self.display_current_image()
            else:
                messagebox.showinfo("Complete", "All images have been processed.")
                self.status_label.config(text="Processing complete.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename file: {str(e)}")
    
    def skip_image(self):
        """Skip the current image without renaming"""
        if not self.display_order or self.current_index >= len(self.display_order):
            return
            
        self.current_index += 1
        
        if self.current_index < len(self.display_order):
            self.display_current_image()
        else:
            messagebox.showinfo("Complete", "All images have been processed.")
            self.status_label.config(text="Processing complete.")
    
    def previous_image(self):
        """Go to the previous image"""
        if not self.display_order or self.current_index <= 0:
            return
        
        # Refresh directory to make sure our file mappings are current
        self.refresh_directory()
            
        # Move to previous image
        self.current_index -= 1
        self.display_current_image()
    
    def reset_session(self):
        """Reset the session to start over"""
        self.current_index = 0
        self.used_names = set()  # Clear used names
        self.reset_button_appearances()
        
        # Refresh directory contents
        self.refresh_directory()
        
        if self.image_dir and self.display_order:
            self.scan_existing_names()
            self.display_current_image()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRenamerApp(root)
    
    # Set min window size
    root.minsize(800, 600)
    
    # Add window resize event to redisplay image on resize
    def on_resize(event):
        if hasattr(app, 'current_index') and app.display_order and app.current_index < len(app.display_order):
            current_file = app.get_current_filename()
            if current_file:
                image_path = os.path.join(app.image_dir, current_file)
                app.display_image(image_path)
    
    root.bind("<Configure>", on_resize)
    
    root.mainloop()