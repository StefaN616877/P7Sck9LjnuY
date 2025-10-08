# 代码生成时间: 2025-10-09 03:44:22
import tornado.ioloop
import tornado.web
from datetime import datetime

# 模拟的智能家居设备状态，可以扩展为数据库存储
SMART_DEVICES = {
    'light': {'status': 'off', 'last_updated': datetime.now()},
    'thermostat': {'temperature': 22, 'last_updated': datetime.now()},
    'security_system': {'status': 'armed', 'last_updated': datetime.now()},
}

# 错误处理类
class SmartHomeError(Exception):
    pass

class DeviceNotFoundError(SmartHomeError):
    pass

# 设备控制接口
class DeviceController:
    def __init__(self, device_name):
        self.device_name = device_name

    # 检查设备是否存在
    def device_exists(self):
        if self.device_name not in SMART_DEVICES:
            raise DeviceNotFoundError(f"Device {self.device_name} not found.")

    # 更新设备状态
    def update_device_status(self, new_status):
        self.device_exists()
        SMART_DEVICES[self.device_name]['last_updated'] = datetime.now()
        SMART_DEVICES[self.device_name]['status'] = new_status
        return SMART_DEVICES[self.device_name]

# Tornado 路由和请求处理
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to the Smart Home Controller!")

class DeviceHandler(tornado.web.RequestHandler):
    def get(self, device_name):
        try:
            device_controller = DeviceController(device_name)
            device_status = device_controller.update_device_status('on')
            self.write(f"Device {device_name} status updated to {device_status['status']}")
        except DeviceNotFoundError as e:
            self.set_status(404)
            self.write(str(e))

# 应用配置
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/device/([^/]+)", DeviceHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Smart Home Controller is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()