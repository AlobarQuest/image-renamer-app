# Image Renamer App

![GitHub last commit](https://img.shields.io/github/last-commit/AlobarQuest/image-renamer-app)
![License](https://img.shields.io/github/license/AlobarQuest/image-renamer-app)

A Python desktop application for efficiently renaming batches of vehicle inspection images using a predefined list of names.

## 🔍 Overview

Image Renamer App is a streamlined tool designed to make renaming multiple image files quick and efficient. It was created to assist with organizing field appraisal photos but can be used for any scenario requiring consistent image naming from a predefined list.

The application provides a simple, visual interface that allows you to quickly cycle through images and assign them standardized names with a single click.

## ✨ Key Features

- **Fast Batch Renaming**: Quickly rename multiple images with just one click per image
- **Visual Image Preview**: View each image while deciding on a name
- **Predefined Name List**: Load and use a customizable list of standard names
- **Used Name Tracking**: Visual indicators show which names have already been used (red buttons)
- **Preserved Image Order**: Images maintain their original order throughout your session
- **Navigation Controls**: Easily move back and forth between images
- **Automatic Numbering**: Adds numbers to duplicate names (e.g., "Dashboard_1", "Dashboard_2")
- **Configuration System**: Save default directories and name lists between sessions

## 📋 Requirements

- Python 3.7 or higher
- Pillow (PIL Fork) 9.0.0 or higher

## 🚀 Installation

### From Source

1. Clone the repository:
   ```
   git clone https://github.com/AlobarQuest/image-renamer-app.git
   cd image-renamer-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python image_renamer.py
   ```

### Creating a Windows Executable

1. Run the included batch file:
   ```
   build_executable.bat
   ```
   
This will:
- Install PyInstaller if needed
- Build a standalone executable
- Place it in the `dist` folder

After building, copy `config.ini` and `namelist.txt` to the same directory as the executable.

## 📖 Usage

### Quick Start

1. **Launch the application**
2. **Select an image directory** using the "Select Image Directory" button
3. **Browse through images** using the arrow buttons
4. **Rename each image** by clicking on the appropriate name button
5. **Skip images** you don't want to rename using the "Don't Rename" button

### Workflow Details

- The program automatically loads the name list specified in your config.ini file
- All name buttons appear at the bottom of the window in alphabetical order
- When a name has been used, its button turns red with white text (but remains available for reuse)
- Original image order is preserved throughout your session
- You can navigate back to review or change previous renaming decisions

## ⚙️ Configuration

The application uses a `config.ini` file to store default settings:

```ini
[Settings]
default_image_directory=C:\Path\To\Images
default_namelist=namelist.txt
```

### Customizing the Name List

Edit the `namelist.txt` file to include your desired names, with one name per line:

```
Corner - LF
Corner - RF
Corner - RR
Corner - LR
Tag
VIN
```

You can create multiple name list files and specify which one to use by default in `config.ini`.

## 🔧 Tips for Effective Use

- **Prepare your name list ahead of time** to make the renaming process smoother
- **Use descriptive names** that will help you identify images later
- **For batch processing**, consider creating specific name lists for different image sets
- **Use the back navigation** to review and correct any naming mistakes
- **For chronological sequences**, the preserved order feature ensures images remain in their original sequence

## 📝 Documentation

For detailed usage instructions, see the [How To Use Guide](HOW_TO_USE.md) included in this repository.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Created by Devon (AlobarQuest)
- Built using Python and Tkinter
- Developed to streamline field appraisal workflows
