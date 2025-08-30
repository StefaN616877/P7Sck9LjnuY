# 代码生成时间: 2025-08-30 14:36:50
import tornado.ioloop
import tornado.web
import schedule
import time

"""
定时任务调度器服务，使用Tornado框架实现。
提供简单的定时任务调度功能，可以方便地添加、删除定时任务。
"""

def hello():
    """
    简单的定时任务，打印Hello World。
    """
    print("Hello World!")


def start_scheduler():
    """
    启动定时任务调度器。
    """
    # 定义定时任务：每10秒执行一次hello函数
    schedule.every(10).seconds.do(hello)

    # 启动调度器
    while True:
        schedule.run_pending()
        time.sleep(1)

class MainHandler(tornado.web.RequestHandler):
    """
    主请求处理器，用于启动定时任务调度器。
    """
    def get(self):
        self.write("定时任务调度器启动成功！")

        # 启动调度器线程
        import threading
        threading.Thread(target=start_scheduler).start()

def make_app():
    """
    创建Tornado应用程序。
    """
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
