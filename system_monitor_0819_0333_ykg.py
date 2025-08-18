# 代码生成时间: 2025-08-19 03:33:06
import psutil
import json
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

"""
系统性能监控工具
这个程序使用Python和Tornado框架来监控系统性能指标。
它可以作为一个HTTP服务器运行，提供API来获取CPU、内存和磁盘使用情况。
"""

class SystemStatsHandler(RequestHandler):
    """
    处理系统性能监控请求的请求处理器
    """
    def get(self):
        try:
            # 获取CPU使用率
            cpu_usage = psutil.cpu_percent(interval=1)
            # 获取内存使用率
            memory_usage = psutil.virtual_memory().percent
            # 获取磁盘使用率
            disk_usage = psutil.disk_usage('/').percent

            # 构建响应数据
            stats = {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage
            }

            # 将响应数据转换为JSON格式
            self.write(json.dumps(stats))
        except Exception as e:
            # 处理错误
            self.write(json.dumps({'error': str(e)}))

def make_app():
    """
    创建Tornado应用程序
    """
    return Application(
        [
            (r"/stats", SystemStatsHandler),
        ],
        debug=True
    )

if __name__ == "__main__":
    # 创建并启动Tornado应用程序
    app = make_app()
    app.listen(8888)
    print("System monitor server is running on http://localhost:8888")
    IOLoop.current().start()
