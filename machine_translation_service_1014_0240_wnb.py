# 代码生成时间: 2025-10-14 02:40:20
import tornado.ioloop
import tornado.web
from googletrans import Translator, LANGUAGES


class MachineTranslationHandler(tornado.web.RequestHandler):
    """Handler for machine translation requests."""
    def get(self):
        try:
            # Parsing query parameters from the request
            source_text = self.get_query_argument('text')
            target_language = self.get_query_argument('lang')

            # Validate the input parameters
            if not source_text or not target_language:
                self.set_status(400)
                self.write({'error': 'Missing required parameters'})
                return

            # Translate the text using the translator
            translator = Translator()
            result = translator.translate(source_text, dest=target_language)

            # Send the translated text back as a response
            self.write({'translatedText': result.text})
        except Exception as e:
            # Handle any unexpected errors
            self.set_status(500)
            self.write({'error': str(e)})


class Application(tornado.web.Application):
    """Main application class."""
    def __init__(self):
        handlers = [
            (r"/translate", MachineTranslationHandler),
        ]
        settings = dict(
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    """Main function to start the Tornado application."""
    application = Application()
    application.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
