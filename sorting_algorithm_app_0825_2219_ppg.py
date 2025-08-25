# 代码生成时间: 2025-08-25 22:19:11
import tornado.ioloop
import tornado.web
import json

# 一个简单的排序算法实现，这里以冒泡排序为例
def bubble_sort(arr):
    """实现冒泡排序算法。
    参数:
    arr (list): 需要排序的列表。
    返回:
    list: 排序后的列表。
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

class SortingHandler(tornado.web.RequestHandler):
    """处理排序请求的Handler。"""
    def post(self):
        """处理POST请求。
        通过JSON接收一个列表，返回排序后的列表。
        """
        try:
            data = json.loads(self.request.body)
            if not isinstance(data, list):
                raise ValueError("输入数据必须是列表。")
            sorted_data = bubble_sort(data)
            self.write(json.dumps({'sorted_list': sorted_data}))
        except json.JSONDecodeError:
            self.write(json.dumps({'error': '无效的JSON格式。'}))
            self.set_status(400)
        except ValueError as e:
            self.write(json.dumps({'error': str(e)}))
            self.set_status(400)

def make_app():
    """创建Tornado应用。"""
    return tornado.web.Application([
        (r"/sort", SortingHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("服务器启动，监听8888端口...")
    tornado.ioloop.IOLoop.current().start()