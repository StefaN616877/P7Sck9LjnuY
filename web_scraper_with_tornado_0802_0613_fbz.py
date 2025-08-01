# 代码生成时间: 2025-08-02 06:13:45
import urllib.request
import tornado.ioloop
import tornado.web
from bs4 import BeautifulSoup

"""
A simple web scraper using Python and Tornado framework.
It demonstrates how to create a web server with a single route to scrape web content.
"""

class ScrapeHandler(tornado.web.RequestHandler):
    """
    A RequestHandler to serve the scraping functionality.

    It takes a URL from the query string, scrapes the content and returns it as HTML.
    """
    async def get(self):
        # Retrieve the URL from the query string
        url = self.get_argument('url', None)

        if not url:
            # If no URL is provided, return an error message
            self.write("Please provide a URL to scrape.")
            self.set_status(400)
            return

        try:
            # Fetch the content of the webpage
            with urllib.request.urlopen(url) as response:
                html_content = response.read()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Return the parsed HTML content
            self.write(str(soup.prettify()))
        except urllib.error.URLError as e:
            # Handle URL error (e.g., network error, invalid URL)
            self.write(f"URL Error: {e.reason}")
            self.set_status(500)
        except Exception as e:
            # Handle other exceptions
            self.write(f"An error occurred: {str(e)}")
            self.set_status(500)

def make_app():
    """
    Create a Tornado application with the ScrapeHandler.
    """
    return tornado.web.Application([
        (r"/", ScrapeHandler),
    ])

if __name__ == "__main__":
    # Create the application
    app = make_app()

    # Bind the application to port 8888
    app.listen(8888)

    # Start the IOLoop
    tornado.ioloop.IOLoop.current().start()