# 代码生成时间: 2025-08-28 02:53:07
import tornado.ioloop
import tornado.web

# 用户权限模型
class UserPermission:
    def __init__(self, user_id, permissions):
        self.user_id = user_id
        self.permissions = permissions  # 权限列表

    def has_permission(self, permission):
        """检查用户是否有特定权限"""
        return permission in self.permissions

# 权限管理器
class PermissionManager:
    def __init__(self):
        self.users_permissions = {}

    def add_user(self, user_id, permissions):
        """添加用户及其权限"""
        self.users_permissions[user_id] = UserPermission(user_id, permissions)

    def get_user_permissions(self, user_id):
        """获取用户权限"""
        return self.users_permissions.get(user_id)

    def remove_user(self, user_id):
        """删除用户"""
        if user_id in self.users_permissions:
            del self.users_permissions[user_id]

# Tornado 路由处理器
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to the User Permission Management System")

class PermissionHandler(tornado.web.RequestHandler):
    def initialize(self, permission_manager):
        self.permission_manager = permission_manager

    def get(self, user_id, permission):
        user_permissions = self.permission_manager.get_user_permissions(user_id)
        if user_permissions and user_permissions.has_permission(permission):
            self.write(f"User {user_id} has permission {permission}")
        else:
            self.write(f"User {user_id} does not have permission {permission}", status=403)

# 设置 Tornado 应用程序
def make_app():
    permission_manager = PermissionManager()
    # 添加测试用户及其权限
    permission_manager.add_user('user1', ['read', 'write'])
    permission_manager.add_user('user2', ['read'])

    return tornado.web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/permission/([^/]+)/([^/]+)", PermissionHandler, dict(permission_manager=permission_manager)),
        ],
        debug=True,  # 开启调试模式
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()