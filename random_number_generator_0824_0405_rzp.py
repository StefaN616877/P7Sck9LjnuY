# 代码生成时间: 2025-08-24 04:05:28
import tornado.ioloop
import tornado.web
import random
from tornado.options import define, options

# 定义端口号
define('port', default=8888, help='run on the given port', type=int)

class RandomNumberHandler(tornado.web.RequestHandler):
    """
    生成随机数的请求处理器。
    用户可以通过访问 /random?max=<max_value> 来获取一个0到<max_value>之间的随机数。
    如果<max_value>不在查询参数中，则默认为100。
    错误处理：如果参数不是整数，则抛出HTTP 400错误。
    """
    def get(self):
        try:
            # 从查询参数中获取最大值，如果未提供，则默认为100
            max_value = int(self.get_query_argument('max', '100'))
        except ValueError:
            # 如果参数不是整数，则返回400错误
            self.set_status(400)
            self.write("The 'max' parameter must be an integer.")
            return

        # 生成一个0到max_value之间的随机数
        random_number = random.randint(0, max_value)
        # 将随机数作为响应返回
        self.write({'random_number': random_number})

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/random', RandomNumberHandler)
        ]
        settings = dict(
            debug=True,  # 开启调试模式
        )
        super(Application, self).__init__(handlers, **settings)

def main():
    application = Application()
    options.parse_command_line()
    application.listen(options.port)
    print(f"Server is running on http://localhost:{options.port}")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
