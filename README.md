# Image Renamer Tool

A Python tool for quickly renaming image files using a predefined list of names.

## Features

- Load and display images from any directory
- Rename images with names from a customizable list
- Fast performance with buttons created only once at startup
- Automatic detection of already-used names
- Navigation through images with previous/next buttons
- Visual feedback showing which names have been used (red buttons)
- Configurable default directories and name lists

## Setup Instructions

1. Make sure you have Python installed (3.7 or higher recommended)
2. Install required libraries by running:
   ```
   pip install pillow
   ```
3. Run the tool using:
   ```
   python image_renamer.py
   ```

## Configuration

The tool supports automatic configuration through a `config.ini` file:

```
[Settings]
default_image_directory=C:\Path\To\Your\Images
default_namelist=namelist.txt
```

- `default_image_directory`: The directory that will open by default when selecting images
- `default_namelist`: The name list file to load at startup (must be in the same directory as the script)

## Creating an Executable

To create a standalone Windows executable:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Run from the command prompt:
   ```
   pyinstaller --onefile --windowed --name ImageRenamer image_renamer.py
   ```
3. Find the executable in the `dist` folder
4. Copy `config.ini` and `namelist.txt` to the same directory as the executable

## Usage

1. Run the tool (either `python image_renamer.py` or the executable)
2. The program automatically loads the default name list file specified in config.ini
3. All name buttons are created at startup for maximum performance
4. The program scans the selected directory for files already named with names from your list and marks those buttons in red
5. Click "Select Image Directory" to choose a folder with images (starts in the directory specified in config.ini)
6. For each image:
   - Click a name button to rename the image and move to the next
   - Use the arrow buttons to navigate between images
   - Click "Don't Rename" to move to the next image without renaming
7. When a name has been used, its button turns red with white text but remains available for reuse

## Customizing Names

Edit the `namelist.txt` file to include your desired names, with one name per line:

```
Corner - LF
Corner - RF
Corner - RR
Corner - LR
Tag
Dash VIN
Door VIN
```

You can create multiple name list files and specify which one to use by default in `config.ini`.

## License

This project is open source and available under the MIT License.
