# 代码生成时间: 2025-09-28 23:06:31
import tornado.ioloop
import tornado.web
import json

# 排序算法实现
class SortingAlgorithmHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            # 获取请求体中的JSON数据
            data = json.loads(self.request.body)
            # 提取需要排序的列表
            numbers = data.get('numbers')
            # 检查列表是否为空，若为空则返回错误信息
            if not numbers:
                self.set_status(400)
                self.write(json.dumps({'error': 'Empty list provided'}))
                return
            # 调用排序函数
            sorted_numbers = self.sort_numbers(numbers)
            # 将排序后的结果返回给客户端
            self.write(json.dumps({'sorted_numbers': sorted_numbers}))
        except json.JSONDecodeError:
            self.set_status(400)
            self.write(json.dumps({'error': 'Invalid JSON data'}))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'error': str(e)}))

    @staticmethod
    def sort_numbers(numbers):
        # 简单的冒泡排序算法实现
        for i in range(len(numbers) - 1):
            for j in range(0, len(numbers) - i - 1):
                if numbers[j] > numbers[j + 1]:
                    # 交换元素位置
                    numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
        return numbers

# 应用配置
def make_app():
    return tornado.web.Application([
        (r"/sort", SortingAlgorithmHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()