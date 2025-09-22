# 代码生成时间: 2025-09-23 06:31:58
import tornado.ioloop
import tornado.web
from tornado.options import define, options

# 定义全局变量
class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, item_id, quantity):
        """
        向购物车添加商品

        :param item_id: 商品ID
        :param quantity: 商品数量
        """
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity

    def remove_item(self, item_id):
        """
        从购物车移除商品

        :param item_id: 商品ID
        """
        if item_id in self.items:
            del self.items[item_id]

    def get_cart(self):
        """
        获取购物车中的商品列表

        :return: 购物车商品列表
        """
        return self.items

class CartHandler(tornado.web.RequestHandler):
    def initialize(self, cart):
        self.cart = cart

    def get(self):
        """
        获取购物车信息
        """
        try:
            cart_items = self.cart.get_cart()
            self.write({'status': 'success', 'data': cart_items})
        except Exception as e:
            self.write({'status': 'error', 'error': str(e)})

    def post(self):
        """
        添加商品到购物车
        """
        try:
            item_id = self.get_argument('item_id')
            quantity = int(self.get_argument('quantity'))
            self.cart.add_item(item_id, quantity)
            self.write({'status': 'success', 'message': 'Item added to cart'})
        except Exception as e:
            self.write({'status': 'error', 'error': str(e)})

    def delete(self):
        """
        从购物车移除商品
        """
        try:
            item_id = self.get_argument('item_id')
            self.cart.remove_item(item_id)
            self.write({'status': 'success', 'message': 'Item removed from cart'})
        except Exception as e:
            self.write({'status': 'error', 'error': str(e)})

def make_app():
    """
    创建Tornado应用程序
    """
    return tornado.web.Application([
        (r"/cart", CartHandler, dict(cart=Cart())),
    ])

if __name__ == "__main__":
    define("port", default=8888, help="run on the given port")
    app = make_app()
    app.listen(options.port)
    print("Starting server at http://localhost:%d" % options.port)
    tornado.ioloop.IOLoop.current().start()