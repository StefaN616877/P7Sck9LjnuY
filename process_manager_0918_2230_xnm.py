# 代码生成时间: 2025-09-18 22:30:21
import os
import signal
import subprocess
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application


class ProcessManager(RequestHandler):
    """
    A Tornado RequestHandler for managing processes.
    It provides endpoints to start, stop, and list processes.
    """
    processes = {}

    def get(self):
        # List all managed processes
        self.write({'processes': list(self.processes.keys())})

    def post(self):
        # Start a new process
        command = self.get_argument('command')
        try:
            process = subprocess.Popen(command, shell=True)
            self.processes[process.pid] = process
            self.write({'success': True, 'pid': process.pid})
        except Exception as e:
            self.write({'success': False, 'error': str(e)})
            self.set_status(400)

    def delete(self, pid):
        # Stop a process by its PID
        if pid in self.processes:
            try:
                process = self.processes[pid]
                os.kill(process.pid, signal.SIGTERM)
                process.wait()
                del self.processes[pid]
                self.write({'success': True})
            except Exception as e:
                self.write({'success': False, 'error': str(e)})
                self.set_status(400)
        else:
            self.write({'success': False, 'error': 'Process not found'})
            self.set_status(404)


def make_app():
    """
    Create an instance of the Tornado Application.
    """
    return Application([
        (r"/", ProcessManager),
        (r"/(\d+)", ProcessManager),  # The \d+ is a regex for PID
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Process Manager started on http://localhost:8888")
    IOLoop.current().start()