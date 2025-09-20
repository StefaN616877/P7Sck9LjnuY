# 代码生成时间: 2025-09-21 01:03:38
import tornado.ioloop
import tornado.web
import schedule
import time

"""
定时任务调度器
使用Tornado框架实现一个简单的定时任务调度器
"""

class SchedulerService:
    def __init__(self):
        """初始化调度器"""
        self.job_list = []

    def add_job(self, job_func, job_interval):
        """
        添加定时任务
        :param job_func: 任务函数
        :param job_interval: 任务间隔（秒）
        """
        job = schedule.every(job_interval).seconds.do(job_func)
        self.job_list.append(job)
        schedule.every(job_interval).seconds.do(job_func)

    def start(self):
        """启动调度器"""
        schedule_thread = threading.Thread(target=self.run_scheduler)
        schedule_thread.start()

    def run_scheduler(self):
        """运行调度器"""
        while True:
            schedule.run_pending()
            time.sleep(1)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        "