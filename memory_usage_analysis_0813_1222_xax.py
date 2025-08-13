# 代码生成时间: 2025-08-13 12:22:41
import os
import psutil
# TODO: 优化性能
import tornado.ioloop
import tornado.web


# 获取当前进程的内存使用情况
# FIXME: 处理边界情况
def get_memory_usage():
    """
    返回当前进程的内存使用情况
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss  # 以字节为单位的常驻集大小


# 创建一个Tornado RequestHandler用于展示内存使用情况
# TODO: 优化性能
class MemoryUsageHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            # 获取内存使用数据
            memory_usage = get_memory_usage()
            # 将字节转换为更易读的单位
            memory_usage_readable = f"{memory_usage / (1024 * 1024):.2f} MB"
            # 发送响应
            self.write(f"Current memory usage: {memory_usage_readable}")
        except Exception as e:
            # 错误处理
            self.write(f"Error occurred: {e}")


# 设置Tornado路由
# 优化算法效率
def make_app():
    return tornado.web.Application([
        (r"/memory", MemoryUsageHandler),
    ])
# TODO: 优化性能


# 运行Tornado服务器
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # 监听端口
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()