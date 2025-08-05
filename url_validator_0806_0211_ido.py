# 代码生成时间: 2025-08-06 02:11:29
import tornado.ioloop
import tornado.web
import requests
from urllib.parse import urlparse

"""
A simple Tornado application to validate URL links.
This application provides a web service that checks if given URLs are valid.
"""

class UrlValidatorHandler(tornado.web.RequestHandler):
    """
    Handles HTTP GET requests to validate a URL.
    """
    def get(self):
        # Get the URL to validate from the query string
        url_to_validate = self.get_argument('url', None)
        if not url_to_validate:
            self.set_status(400)
            self.write("Missing 'url' parameter in the query string.")
            return
        
        try:
            valid, reason = validate_url(url_to_validate)
            if valid:
                self.write({'status': 'valid', 'reason': reason})
            else:
                self.set_status(400)
                self.write({'status': 'invalid', 'reason': reason})
        except Exception as e:
            self.set_status(500)
            self.write({'status': 'error', 'reason': str(e)})


def validate_url(url):
    """
    Validates the given URL by checking if it can be reached and if it has a valid scheme.
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return False, 'URL has no scheme.'
    try:
        # Use requests.head to check URL validity without downloading the whole content
        response = requests.head(url, timeout=5)
        return response.status_code < 400, f'HTTP status code: {response.status_code}'
    except requests.RequestException as e:
        return False, str(e)


def make_app():
    """
    Creates a Tornado web application with the URL validator handler.
    """
    return tornado.web.Application([
        (r"/validate", UrlValidatorHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("URL validator service running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()