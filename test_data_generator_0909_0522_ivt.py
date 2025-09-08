# 代码生成时间: 2025-09-09 05:22:00
# 测试数据生成器
# 使用Tornado框架创建一个简单的HTTP服务，生成测试数据

import tornado.ioloop
import tornado.web
import json
import random
import string

# 测试数据生成器类
class TestDataGenerator:
    def generate_data(self, count):
        """
        生成指定数量的随机测试数据
        """
        data = []
        for _ in range(count):
            name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
            age = random.randint(18, 60)
            gender = random.choice(['Male', 'Female'])
            data.append({'name': name, 'age': age, 'gender': gender})
        return data

# Tornado请求处理类
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """
        处理GET请求，返回随机生成的测试数据
        """
        try:
            count = int(self.get_argument('count', 10))  # 默认生成10条数据
            data_generator = TestDataGenerator()
            data = data_generator.generate_data(count)
            self.write(json.dumps(data))
        except ValueError:
            self.set_status(400)
            self.write(json.dumps({'error': 'Invalid count value'}))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'error': str(e)}))

# 定义Tornado应用
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)  # 监听端口8888
    print('Server started on http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()