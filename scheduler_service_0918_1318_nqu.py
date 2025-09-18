# 代码生成时间: 2025-09-18 13:18:54
import tornado.ioloop
import tornado.web
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)


class ScheduledTask:
    """
    定时任务类，用于存储和执行任务
    """
    def __init__(self):
        self.tasks = defaultdict(list)

    def add_task(self, name, func, interval):
        """
        添加任务
        :param name: 任务名称
        :param func: 任务函数
        :param interval: 执行间隔
        """
        self.tasks[name].append((func, interval))

    def run(self):
        """
        运行所有任务
        "