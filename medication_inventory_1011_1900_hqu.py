# 代码生成时间: 2025-10-11 19:00:47
# medication_inventory.py
# A simple medication inventory management system using the Tornado framework.

import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
import json

# Define command line options
define("port", default=8888, help="run on the given port", type=int)

# Medication Inventory Data Structure
class MedicationInventory:
    def __init__(self):
        self.inventory = {}

    def add_medication(self, name, quantity):
        """Add medication to the inventory."""
        if name in self.inventory:
            self.inventory[name] += quantity
        else:
            self.inventory[name] = quantity

    def remove_medication(self, name, quantity):
        """Remove medication from the inventory."""
        if name in self.inventory and self.inventory[name] >= quantity:
            self.inventory[name] -= quantity
        else:
            raise ValueError("Not enough medication in inventory.")

    def get_inventory(self):
        """Get the current inventory."""
        return self.inventory

# Tornado Request Handlers
class InventoryHandler(tornado.web.RequestHandler):
    def initialize(self, inventory):
        self.inventory = inventory

    def post(self):
        "