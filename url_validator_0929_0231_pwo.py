# 代码生成时间: 2025-09-29 02:31:22
import tornado.ioloop
import tornado.web
import requests
from urllib.parse import urlparse

"""
URL Validator application using Tornado Framework.
This application validates the given URL for its existence.
"""

class MainHandler(tornado.web.RequestHandler):
    """
    Request handler for validating URLs.
    """
    def get(self):
        # Get the URL from the query parameters
        url_to_validate = self.get_argument('url', '')
        try:
            # Validate the URL
            if self.is_valid_url(url_to_validate):
                self.write({'status': 'valid', 'message': 'URL is valid.'})
            else:
                self.write({'status': 'invalid', 'message': 'URL is invalid.'})
        except Exception as e:
            # Handle any unforeseen errors
            self.write({'status': 'error', 'message': str(e)})

    def is_valid_url(self, url):
        """
        Checks if the provided URL is valid.
        """
        try:
            # Parse the URL to check its structure
            result = urlparse(url)
            # Check if the scheme and netloc are present
            if all([result.scheme, result.netloc]):
                # Make a HEAD request to check if the URL is reachable
                response = requests.head(url, allow_redirects=True, timeout=5)
                # Check if the response status code is 2xx or 3xx
                return 200 <= response.status_code < 400
            else:
                return False
        except requests.RequestException:
            return False
        except ValueError:
            return False

def make_app():
    """
    Creates the Tornado application with the URL validator handler.
    """
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("URL Validator app is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()