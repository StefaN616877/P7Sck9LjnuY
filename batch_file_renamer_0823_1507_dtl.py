# 代码生成时间: 2025-08-23 15:07:41
import os
import re

"""
Batch File Renamer tool using Python and Tornado framework.
This program allows users to rename files in a batch based on a given pattern.
"""

class BatchFileRenamer:
    def __init__(self, directory):
        """
        Initialize the BatchFileRenamer object with the target directory.
        :param directory: The directory to perform file renaming.
        """
        self.directory = directory

    def rename_files(self, pattern, new_name):
        """
        Rename files in the directory based on the given pattern.
        :param pattern: A regex pattern to match files for renaming.
        :param new_name: The new name for the files.
        """
        try:
            files = self._list_files()
            for file in files:
                if re.match(pattern, file):
                    new_path = self._construct_new_path(file, new_name)
                    self._move_file(file, new_path)
            print(f"Renamed {len(files)} files successfully.")
        except Exception as e:
            print(f"Error occurred: {e}")

    def _list_files(self):
        """
        List all files in the target directory.
        :return: A list of file names.
        """
        return [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]

    def _construct_new_path(self, file, new_name):
        """
        Construct the new file path based on the original file and new name.
        :param file: The original file name.
        :param new_name: The new name for the file.
        :return: The new file path.
        """
        file_extension = os.path.splitext(file)[1]
        return os.path.join(self.directory, f"{new_name}{file_extension}")

    def _move_file(self, old_path, new_path):
        """
        Move (or rename) the file to the new path.
        :param old_path: The original file path.
        :param new_path: The new file path.
        """
        os.rename(old_path, new_path)

# Example usage:
if __name__ == "__main__":
    directory = "/path/to/your/directory"
    pattern = "^old_name_.*"  # Pattern to match files for renaming
    new_name = "new_name"  # New file name

    # Initialize the BatchFileRenamer object
    renamer = BatchFileRenamer(directory)

    # Rename files in the directory
    renamer.rename_files(pattern, new_name)