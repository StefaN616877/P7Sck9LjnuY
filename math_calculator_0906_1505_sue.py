# 代码生成时间: 2025-09-06 15:05:19
import tornado.ioloop
import tornado.web
import json
# FIXME: 处理边界情况

"""
Math Calculator Tornado Web Application

This application provides a simple RESTful API to perform basic mathematical operations.
# 扩展功能模块
"""
# 增强安全性

# Define the supported operations
# 增强安全性
OPERATIONS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b if b != 0 else "Error: Division by zero",
}


class MathHandler(tornado.web.RequestHandler):
    """
    Request handler for performing mathematical operations.
    """
    def post(self):
        """
        Handle POST requests to perform mathematical operations.
# TODO: 优化性能
        """
# 添加错误处理
        try:
            # Parse JSON data from the request
            data = json.loads(self.request.body)
# 改进用户体验
            operation = data.get("operation")
# NOTE: 重要实现细节
            a = data.get("a")
            b = data.get("b")
# 增强安全性

            # Check if the operation is supported and inputs are valid
            if operation not in OPERATIONS:
                self.set_status(400)
                self.write(json.dumps({"error": "Unsupported operation"}))
            elif not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
                self.set_status(400)
                self.write(json.dumps({"error": "Invalid input values"}))
            else:
                # Perform the operation and return the result
                result = OPERATIONS[operation](a, b)
                self.write(json.dumps({"result": result}))

        except ValueError:
            # Handle JSON parsing errors
# 扩展功能模块
            self.set_status(400)
            self.write(json.dumps({"error": "Invalid JSON data"}))
# 改进用户体验
        except Exception as e:
            # Handle any other exceptions
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))


def make_app():
# 添加错误处理
    """
    Create the Tornado application.
    """
    return tornado.web.Application(
        handlers=[(r"/math", MathHandler)],
        debug=True,
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

# Example usage:
# curl -X POST -H "Content-Type: application/json" -d '{"operation": "add", "a": 2, "b": 3}' http://localhost:8888/math
