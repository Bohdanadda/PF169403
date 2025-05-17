from __future__ import annotations

import json
import os
import shutil
import time
from datetime import datetime
from typing import Any, Dict, Optional


class JSONHandler:
    """
    Handles JSON file operations with error handling and backup functionality.

    Methods
    -------
    save_to_file(data: Dict[str, Any], filepath: str) -> None
        Save data to JSON file with backup creation
    load_from_file(filepath: str) -> Dict[str, Any]
        Load data from JSON file
    """

    @staticmethod
    def save_to_file(data: Dict[str, Any], filepath: str) -> None:
        """
        Save data to JSON file with backup creation.

        Parameters
        ----------
        data : Dict[str, Any]
            Data to save
        filepath : str
            Path to the JSON file

        Raises
        ------
        PermissionError
            If file is read-only or no write permissions
        """
        try:
            # Create backup if file exists
            if os.path.exists(filepath):
                # Create backup with microsecond precision timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                backup_path = f"{filepath}.{timestamp}.bak"
                shutil.copy2(filepath, backup_path)
                # Small delay to ensure unique timestamps
                time.sleep(0.001)

            # Save new data
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)

        except PermissionError:
            raise PermissionError(f"No permission to write to {filepath}")
        except Exception as e:
            raise Exception(f"Error saving to {filepath}: {str(e)}")

    @staticmethod
    def load_from_file(filepath: str) -> Dict[str, Any]:
        """
        Load data from JSON file.

        Parameters
        ----------
        filepath : str
            Path to the JSON file

        Returns
        -------
        Dict[str, Any]
            Loaded data

        Raises
        ------
        FileNotFoundError
            If file doesn't exist
        json.JSONDecodeError
            If file contains invalid JSON
        """
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Invalid JSON format", filepath, 0)
