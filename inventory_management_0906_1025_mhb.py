# 代码生成时间: 2025-09-06 10:25:48
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import json

# Define the application settings
define("port", default=8888, help="run on the given port", type=int)

class InventoryItem:
    """Represents an item in the inventory."""
    def __init__(self, item_id, name, quantity):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity

class InventoryManager:
    """Manages inventory items."""
    def __init__(self):
        self.items = {}

    def add_item(self, item_id, name, quantity):
        """Adds a new item to the inventory."""
        if item_id in self.items:
            raise ValueError(f"Item with ID {item_id} already exists.")
        self.items[item_id] = InventoryItem(item_id, name, quantity)

    def update_item_quantity(self, item_id, quantity):
        "