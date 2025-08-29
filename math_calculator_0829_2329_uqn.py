# 代码生成时间: 2025-08-29 23:29:55
import tornado.ioloop
import tornado.web
import json

"""
A simple math calculator Tornado web service that provides basic mathematical operations.
"""

# Define a class for the math calculator application
class MathCalculatorHandler(tornado.web.RequestHandler):
# 改进用户体验
    def post(self):
        # Parse the JSON data from the request
        try:
# 添加错误处理
            request_data = json.loads(self.request.body)
            # Check if the required keys are present
            operation = request_data.get('operation')
            operand1 = request_data.get('operand1')
            operand2 = request_data.get('operand2')
# 改进用户体验
            
            # Perform the operation based on the input
            if operation == 'add':
                result = self.add(operand1, operand2)
# NOTE: 重要实现细节
            elif operation == 'subtract':
                result = self.subtract(operand1, operand2)
            elif operation == 'multiply':
                result = self.multiply(operand1, operand2)
            elif operation == 'divide':
                result = self.divide(operand1, operand2)
            else:
                self.set_status(400)
                self.write(json.dumps({'error': 'Invalid operation'}))
                return
# 添加错误处理
            
            # Return the result as a JSON response
            self.write(json.dumps({'result': result}))
        except json.JSONDecodeError:
            self.set_status(400)
            self.write(json.dumps({'error': 'Invalid JSON format'}))
# 添加错误处理
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'error': str(e)}))

    # Define the mathematical operations
    def add(self, operand1, operand2):
        """Add two operands."""
        return operand1 + operand2

    def subtract(self, operand1, operand2):
        """Subtract the second operand from the first."""
        return operand1 - operand2

    def multiply(self, operand1, operand2):
# FIXME: 处理边界情况
        """Multiply two operands."""
        return operand1 * operand2

    def divide(self, operand1, operand2):
        """Divide the first operand by the second.
# 增强安全性
        Raise a ValueError if the second operand is zero."""
        if operand2 == 0:
            raise ValueError('Cannot divide by zero')
        return operand1 / operand2

# Define the URL route and the handler
def make_app():
    return tornado.web.Application([
        (r"/calculate", MathCalculatorHandler),
    ])

# Run the Tornado IOLoop if this script is executed directly
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Math calculator server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()