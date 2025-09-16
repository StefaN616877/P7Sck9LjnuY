# 代码生成时间: 2025-09-16 17:40:09
import os
import tornado.ioloop
import tornado.web
from PIL import Image
from tornado.options import define, options

# Define the maximum allowed file size
define("max_size", default=10485760)  # 10 MB

# Define the default output size
define("output_size", default="800x600")  # 800x600 pixels

class UploadHandler(tornado.web.RequestHandler):
    """
    A handler for uploading images and resizing them.
    """
    def post(self):
        # Check if the client sent a file
        fileinfo = self.request.files.get("file", None)
        if not fileinfo:
            self.set_status(400)
            self.write("No file uploaded.")
            return

        # Check file size
        file = fileinfo[0]  # Get the first file
        if file['body'].tell() > options.max_size:
            self.set_status(413)  # Request Entity Too Large
            self.write("File too large.")
            return

        # Attempt to open the image
        try:
            image = Image.open(file['body'])
        except IOError:
            self.set_status(400)
            self.write("Invalid image file.")
            return

        # Resize the image
        self.resize_image(image, file['filename'])

    def resize_image(self, image, filename):
        # Split the output size into width and height
        width, height = map(int, options.output_size.split('x'))

        # Resize the image
        resized_image = image.resize((width, height), Image.ANTIALIAS)

        # Save the resized image
        resized_filename = f"resized_{filename}"
        resized_image.save(resized_filename)

        # Write the result to the response
        self.write(f"Image resized to {resized_filename}")
        self.set_header("Content-Type", "text/plain")

class Application(tornado.web.Application):
    def __init__(self):
        # Define the handlers
        handlers = [
            (r"/upload", UploadHandler),
        ]
        super(Application, self).__init__(handlers)

if __name__ == "__main__":
    # Parse command line options
    tornado.options.parse_command_line()

    # Start the application
    app = Application()
    app.listen(8888)
    print("Server started on http://localhost:8888")

    # Start the IOLoop
    tornado.ioloop.IOLoop.current().start()