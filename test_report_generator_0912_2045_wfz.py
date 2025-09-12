# 代码生成时间: 2025-09-12 20:45:57
import tornado.ioloop
import tornado.web
import json
import datetime
import os


# 定义一个TestReportGenerator类
class TestReportGenerator:
    def __init__(self, test_results):
        """初始化测试报告生成器"""
        self.test_results = test_results

    def generate_report(self, report_name):
        """生成测试报告"""
        try:
            # 确保测试结果不为空
            if not self.test_results:
                raise ValueError("Test results are empty")

            # 构建报告目录
            report_dir = "./reports/"
            if not os.path.exists(report_dir):
                os.makedirs(report_dir)

            # 生成报告文件名
            report_file = f"{report_dir}{report_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.html"

            # 将测试结果写入HTML文件
            with open(report_file, 'w') as f:
                f.write("<html><body>")
                for test_name, result in self.test_results.items():
                    f.write(f"<h3>{test_name}</h3>")
                    f.write(f"<p>Status: {result['status']}</p>")
                    f.write(f"<p>Duration: {result['duration']} seconds</p>")
                    f.write(f"<p>Output: {result['output']}</p>")
                f.write("</body></html>")

            return f"Report generated successfully: {report_file}"

        except Exception as e:
            return f"Failed to generate report: {str(e)}"


# 定义一个Tornado RequestHandler
class ReportHandler(tornado.web.RequestHandler):
    def post(self):
        """处理POST请求以生成测试报告"""
        try:
            # 解析请求体中的JSON数据
            test_results = json.loads(self.request.body)

            # 创建测试报告生成器实例
            report_generator = TestReportGenerator(test_results)

            # 生成测试报告
            report_name = "test"
            result = report_generator.generate_report(report_name)

            # 返回结果
            self.write(result)

        except json.JSONDecodeError:
            self.write("Invalid JSON data")
            self.set_status(400)
        except Exception as e:
            self.write(f"Error: {str(e)}")
            self.set_status(500)


# 定义Tornado应用和路由
def make_app():
    return tornado.web.Application([
        (r"/report", ReportHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Test report generator server is running on port 8888")
    tornado.ioloop.IOLoop.current().start()