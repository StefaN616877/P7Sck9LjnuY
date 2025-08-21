# 代码生成时间: 2025-08-22 01:04:20
import os
import tornado.ioloop
import tornado.web
from PIL import Image
from tornado.options import define, options

# 定义允许的图片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# 定义最大文件大小（单位：MB）
MAX_FILE_SIZE = 10

# 设置Tornado选项
define('port', default=8888, help='运行服务的端口', type=int)

class ImageResizerHandler(tornado.web.RequestHandler):
    """处理图片尺寸调整请求的Handler"""
    def get(self):
        self.render('image_upload.html')

    def post(self):
        # 获取上传的文件
        file = self.request.files['file'][0]
        file_name = file['filename']
        file_type = file_name.split('.')[-1].lower()

        # 检查文件类型是否被允许
        if file_type not in ALLOWED_EXTENSIONS:
            self.write({'error': '不支持的文件类型'})
            return

        # 检查文件大小是否超过限制
        if file.size > MAX_FILE_SIZE * 1024 * 1024:
            self.write({'error': '文件大小超过限制'})
            return

        # 尝试打开图片
        try:
            image = Image.open(file['body'])
        except IOError:
            self.write({'error': '无法打开图片文件'})
            return

        # 获取原始图片尺寸
        original_width, original_height = image.size

        # 提示用户输入新的尺寸或者比例
        new_width = self.get_argument('new_width', type=int)
        new_height = self.get_argument('new_height', type=int)

        # 检查新尺寸是否有效
        if new_width is None or new_height is None:
            self.write({'error': '请提供新的尺寸'})
            return

        # 调整图片尺寸
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

        # 保存调整后的图片
        resized_image.save('resized_image.' + file_type)
        self.write({'message': '图片尺寸调整成功', 'new_size': (new_width, new_height)})

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', ImageResizerHandler),
        ]
        super(Application, self).__init__(handlers)

if __name__ == '__main__':
    options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print(f'服务正在运行在 http://localhost:{options.port}')
    tornado.ioloop.IOLoop.current().start()