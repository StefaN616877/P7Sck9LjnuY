# 代码生成时间: 2025-10-08 03:36:23
import os
import base64
from tornado.web import RequestHandler, Application
from PIL import Image, ImageDraw, ImageFont
import numpy as np

"""
数字水印技术实现，使用Tornado框架作为服务端。
这个程序允许用户上传图片，然后在图片上添加数字水印，最后返回水印后的图片。
"""

class WatermarkHandler(RequestHandler):
    """处理数字水印的添加"""
    def post(self):
        try:
            # 获取上传的图片文件
            file = self.request.files["image"][0]
            image_data = file['body']

            # 解码图片
            image = Image.open(io.BytesIO(image_data))
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()

            # 添加数字水印
            watermark_text = "Watermark"  # 这里可以自定义水印文本
            draw.text((10, 10), text=watermark_text, font=font, fill=(255, 255, 255, 128))
            watermarked_image = image

            # 将水印图片转换为base64
            buffered = io.BytesIO()
            watermarked_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # 响应客户端
            self.write({
                "success": True,
                "image": img_str
            })
        except Exception as e:
            # 错误处理
            self.write({
                "success": False,
                "error": str(e)
            })

def make_app():
    """创建Tornado应用"""
    return Application(
        [
            (r"/watermark", WatermarkHandler),
        ],
        debug=True
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
