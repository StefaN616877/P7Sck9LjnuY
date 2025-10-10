# 代码生成时间: 2025-10-10 17:20:41
import os
import time
from tornado.ioloop import IOLoop
from tornado.iostream import PipeIOStream
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileWatcher:
    """监控文件系统的变化，并在文件发生变化时进行通知。"""

    def __init__(self, path):
        """初始化文件监控器。"""
        self.path = path
        self.observer = Observer()

    def start(self):
        """开始监控文件系统变化。"""
        self.observer.schedule(self, self.path, recursive=True)
        self.observer.start()
        IOLoop.current().start()

    def stop(self):
        """停止监控文件系统变化。"""
        self.observer.stop()
        self.observer.join()

    class WatcherHandler(FileSystemEventHandler):
        """文件系统事件处理器。"""
        def on_modified(self, event):
            """当文件被修改时触发。"""
            if not event.is_directory:
                print(f'文件 {event.src_path} 被修改了。')

        def on_created(self, event):
            """当文件被创建时触发。"""
            if not event.is_directory:
                print(f'文件 {event.src_path} 被创建了。')

        def on_deleted(self, event):
            """当文件被删除时触发。"""
            if not event.is_directory:
                print(f'文件 {event.src_path} 被删除了。')

if __name__ == '__main__':
    # 设置要监控的目录
    path_to_watch = '/path/to/watch'
    file_watcher = FileWatcher(path_to_watch)
    file_watcher.start()  # 开始监控
    # 若要停止监控，在适当的时候调用 file_watcher.stop()

# 注意：
# 1. 确保已经安装了 watchdog 库（pip install watchdog）
# 2. 修改 path_to_watch 为实际需要监控的目录
