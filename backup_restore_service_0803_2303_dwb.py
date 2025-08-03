# 代码生成时间: 2025-08-03 23:03:43
import os
import shutil
import json
import logging
from tornado import ioloop, web, options
from tornado.options import define, options

# Define the command-line options
define("port", default=8888, help="run on the given port", type=int)

# Configuration
CONFIG = {
    "backup_dir": "./backup",
    "data_dir": "./data"
}

class BackupHandler(web.RequestHandler):
    """ Handles backup requests. """
    def post(self):
        try:
            # Perform backup operation
            self.backup_data()
            self.write({'status': 'success', 'message': 'Data backed up successfully'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})

    def backup_data(self):
        """ Backs up the data from the data directory to a backup file. """
        if not os.path.exists(CONFIG['data_dir']):
            raise Exception("Data directory does not exist.")

        backup_path = f"{CONFIG['backup_dir']}/data_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
        shutil.make_archive(backup_path, 'zip', CONFIG['data_dir'])
        logging.info(f"Data backed up to {backup_path}")

class RestoreHandler(web.RequestHandler):
    """ Handles restore requests. """
    def post(self):
        try:
            # Perform restore operation
            self.restore_data()
            self.write({'status': 'success', 'message': 'Data restored successfully'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})

    def restore_data(self):
        """ Restores the data from the latest backup file to the data directory. """
        if not os.path.exists(CONFIG['backup_dir']):
            raise Exception("Backup directory does not exist.")

        latest_backup = max([f for f in os.listdir(CONFIG['backup_dir']) if f.endswith(".zip")], key=lambda x: os.path.getctime(os.path.join(CONFIG['backup_dir'], x)))
        backup_path = os.path.join(CONFIG['backup_dir'], latest_backup)

        if not latest_backup:
            raise Exception("No backup files found.")

        with zipfile.ZipFile(backup_path, 'r') as zip_ref:
            zip_ref.extractall(CONFIG['data_dir'])
        logging.info(f"Data restored from {latest_backup}")

class MainHandler(web.RequestHandler):
    """ Handles the main request to display the status. """
    def get(self):
        self.write("Backup and Restore Service is running...")

def make_app():
    """ Creates the Tornado application. """
    return web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/backup", BackupHandler),
            (r"/restore", RestoreHandler),
        ],
        debug=True
    )

if __name__ == "__main__":
    # Parse command-line options
    options.parse_command_line()

    # Create and run the application
    app = make_app()
    app.listen(options.port)
    logging.info(f"Server starting on port {options.port}")
    ioloop.IOLoop.current().start()