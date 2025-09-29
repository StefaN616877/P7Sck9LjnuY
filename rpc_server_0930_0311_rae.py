# 代码生成时间: 2025-09-30 03:11:19
import tornado.ioloop
import tornado.web
import json
from concurrent import futures
import datetime

def rpc_handler(request):
    # 处理RPC请求
    try:
        data = json.loads(request.body)
        func_name = data['func']
        args = data['args'] if 'args' in data else ()
        kwargs = data['kwargs'] if 'kwargs' in data else {}
        # 动态调用函数
        result = globals().get(func_name)(*args, **kwargs)
        return json.dumps({'result': result}, indent=4)
    except Exception as e:
        return json.dumps({'error': str(e)}, indent=4)

class RpcHandler(tornado.web.RequestHandler):
    def post(self):
        # 处理POST请求
        self.write(rpc_handler(self.request))

def get_current_time():
    # 返回当前时间
    return datetime.datetime.now()

def add_numbers(a, b):
    # 返回两个数的和
    return a + b

def main():
    # 设置路由，启动服务
    application = tornado.web.Application([
        (r"/rpc", RpcHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
