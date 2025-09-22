# 代码生成时间: 2025-09-22 23:53:37
import os
import zipfile
import logging
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

# 设置日志记录
logging.basicConfig(level=logging.INFO)


class UnzipHandler(RequestHandler):
    """处理文件解压的请求。"""
    def post(self):
        # 获取上传的文件
        file_info = self.request.files['file'][0]
        file_path = file_info['filename']
        file_content = file_info['body']
        
        # 写入临时文件
        temp_file_path = f'/tmp/{file_path}'
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(file_content)
        
        try:
            # 解压文件
            self.unzip_file(temp_file_path, f'./unzipped/{file_path}')
            
            # 返回成功响应
            self.write({'status': 'success', 'message': 'File has been successfully unzipped'})
        except zipfile.BadZipFile:
            # 处理压缩文件损坏的错误
            self.write({'status': 'error', 'message': 'The file is not a zip file or it is corrupt'})
        except Exception as e:
            # 处理其他错误
            logging.error(f'An error occurred: {e}')
            self.write({'status': 'error', 'message': 'An unexpected error occurred'})
        finally:
            # 删除临时文件
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            
    def unzip_file(self, zip_path, extract_path):
        """解压zip文件到指定目录。"""
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)


def make_app():
    """创建Tornado应用。"""
    return Application([
        (r"/unzip", UnzipHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    logging.info("Server is running on http://localhost:8888")
    IOLoop.current().start()
