# 代码生成时间: 2025-08-11 18:22:28
import tornado.ioloop
import tornado.web

def add(x, y):
    """Add two numbers."""
    return x + y

def subtract(x, y):
    """Subtract two numbers."""
    return x - y

def multiply(x, y):
    """Multiply two numbers."""
    return x * y

def divide(x, y):
    """Divide two numbers."""
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def handle_request(self):
    """Handle HTTP request and perform the calculation."""
    try:
        x = float(self.get_argument("x"))
        y = float(self.get_argument("y"))
        operation = self.get_argument("operation")
        if operation == "add":
            result = add(x, y)
        elif operation == "subtract":
            result = subtract(x, y)
        elif operation == "multiply":
            result = multiply(x, y)
        elif operation == "divide":
            result = divide(x, y)
        else:
            self.write("Invalid operation.")
            self.set_status(400)
            return
        self.write(f"{{"result": {result}}}")
    except ValueError as e:
        self.write(f"{{"error": "{e}"}}")
        self.set_status(400)

def make_app():
    """Create a Tornado web application."""
    return tornado.web.Application(
        [
            (r"/calculate", CalcHandler),
        ]
    )

def main():
    """Run the Tornado web application."""
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

class CalcHandler(tornado.web.RequestHandler):
    """HTTP handler for the calculator."""
    def get(self):
        handle_request(self)

if __name__ == "__main__":
    main()