# 代码生成时间: 2025-08-01 19:43:59
import tornado.ioloop
import tornado.web
import requests
from urllib.parse import urlparse
from datetime import datetime

# 定义一个URL验证的Handler
class URLValidatorHandler(tornado.web.RequestHandler):
    def get(self):
        # 获取URL参数
        url = self.get_argument('url')

        # 验证URL格式
        if not self.is_valid_url(url):
            self.write({'error': 'Invalid URL format'})
            return

        try:
            # 发送HEAD请求检查URL有效性
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                self.write({'message': 'URL is valid', 'status_code': response.status_code, 'checked_at': datetime.now().isoformat()})
            else:
                self.write({'message': 'URL is not valid', 'status_code': response.status_code})
        except requests.RequestException as e:
            # 处理请求异常
            self.write({'error': str(e)})

    def is_valid_url(self, url):
        """
        验证URL格式是否合法。
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

# 定义Tornado应用
def make_app():
    return tornado.web.Application([
        (r"/validate_url", URLValidatorHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # 设置监听端口
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()