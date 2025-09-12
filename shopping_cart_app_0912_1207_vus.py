# 代码生成时间: 2025-09-12 12:07:31
import tornado.ioloop
import tornado.web
import json
from tornado.options import define, options

# 定义全局购物车数据存储
shopping_cart = {}

class MainHandler(tornado.web.RequestHandler):
    """首页Handler，展示购物车内容"""
    def get(self):
        cart_id = self.get_secure_cookie("cart_id")
        if not cart_id:
            # 如果没有购物车ID，则创建一个新的购物车
            cart_id = self.set_new_cart()
        self.write(f"Cart: {json.dumps(shopping_cart.get(cart_id, {}))}")

    def set_new_cart(self):
        """创建一个新的购物车"""
        new_cart_id = str(len(shopping_cart) + 1)
        shopping_cart[new_cart_id] = {}
        self.set_secure_cookie("cart_id", new_cart_id)
        return new_cart_id

class AddItemHandler(tornado.web.RequestHandler):
    """添加商品到购物车Handler"""
    def post(self):
        try:
            cart_id = self.get_secure_cookie("cart_id")
            if not cart_id:
                self.set_status(400)
                self.write("购物车ID未找到")
                return
            data = json.loads(self.request.body)
            if not data:
                raise ValueError("无效的商品数据")
            item_id = data.get("item_id")
            quantity = data.get("quantity")
            if not item_id or not quantity or not isinstance(quantity, int):
                self.set_status(400)
                self.write("无效的商品ID或数量")
                return
            if cart_id not in shopping_cart:
                shopping_cart[cart_id] = {}\
            shopping_cart[cart_id][item_id] = quantity
            self.write("商品添加成功")
        except ValueError as e:
            self.set_status(400)
            self.write(str(e))

class RemoveItemHandler(tornado.web.RequestHandler):
    """从购物车删除商品Handler"""
    def post(self):
        try:
            cart_id = self.get_secure_cookie("cart_id")
            if not cart_id:
                self.set_status(400)
                self.write("购物车ID未找到")
                return
            data = json.loads(self.request.body)
            if not data:
                raise ValueError("无效的商品数据")
            item_id = data.get("item_id\)
            if not item_id:
                self.set_status(400)
                self.write("无效的商品ID")
                return
            if cart_id in shopping_cart and item_id in shopping_cart[cart_id]:
                del shopping_cart[cart_id][item_id]
                self.write("商品删除成功")
            else:
                self.set_status(404)
                self.write("商品未找到")
        except ValueError as e:
            self.set_status(400)
            self.write(str(e))

def make_app():
    """创建Tornado应用"""
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/add", AddItemHandler),
        (r"/remove", RemoveItemHandler),
    ])

if __name__ == "__main__":
    define("port", default=8888, help="运行服务的端口", type=int)
    app = make_app()
    app.listen(options.port)
    print(f"Server is running on http://localhost:{options.port}")
    tornado.ioloop.IOLoop.current().start()