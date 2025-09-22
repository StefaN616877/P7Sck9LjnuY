# 代码生成时间: 2025-09-22 15:25:12
import tornado.ioloop
import tornado.web
import hashlib
import json

"""
Hash Calculator Application using Tornado Framework.
This application provides an endpoint for calculating hash values.
"""

class HashCalculatorHandler(tornado.web.RequestHandler):
    """
    Handler for calculating hash values.
    """
    def post(self):
        try:
            # Parse the JSON request body
            data = json.loads(self.request.body)
            # Check if the 'text' key is present in the request data
            if 'text' not in data:
                raise ValueError('Missing text key in request data')

            # Calculate the hash value using SHA-256
            hash_value = hashlib.sha256(data['text'].encode()).hexdigest()

            # Return the hash value in the response
            self.write({'hash': hash_value})
        except ValueError as e:
            # Handle missing 'text' key error
            self.set_status(400)
            self.write({'error': str(e)})
        except Exception as e:
            # Handle any other errors
            self.set_status(500)
            self.write({'error': 'Internal Server Error'})

class Application(tornado.web.Application):
    """
    Tornado application setup.
    """
    def __init__(self):
        handlers = [
            (r"/hash", HashCalculatorHandler),
        ]
        tornado.web.Application.__init__(self, handlers)

def main():
    """
    Main function to run the Tornado application.
    """
    app = Application()
    app.listen(8888)
    print("Hash Calculator App is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()