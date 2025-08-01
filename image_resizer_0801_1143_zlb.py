# 代码生成时间: 2025-08-01 11:43:39
import os
import tornado.ioloop
import tornado.web
from PIL import Image

# 图片尺寸批量调整器的配置类
class ImageResizerConfig:
    def __init__(self, input_dir, output_dir, target_size):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.target_size = target_size

# 图片尺寸批量调整器的主要逻辑
class ImageResizer:
    def __init__(self, config):
        self.config = config

    def resize_images(self):
        # 遍历输入目录中的所有图片
        for filename in os.listdir(self.config.input_dir):
            file_path = os.path.join(self.config.input_dir, filename)
            if os.path.isfile(file_path):
                try:
                    # 打开图片
                    img = Image.open(file_path)
                    # 调整图片尺寸
                    img = img.resize(self.config.target_size, Image.ANTIALIAS)
                    # 生成输出文件路径
                    output_path = os.path.join(self.config.output_dir, filename)
                    # 保存调整后的图片
                    img.save(output_path)
                except IOError as e:
                    print(f"Error resizing image {filename}: {e}")

# Tornado HTTP 服务器，用于接收调整图片尺寸的请求
class ResizeHandler(tornado.web.RequestHandler):
    def post(self):
        # 解析请求体中的配置信息
        config = ImageResizerConfig(
            input_dir=self.get_body_argument("input_dir"),
            output_dir=self.get_body_argument("output_dir"),
            target_size=tuple(map(int, self.get_body_argument("target_size").split(',')))
        )
        # 创建图片尺寸批量调整器实例并执行调整
        resizer = ImageResizer(config)
        resizer.resize_images()
        # 返回成功响应
        self.write({"status": "success"})

# 定义 Tornado 应用程序
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/resize", ResizeHandler),
        ]
        tornado.web.Application.__init__(self, handlers)

# 启动 Tornado 应用程序
if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    print("Image resizer server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
