# 代码生成时间: 2025-08-30 05:11:23
import os
import json
import shutil
from tornado import web, ioloop
from tornado.options import define, options
from tornado.web import RequestHandler

# Define the command line options
define("port", default=8888, help="run on the given port", type=int)

# Directory where the backups will be stored
BACKUP_DIR = "backups"

class MainHandler(RequestHandler):
    """
    Handles the main page request.
    Displays the list of backups and allows to perform backup or restore operations.
    """
    def get(self):
        self.render("index.html", backups=self.get_backup_list())

    def post(self):
        action = self.get_argument("action")
        if action == "backup":
            self.backup()
        elif action == "restore":
            backup_file = self.get_argument("backup")
            self.restore(backup_file)
        self.redirect("/")

    def get_backup_list(self):
        """
        Returns a list of backups in the backup directory.
        Each backup is represented as a dictionary with 'name' and 'created' keys.
        """
        backups = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(BACKUP_DIR, filename)
                with open(file_path, "r") as file:
                    backup_data = json.load(file)
                backups.append({"name": filename, "created": backup_data["created"]})
        return backups

    def backup(self):
        """
        Creates a backup of the current state and saves it in the backup directory.
        """
        try:
            # Simulate the backup process
            backup_data = {"data": "This is a backup of the data.", "created": self.get_current_time()}
            with open(os.path.join(BACKUP_DIR, self.get_backup_filename()), "w") as backup_file:
                json.dump(backup_data, backup_file)
        except Exception as e:
            self.write(f"Backup failed: {e}")
            self.set_status(500)

    def restore(self, backup_file):
        """
        Restores the data from the specified backup file.
        """
        try:
            file_path = os.path.join(BACKUP_DIR, backup_file)
            with open(file_path, "r\) as backup_file:
                backup_data = json.load(backup_file)
                # Simulate the restore process
                print("Restoring from backup: ", backup_data)
        except FileNotFoundError:
            self.write("Backup file not found.")
            self.set_status(404)
        except Exception as e:
            self.write(f"Restore failed: {e}")
            self.set_status(500)

    def get_current_time(self):
        """
        Returns the current time as a string.
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_backup_filename(self):
        """
        Generates a filename for the backup file based on the current time.
        """
        return f"backup_{self.get_current_time()}.json"

class BackupApplication(web.Application):
    """
    The main application class that sets up the Tornado web application.
    """
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = {
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
        }
        super(BackupApplication, self).__init__(handlers, **settings)

if __name__ == "__main__":
    # Prepare the backup directory
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # Run the Tornado application
    options.parse_command_line()
    app = BackupApplication()
    app.listen(options.port)
    print(f"Server starting on port {options.port}...")
    ioloop.IOLoop.current().start()