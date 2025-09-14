# 代码生成时间: 2025-09-14 18:51:05
import os
import shutil
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.options import define, options
from tornado.web import Application, RequestHandler

# Define the path for the backup directory
DEFAULT_BACKUP_DIR = "./backup/"

class FileBackupSyncHandler(RequestHandler):
    @gen.coroutine
    def post(self):
        # Get the source and destination directories from the request
        source_path = self.get_argument('source')
        destination_path = self.get_argument('destination')
        
        # Validate the paths
        if not os.path.exists(source_path):
            self.write("Source path does not exist.")
            self.set_status(404)
            return
        if not os.path.exists(os.path.dirname(destination_path)):
            self.write("Destination path does not exist.")
            self.set_status(404)
            return
        
        try:
            # Create the destination directory if it doesn't exist
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            
            # Copy the files from source to destination
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(destination_path, os.path.relpath(src_file, source_path))
                    shutil.copy2(src_file, dest_file)
            
            # Return success message
            self.write("Backup and sync completed successfully.")
        except Exception as e:
            # Handle any exceptions and return the error message
            self.write(f"An error occurred: {e}")
            self.set_status(500)

def make_app():
    return Application(
        [
            (r"/backup_sync", FileBackupSyncHandler),
        ],
    )

if __name__ == "__main__":
    define("port", default=8888, help="run on the given port", type=int)
    options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print(f"Backup and sync server is running on port {options.port}")
    IOLoop.current().start()
