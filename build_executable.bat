@echo off
echo Building Image Renamer executable...

pip install pyinstaller
pyinstaller --onefile --windowed --name ImageRenamer image_renamer.py

echo.
echo Build complete! Executable can be found in the "dist" folder.
echo Don't forget to copy config.ini and namelist.txt to the same directory as the executable.
echo.
pause