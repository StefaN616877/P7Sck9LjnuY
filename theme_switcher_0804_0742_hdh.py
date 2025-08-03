# 代码生成时间: 2025-08-04 07:42:06
# theme_switcher.py

import tornado.web
import tornado.ioloop
import tornado.options
import json

# 定义主题类，用于处理主题相关逻辑
class ThemeManager:
    def __init__(self):
        self.themes = {"light": "Light Theme", "dark": "Dark Theme"}

    def set_theme(self, user_id, theme_name):
        """
        设置用户主题
        :param user_id: 用户标识
        :param theme_name: 主题名称
        :return: 主题设置结果
        """
        if theme_name in self.themes:
            print(f"User {user_id} theme set to {self.themes[theme_name]}")
            return True
        else:
            print(f"Theme {theme_name} not found for user {user_id}")
            return False

# 设置Tornado选项
def set_options():
    tornado.options.define("port", default=8888, help="run on the given port", type=int)

# 主页处理类
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to Theme Switcher!")

# 设置主题处理类
class ThemeHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            body = json.loads(self.request.body)
            user_id = body.get("user_id")
            theme_name = body.get("theme_name")
            if user_id and theme_name:
                theme_manager = ThemeManager()
                if theme_manager.set_theme(user_id, theme_name):
                    self.write("Theme set successfully")
                else:
                    self.set_status(404)
                    self.write("Theme not found")
            else:
                self.set_status(400)
                self.write("Missing user_id or theme_name in request")
        except json.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON payload")

# 定义Tornado路由
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/set_theme", ThemeHandler),
    ])

if __name__ == "__main__":
    set_options()
    options = tornado.options.options
    app = make_app()
    app.listen(options.port)
    print(f"Server started on http://localhost:{options.port}")
    tornado.ioloop.IOLoop.current().start()