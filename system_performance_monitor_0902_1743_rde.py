# 代码生成时间: 2025-09-02 17:43:36
import os
import psutil
import json
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado import gen
# NOTE: 重要实现细节

"""
A simple system performance monitor tool using Python and Tornado framework.
This tool provides CPU, memory, disk usage statistics and network information.
"""

class SystemPerformanceMonitorHandler(RequestHandler):
# 扩展功能模块
    """
    Handles requests to get system performance data.
# NOTE: 重要实现细节
    """

    @gen.coroutine
    def get(self):
        try:
            # Get CPU usage percentage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Get memory usage stats
            mem = psutil.virtual_memory()
# 改进用户体验
            mem_usage = mem.percent
            mem_free = mem.available
            
            # Get disk usage stats
            disk_usage = psutil.disk_usage('/')
            disk_used = disk_usage.percent
            disk_free = disk_usage.free
            
            # Get network stats
            net_io_counters = psutil.net_io_counters()
# TODO: 优化性能
            net_sent = net_io_counters.bytes_sent
            net_received = net_io_counters.bytes_recv
            
            # Prepare the response data
            response_data = {
                'CPU usage': cpu_usage,
                'Memory usage': mem_usage,
# NOTE: 重要实现细节
                'Memory free': mem_free,
                'Disk usage': disk_used,
                'Disk free': disk_free,
# 优化算法效率
                'Network sent': net_sent,
                'Network received': net_received
            }
            
            # Return JSON response
            self.write(json.dumps(response_data))
        except Exception as e:
            # Handle any exceptions and return error response
            self.write(json.dumps({'error': str(e)}))

class SystemPerformanceMonitorApplication(Application):
    """
# 增强安全性
    The main application class for system performance monitor tool.
    """
    def __init__(self):
        handlers = [
            (r"/", SystemPerformanceMonitorHandler),
        ]
        super(SystemPerformanceMonitorApplication, self).__init__(handlers)

if __name__ == '__main__':
    app = SystemPerformanceMonitorApplication()
# 添加错误处理
    app.listen(8888)  # Run the server on port 8888
    print("System performance monitor tool is running on port 8888...")
    IOLoop.current().start()