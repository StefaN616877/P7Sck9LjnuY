# 代码生成时间: 2025-09-23 18:34:33
import tornado.ioloop
import tornado.web
import json

# ShoppingCart class to handle cart operations
class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, item_id, quantity):
        """Adds an item to the cart or updates its quantity."""
        if item_id in self.items:
            self.items[item_id] += quantity
        else:
            self.items[item_id] = quantity

    def remove_item(self, item_id):
        """Removes an item from the cart."""
        if item_id in self.items:
            del self.items[item_id]
        else:
            raise KeyError("Item not found in cart.")

    def get_cart(self):
        """Returns the current state of the cart."""
        return self.items

# Request handler for adding items to the cart
class AddItemHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            item_id = data.get('item_id')
            quantity = data.get('quantity')

            if not item_id or not quantity:
                self.set_status(400)
                self.write({'error': 'Item ID and quantity are required.'})
                return

            cart.add_item(item_id, quantity)
            self.write({'message': 'Item added to cart.'})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({'error': 'Invalid JSON payload.'})

# Request handler for removing items from the cart
class RemoveItemHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            item_id = data.get('item_id')

            if not item_id:
                self.set_status(400)
                self.write({'error': 'Item ID is required.'})
                return

            cart.remove_item(item_id)
            self.write({'message': 'Item removed from cart.'})
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({'error': 'Invalid JSON payload.'})

# Request handler for getting the cart contents
class GetCartHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            cart_contents = cart.get_cart()
            self.write({'cart': cart_contents})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

# Application setup
def make_app():
    return tornado.web.Application([
        (r"/add_item", AddItemHandler),
        (r"/remove_item", RemoveItemHandler),
        (r"/get_cart", GetCartHandler),
    ])

# Global cart instance
cart = ShoppingCart()

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()