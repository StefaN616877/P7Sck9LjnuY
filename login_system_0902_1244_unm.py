# 代码生成时间: 2025-09-02 12:44:05
import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.options
import tornado.httpserver
import bcrypt
import json
from bson import ObjectId
from pymongo import MongoClient
from tornado.options import define, options

# Define options
define("port", default=8888, help="run on the given port", type=int)

# MongoDB connection setup
class MongoConnection:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["UserDB"]
        self.collection = self.db["users"]

    def get_user(self, username):
        return self.collection.find_one({"username": username})

    def insert_user(self, user_data):
        self.collection.insert_one(user_data)

# User authentication handler
class AuthHandler(tornado.web.RequestHandler):
    def initialize(self, mongo_connection):
        self.mongo_connection = mongo_connection

    @tornado.gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body.decode("utf-8"))
            username = data["username"]
            password = data["password"]

            user = self.mongo_connection.get_user(username)
            if user:
                if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
                    self.write(json.dumps({"message": "Login successful", "user": user}))
                    self.set_status(200)
                else:
                    self.set_status(401)
                    self.write(json.dumps({"error": "Invalid credentials"}))
            else:
                self.set_status(404)
                self.write(json.dumps({"error": "User not found"}))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))

# Application setup
def make_app():
    mongo_connection = MongoConnection()
    return tornado.web.Application([
        (r"/login", AuthHandler, dict(mongo_connection=mongo_connection)),
    ])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print(f"Server running on port {options.port}")
    tornado.ioloop.IOLoop.current().start()