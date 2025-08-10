# 代码生成时间: 2025-08-11 07:02:00
import os
import shutil
from collections import defaultdict
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

"""
Folder Organizer Application using Tornado Framework

This application is designed to organize files in a specified directory by moving files
into subdirectories based on their extensions.
"""

class FolderOrganizerHandler(RequestHandler):
    def get(self):
        """
        Handles GET requests to organize files in the specified directory.
        """
        # Retrieve directory path from query parameters
        directory = self.get_query_argument('directory', default='.')
        try:
            # Organize files in the directory
            self.organized_files(directory)
            self.write({"status": "Files organized successfully"})
        except Exception as e:
            # Handle any exceptions that occur during the organizing process
            self.write({"status": "Error occurred", "error": str(e)})

    def organized_files(self, directory):
        """
        Organizes files in the given directory by moving them into subdirectories based on their extensions.
        """
        # Check if the directory exists
# 增强安全性
        if not os.path.exists(directory):
            raise ValueError(f"Directory '{directory}' does not exist.")
        
        # Create a dictionary to store files by their extensions
        files_by_extension = defaultdict(list)
        
        # Iterate through all files in the directory
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                # Get the file extension
                extension = os.path.splitext(filename)[1]
                
                # Add the file to the dictionary
                files_by_extension[extension].append(filename)
        
        # Create subdirectories for each extension and move files into them
        for extension, filenames in files_by_extension.items():
            subdirectory = os.path.join(directory, extension[1:])  # Remove the dot from the extension
            if not os.path.exists(subdirectory):
                os.makedirs(subdirectory)
            for filename in filenames:
                shutil.move(os.path.join(directory, filename), os.path.join(subdirectory, filename))

def make_app():
    """
    Creates a Tornado application with the FolderOrganizerHandler.
    """
    return Application([
        (r"/", FolderOrganizerHandler),
# 扩展功能模块
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()