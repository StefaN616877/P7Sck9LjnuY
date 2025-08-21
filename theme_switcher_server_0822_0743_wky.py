# 代码生成时间: 2025-08-22 07:43:45
import tornado.ioloop
import tornado.web

# 定义一个全局变量来存储主题
current_theme = 'default'

class ThemeHandler(tornado.web.RequestHandler):
    """
    处理主题切换请求的处理器
    """
    def get(self):
        # 获取请求参数，主题名称
        theme_name = self.get_argument('theme', None)

        # 检查主题是否存在
        if theme_name and theme_name in ['default', 'dark', 'light']:
            # 更新全局主题变量
            global current_theme
            current_theme = theme_name
            # 响应成功消息
            self.write(f"Theme switched to {current_theme}")
        else:
            # 如果请求的主题不存在，返回错误消息
            self.set_status(400)
            self.write("Invalid theme requested")

    def set_default_headers(self):
        # 设置响应头，允许跨域请求
        self.set_header("Access-Control-Allow-Origin\, "*")

class MainHandler(tornado.web.RequestHandler):
    """
    主页处理器，显示当前主题
    """
    def get(self):
        # 响应当前主题
        self.write(f"Current theme is {current_theme}")

def make_app():
    """
    创建Tornado应用
    """
    return tornado.web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/switch_theme", ThemeHandler),
        ],
        debug=True,
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on port 8888")
    tornado.ioloop.IOLoop.current().start()