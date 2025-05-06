import pytest
import os
import tkinter as tk
from unittest.mock import patch, MagicMock
from PIL import Image
import sys

# Add the project root to sys.path to allow importing the application
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_renamer import ImageRenamerApp

@pytest.fixture
def sample_image_dir(tmpdir):
    """
    Create a temporary directory with sample images for testing.
    
    Returns:
        dict: Dictionary containing paths and file information
    """
    # Create a temporary directory for test images
    image_dir = tmpdir.mkdir("test_images")
    
    # Create sample test images
    test_image = Image.new('RGB', (100, 100), color='red')
    image_files = []
    
    for i in range(1, 6):
        img_path = image_dir.join(f"test{i}.jpg")
        test_image.save(str(img_path))
        image_files.append(f"test{i}.jpg")
    
    return {
        "image_dir": str(image_dir),
        "image_files": image_files
    }

@pytest.fixture
def sample_name_list(tmpdir):
    """
    Create a sample name list file for testing.
    
    Returns:
        str: Path to the name list file
    """
    # Create a name list file
    name_list_file = tmpdir.join("namelist.txt")
    name_list_file.write("Dashboard\nEngine\nSeat\nWheel\nVIN\nExterior\nInterior\nDamage")
    
    return str(name_list_file)

@pytest.fixture
def mock_app():
    """
    Create a mocked instance of the ImageRenamerApp with GUI elements disabled.
    
    Returns:
        ImageRenamerApp: Mocked application instance
    """
    with patch('tkinter.Tk') as mock_tk:
        root = mock_tk.return_value
        app = ImageRenamerApp(root)
        
        # Mock GUI-related methods to avoid actual rendering
        app.display_image = MagicMock()
        app.update_button_appearances = MagicMock()
        app.update_nav_buttons = MagicMock()
        app.create_name_buttons = MagicMock()
        
        yield app

@pytest.fixture
def configured_app(mock_app, sample_image_dir, sample_name_list):
    """
    Configure the mocked app with test data.
    
    Args:
        mock_app: The mocked application instance
        sample_image_dir: Test image directory fixture
        sample_name_list: Test name list fixture
        
    Returns:
        ImageRenamerApp: Configured application instance
    """
    # Set up the app with test data
    with patch('tkinter.messagebox.showinfo'):
        # Configure image directory
        mock_app.image_dir = sample_image_dir["image_dir"]
        mock_app.image_files = sample_image_dir["image_files"]
        mock_app.display_order = sample_image_dir["image_files"].copy()
        mock_app.filename_map = {i: filename for i, filename in enumerate(mock_app.display_order)}
        mock_app.current_index = 0
        
        # Load name list
        mock_app.load_name_list_from_file(sample_name_list)
        
        # Set up mock name buttons
        mock_app.name_buttons = {name: MagicMock() for name in mock_app.names}
    
    return mock_app

@pytest.fixture
def mock_pil_image():
    """
    Create a mock PIL Image for testing image display functions.
    
    Returns:
        MagicMock: Mocked PIL Image object
    """
    with patch('PIL.Image.open') as mock_open:
        img_mock = MagicMock()
        img_mock.size = (200, 150)
        mock_open.return_value = img_mock
        yield img_mock
