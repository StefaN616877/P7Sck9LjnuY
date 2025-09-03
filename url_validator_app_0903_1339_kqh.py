# 代码生成时间: 2025-09-03 13:39:36
import tornado.ioloop
import tornado.web
from urllib.parse import urlparse
import requests

"""
URL Validator Application using Tornado Framework.

This application validates the given URL by checking if it is reachable.
It provides a simple web service that accepts a URL as input and returns
whether the URL is valid or not.
"""

class MainHandler(tornado.web.RequestHandler):
    """
    Main request handler for the URL validation service.
    """
    def get(self):
        # Get the URL from the query parameters
        url = self.get_query_argument('url')
        try:
            # Validate the URL
            result = self.validate_url(url)
            self.write({'status': 'success', 'message': result})
        except Exception as e:
            # Handle any unexpected errors
            self.write({'status': 'error', 'message': str(e)})

    def validate_url(self, url):
        """
        Validate the given URL by checking if it is reachable.
        
        Args:
        url (str): The URL to validate.
        
        Returns:
        str: 'Valid' if the URL is reachable, 'Invalid' otherwise.
        """
        try:
            # Check if the URL is well-formed
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                return 'Invalid'
            
            # Send a HEAD request to check if the URL is reachable
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                return 'Valid'
            else:
                return 'Invalid'
        except requests.RequestException as e:
            return 'Invalid'
        except Exception as e:
            # Handle any unexpected errors
            raise e

def make_app():
    """
    Create the Tornado application.
    """
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("URL Validator app is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()