# 代码生成时间: 2025-08-18 09:42:11
import os
import shutil
import json
import logging
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.options import define, options

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义备份和恢复的文件路径
BACKUP_DIR = "./backups"

# 定义选项
define("port