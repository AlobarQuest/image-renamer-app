import pytest
import os
import sys
import tkinter as tk
from unittest.mock import patch, MagicMock
from PIL import Image, ImageTk
import io

# Adjust system path to import the ImageRenamerApp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from image_renamer import ImageRenamerApp

class TestFileOperations:
    """
    Test class for file operations in the Image Renamer application.
    Tests file loading, renaming, and directory operations.
    """
    
    @pytest.fixture
    def setup_test_env(self, tmpdir):
        """Create a test environment with sample images and name list."""
        # Create a temporary directory with test images
        image_dir = tmpdir.mkdir("test_images")
        
        # Create a few test images
        test_image = Image.new('RGB', (100, 100), color='red')
        for i in range(1, 4):
            img_path = image_dir.join(f"test{i}.jpg")
            test_image.save(str(img_path))
        
        # Create a name list file
        name_list_file = tmpdir.join("namelist.txt")
        name_list_file.write("Name1\nName2\nName3\nName4")
        
        return {
            "image_dir": str(image_dir),
            "name_list_path": str(name_list_file),
            "image_files": [f"test{i}.jpg" for i in range(1, 4)]
        }
    
    @pytest.fixture
    def mock_app(self):
        """Create a mocked instance of the ImageRenamerApp."""
        with patch('tkinter.Tk') as mock_tk:
            root = mock_tk.return_value
            app = ImageRenamerApp(root)
            
            # Mock GUI-related methods to avoid actual rendering
            app.display_image = MagicMock()
            app.update_button_appearances = MagicMock()
            app.update_nav_buttons = MagicMock()
            
            yield app
    
    def test_load_images(self, mock_app, setup_test_env):
        """Test loading images from a directory."""
        env = setup_test_env
        mock_app.image_dir = env["image_dir"]
        
        # Mock messagebox to prevent actual popups
        with patch('tkinter.messagebox.showinfo'):
            mock_app.load_images()
        
        # Verify images were loaded correctly
        assert len(mock_app.image_files) == 3
        assert all(f in mock_app.image_files for f in env["image_files"])
        assert mock_app.current_index == 0
        assert len(mock_app.display_order) == 3
        assert mock_app.filename_map[0] in env["image_files"]
    
    def test_load_name_list(self, mock_app, setup_test_env):
        """Test loading a name list from a file."""
        env = setup_test_env
        
        # Call the method being tested
        result = mock_app.load_name_list_from_file(env["name_list_path"])
        
        # Verify the name list was loaded correctly
        assert result is True
        assert len(mock_app.names) == 4
        assert "Name1" in mock_app.names
        assert "Name2" in mock_app.names
        assert "Name3" in mock_app.names
        assert "Name4" in mock_app.names
        assert mock_app.original_names == mock_app.names
    
    def test_rename_image(self, mock_app, setup_test_env):
        """Test renaming an image file."""
        env = setup_test_env
        mock_app.image_dir = env["image_dir"]
        mock_app.image_files = env["image_files"]
        mock_app.display_order = env["image_files"].copy()
        mock_app.filename_map = {i: filename for i, filename in enumerate(mock_app.display_order)}
        mock_app.current_index = 0
        mock_app.used_names = set()
        
        # Setup name buttons for testing
        mock_app.name_buttons = {
            "Name1": MagicMock(),
            "Name2": MagicMock(),
            "Name3": MagicMock(),
            "Name4": MagicMock()
        }
        
        # Mock refresh_directory to avoid actual file system operations
        mock_app.refresh_directory = MagicMock(return_value=True)
        
        # Mock os.path.exists to handle file existence checks
        with patch('os.path.exists', return_value=False):
            # Mock os.rename to avoid actual file renaming
            with patch('os.rename') as mock_rename:
                # Call the method being tested
                mock_app.rename_image("Name1")
                
                # Verify rename was called with correct parameters
                mock_rename.assert_called_once_with(
                    os.path.join(env["image_dir"], mock_app.display_order[0]),
                    os.path.join(env["image_dir"], "Name1.jpg")
                )
                
                # Verify state changes
                assert "Name1" in mock_app.used_names
                assert mock_app.filename_map[0] == "Name1.jpg"
                assert mock_app.current_index == 1
                mock_app.refresh_directory.assert_called_once()
    
    def test_rename_image_duplicate(self, mock_app, setup_test_env):
        """Test renaming with duplicate name handling."""
        env = setup_test_env
        mock_app.image_dir = env["image_dir"]
        mock_app.image_files = env["image_files"]
        mock_app.display_order = env["image_files"].copy()
        mock_app.filename_map = {i: filename for i, filename in enumerate(mock_app.display_order)}
        mock_app.current_index = 0
        mock_app.used_names = set()
        
        # Setup name buttons for testing
        mock_app.name_buttons = {
            "Name1": MagicMock(),
            "Name2": MagicMock()
        }
        
        # Mock refresh_directory to avoid actual file system operations
        mock_app.refresh_directory = MagicMock(return_value=True)
        
        # First call: Create Name1.jpg
        with patch('os.path.exists') as mock_exists:
            # First call to exists returns False, second call returns True
            mock_exists.side_effect = [False, True, True]
            
            with patch('os.rename') as mock_rename:
                mock_app.rename_image("Name1")
                
                # Verify rename was called with correct parameters
                mock_rename.assert_called_once_with(
                    os.path.join(env["image_dir"], mock_app.display_order[0]),
                    os.path.join(env["image_dir"], "Name1.jpg")
                )
        
        # Reset for second test and simulate Name1.jpg already exists
        mock_app.current_index = 1
        
        # Second call: Should create Name1_1.jpg because Name1.jpg exists
        with patch('os.path.exists') as mock_exists:
            # Simulate Name1.jpg exists but Name1_1.jpg doesn't
            mock_exists.side_effect = [True, False]
            
            with patch('os.rename') as mock_rename:
                mock_app.rename_image("Name1")
                
                # Verify rename was called with correct parameters for the duplicate
                mock_rename.assert_called_once_with(
                    os.path.join(env["image_dir"], mock_app.display_order[1]),
                    os.path.join(env["image_dir"], "Name1_1.jpg")
                )
    
    def test_skip_image(self, mock_app, setup_test_env):
        """Test skipping an image without renaming."""
        env = setup_test_env
        mock_app.image_dir = env["image_dir"]
        mock_app.image_files = env["image_files"]
        mock_app.display_order = env["image_files"].copy()
        mock_app.filename_map = {i: filename for i, filename in enumerate(mock_app.display_order)}
        mock_app.current_index = 0
        
        # Mock display_current_image to verify it gets called
        mock_app.display_current_image = MagicMock()
        
        # Execute skip_image and verify the index increments
        with patch('tkinter.messagebox.showinfo'):
            mock_app.skip_image()
            
            assert mock_app.current_index == 1
            mock_app.display_current_image.assert_called_once()
    
    def test_previous_image(self, mock_app, setup_test_env):
        """Test navigation to the previous image."""
        env = setup_test_env
        mock_app.image_dir = env["image_dir"]
        mock_app.image_files = env["image_files"]
        mock_app.display_order = env["image_files"].copy()
        mock_app.filename_map = {i: filename for i, filename in enumerate(mock_app.display_order)}
        mock_app.current_index = 1  # Start at second image
        
        # Mock refresh_directory and display_current_image
        mock_app.refresh_directory = MagicMock(return_value=True)
        mock_app.display_current_image = MagicMock()
        
        # Execute previous_image and verify the index decrements
        mock_app.previous_image()
        
        # Verify state changes
        assert mock_app.current_index == 0
        mock_app.refresh_directory.assert_called_once()
        mock_app.display_current_image.assert_called_once()
    
    def test_scan_existing_names(self, mock_app, setup_test_env):
        """Test scanning for existing names in the directory."""
        env = setup_test_env
        mock_app.image_dir = env["image_dir"]
        
        # Create a test file that matches a name in our list
        name1_file = os.path.join(env["image_dir"], "Name1.jpg")
        with open(name1_file, 'w') as f:
            f.write("dummy content")
        
        # Load name list
        mock_app.load_name_list_from_file(env["name_list_path"])
        
        # Mock update_button_appearances
        mock_app.update_button_appearances = MagicMock()
        
        # Execute scan_existing_names
        mock_app.scan_existing_names()
        
        # Verify Name1 was detected as used
        assert "Name1" in mock_app.used_names
        mock_app.update_button_appearances.assert_called_once()
