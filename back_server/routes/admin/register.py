from flask_admin import Admin

from back_server.routes.admin.models import *


admin = Admin(name="后台管理")
admin.add_view(NewsAdmin(models.News, models.db.session, name="新闻"))
admin.add_view(FundAdmin(models.Funds, models.db.session, name="基金列表", category="基金筛选系统"))

