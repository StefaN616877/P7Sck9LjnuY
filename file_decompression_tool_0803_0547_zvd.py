# 代码生成时间: 2025-08-03 05:47:43
import os
import zipfile
import logging
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

# 设置日志记录
logging.basicConfig(level=logging.INFO)


class DecompressionHandler(RequestHandler):
    """
    处理文件解压的Handler。
    """
    def post(self):
        # 获取上传的文件
        file_info = self.request.files.get('file')
        if not file_info:
            self.set_status(400)
            self.write("No file uploaded.")
            return

        file = file_info[0]  # 取出文件
        filename = file['filename']
        file_path = os.path.join('temp', filename)
        with open(file_path, 'wb') as f:
            f.write(file['body'])

        try:
            # 解压文件
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall('extracted_files')
            self.write("File decompressed successfully.")
        except zipfile.BadZipFile:
            self.set_status(400)
            self.write("The uploaded file is not a valid zip file.")
        except Exception as e:
            self.set_status(500)
            self.write(f"An error occurred: {str(e)}")
        finally:
            # 清理临时文件
            os.remove(file_path)


def make_app():
    """
    创建Tornado应用程序。
    """
    return Application(
        [
            (r"/decompress", DecompressionHandler),
        ]
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()
