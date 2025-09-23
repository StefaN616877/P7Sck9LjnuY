# 代码生成时间: 2025-09-23 23:04:01
import tornado.ioloop
import tornado.web
import tornado.gen
import requests

"""
A Tornado web application that validates the effectiveness of a given URL.
"""

# Define a class for URL validation
class URLHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, url):
        # Validate URL format
        try:
            response = yield self.validate_url(url)
            self.write({
                "status": "success",
                "message": "URL is valid",
                "response": response
            })
        except ValueError as e:
            self.write({
                "status": "error",
                "message": str(e)
            })
        except Exception as e:
            self.write({
                "status": "error",
                "message": "An unexpected error occurred"
            })

    # Asynchronously validate a URL
    @tornado.gen.coroutine
    def validate_url(self, url):
        # Check if url is None or empty
        if not url:
            raise ValueError("URL is empty or not provided")
        try:
            # Make a HEAD request to check if the URL is valid
            r = requests.head(url, timeout=5)
            # Check for a valid HTTP response status code
            if 200 <= r.status_code < 400:
                raise tornado.gen.Return(r.status_code)
            else:
                raise ValueError("URL returned a non-successful status code: {}".format(r.status_code))
        except requests.exceptions.RequestException as e:
            raise ValueError("URL is invalid or not reachable: {}".format(e))

# Create the application
def make_app():
    return tornado.web.Application([
        (r"/validate/([^\/]+)",
         URLHandler),
    ])

# Entry point for the application
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()