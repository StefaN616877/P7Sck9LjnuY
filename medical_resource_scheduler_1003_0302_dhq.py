# 代码生成时间: 2025-10-03 03:02:43
import tornado.ioloop
import tornado.web
import json

"""
医疗资源调度程序使用Tornado框架创建。
这个程序提供一个简单的HTTP接口来处理医疗资源分配请求。
"""

class MedicalResourceScheduler:
    def __init__(self):
        # 医疗资源的初始状态
        self.resources = {}

    def add_resource(self, resource_name, amount):
        """ 添加或更新资源及其数量 
        Args:
            resource_name (str): 资源名称
            amount (int): 资源数量
        """
        if resource_name in self.resources:
            self.resources[resource_name] += amount
        else:
            self.resources[resource_name] = amount

    def allocate_resource(self, resource_name, amount):
        """ 分配资源，如果资源不足则抛出异常 
        Args:
            resource_name (str): 资源名称
            amount (int): 需要分配的资源数量
        Returns:
            int: 分配后剩余的资源数量
        Raises:
            Exception: 资源不足时抛出异常
        """
        if resource_name not in self.resources:
            raise Exception(f"Resource {resource_name} not available.")
        if self.resources[resource_name] < amount:
            raise Exception(f"Not enough {resource_name} available.")
        self.resources[resource_name] -= amount
        return self.resources[resource_name]

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, scheduler):
        self.scheduler = scheduler

    def post(self):
        """ 处理资源调度请求 
        """
        try:
            request_data = json.loads(self.request.body)
            resource_name = request_data.get('resource_name')
            amount = request_data.get('amount')
            if not resource_name or not amount:
                self.write({
                    'error': 'Resource name and amount are required.'
                })
                return
            remaining = self.scheduler.allocate_resource(resource_name, amount)
            self.write({
                'success': True,
                'remaining': remaining
            })
        except Exception as e:
            self.write({'error': str(e)})

def make_app():
    scheduler = MedicalResourceScheduler()
    # 初始添加一些资源
    scheduler.add_resource('oxygen_tanks', 100)
    scheduler.add_resource('ventilators', 50)
    return tornado.web.Application([
        (r"/allocate", MainHandler, dict(scheduler=scheduler)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()