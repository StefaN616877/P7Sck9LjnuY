# 代码生成时间: 2025-10-02 16:50:58
import tornado.ioloop
import tornado.web
import json

# Define a Metadata class to handle metadata operations
class Metadata:
    def __init__(self):
        # Initialize an empty dictionary to store metadata
        self.metadata_store = {}

    def add_metadata(self, key, value):
        """Add or update metadata in the store.

        Args:
            key (str): The key for the metadata.
            value (str): The value associated with the key."""
        self.metadata_store[key] = value
        return True

    def get_metadata(self, key):
        """Retrieve metadata from the store.

        Args:
            key (str): The key for the metadata.

        Returns:
            str or None: The metadata value if key exists, otherwise None."""
        return self.metadata_store.get(key)

    def delete_metadata(self, key):
        """Delete metadata from the store.

        Args:
            key (str): The key for the metadata to delete.

        Returns:
            bool: True if deletion was successful, False otherwise."""
        if key in self.metadata_store:
            del self.metadata_store[key]
            return True
        return False

# Define handlers for Tornado web requests
class AddMetadataHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            key = data.get('key')
            value = data.get('value')
            metadata_manager.add_metadata(key, value)
            self.write({'status': 'success', 'message': 'Metadata added successfully.'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})

class GetMetadataHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            key = self.get_argument('key')
            value = metadata_manager.get_metadata(key)
            if value is not None:
                self.write({'status': 'success', 'message': 'Metadata retrieved successfully.', 'data': value})
            else:
                self.write({'status': 'error', 'message': 'Metadata not found.'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})

class DeleteMetadataHandler(tornado.web.RequestHandler):
    def delete(self):
        try:
            key = self.get_argument('key')
            result = metadata_manager.delete_metadata(key)
            if result:
                self.write({'status': 'success', 'message': 'Metadata deleted successfully.'})
            else:
                self.write({'status': 'error', 'message': 'Failed to delete metadata.'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})

# Define the Tornado application
def make_app():
    return tornado.web.Application([
        (r"/add", AddMetadataHandler),
        (r"/get", GetMetadataHandler),
        (r"/delete", DeleteMetadataHandler),
    ])

# Initialize the metadata manager
metadata_manager = Metadata()

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print('Metadata Management System started on port 8888.')
    tornado.ioloop.IOLoop.current().start()