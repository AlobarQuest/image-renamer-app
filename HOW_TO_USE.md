# How to Use the Image Renamer Tool

The Image Renamer Tool is designed to make renaming multiple image files quick and efficient. This guide will walk you through how to use the application and highlight its key features.

## Quick Start Guide

1. **Launch the application** by either:
   - Running `image_renamer.py` if you have Python installed
   - Opening the executable version (ImageRenamer.exe) if you're using the compiled version

2. **Initial Setup:**
   - The program automatically loads the name list specified in your config.ini file
   - All name buttons appear at the bottom of the window in alphabetical order

3. **Select Images:**
   - Click the "Select Image Directory" button at the top left
   - Navigate to the folder containing your images
   - The program will automatically detect any already-used names and mark those buttons red

4. **Rename Images:**
   - The first image will appear in the main window
   - The current filename is displayed above the image
   - Click on any name button to rename the current image to that name
   - The program automatically moves to the next image
   - Used names turn red but remain available for reuse if needed

5. **Navigation:**
   - Use the arrow buttons (◀ ▶) on the sides of the image to navigate back and forth
   - Previous button is disabled when you're at the first image
   - Next button is disabled when you're at the last image
   - Click "Don't Rename" to skip the current image without renaming it
   - You can navigate back through images even after renaming them

6. **Complete:**
   - When all images have been processed, you'll see a completion message
   - You can still navigate back to review and modify previous images
   - You can start over with a new folder at any time

## Key Features

- **Speed and Efficiency:**
  - Name buttons are created once at startup for maximum performance
  - Single-click renaming - just click a name and it moves to the next image
  - Automatic file extension preservation

- **Smart Management:**
  - Automatic detection of already-used names
  - Visual tracking (red buttons) of which names have been used
  - Automatic handling of duplicate filenames by adding numbers (e.g., Name_1.jpg)
  - Directory contents automatically refresh after each rename operation

- **Robust Navigation:**
  - Previous/Next buttons for easy browsing through images
  - Ability to go back and change previous renaming decisions
  - Navigation state indicators (disabled buttons at boundaries)
  - Intelligent handling of renamed files in navigation history
  - Error recovery if a file can't be found or accessed

- **Visual Clarity:**
  - Current filename display above the image
  - Wide name buttons to ensure text is fully visible
  - Alphabetical sorting of names for easier selection
  - Clear visual feedback with red background for used names

- **Customization:**
  - Configurable default image directory
  - Customizable name lists
  - Ability to reload different name lists during a session

## Customizing Your Experience

### Modifying the Name List:
1. Open `namelist.txt` in any text editor
2. Add, remove, or change names (one name per line)
3. Save the file in the same directory as the application

### Changing Default Settings:
1. Open `config.ini` in any text editor
2. Modify the `default_image_directory` path to your preferred starting folder
3. Change `default_namelist` if you want to use a different name list file

## Tips for Effective Use

- **Prepare your name list ahead of time** to make the renaming process smoother
- **Consider organizing names alphabetically** in your namelist.txt file (the program will sort them anyway)
- **Use descriptive names** that will help you identify images later
- **For batch processing**, consider creating specific name lists for different image sets
- **Use the back navigation** to review and correct any naming mistakes

## Troubleshooting

- If the program doesn't find your namelist.txt, make sure it's in the same directory as the application
- If a directory doesn't appear in the file browser, check that you have proper permissions to access it
- If images aren't displaying, verify they are in a supported format (JPG, JPEG, PNG, GIF, BMP, TIFF)
- If the Previous button doesn't work on a specific image, ensure the file still exists and hasn't been moved externally
- Navigation errors usually indicate that a file was renamed or moved outside of the application

## Additional Information

This tool is designed to be straightforward and efficient for quickly renaming batches of images. The interface prioritizes speed and simplicity, allowing you to process many images in minimal time with just single clicks.

### Recent Improvements

The latest version includes significant improvements to navigation functionality:
- Robust error handling for file operations
- Better tracking of file history during renaming
- Improved navigation experience with disabled buttons at boundaries
- Automatic directory refreshing to ensure accuracy