from flask_admin.contrib.sqla import ModelView

from back_server import models


class NewsAdmin(ModelView):
    page_size = 25

    column_labels = {
        "id": "ID",
        "title": "标题",
        "abstract": "摘要",
        "url": "连接",
        "source": "来源",
        "keyword": "关键字",
        "savedate": "时间",
    }

    column_list = ["id", "title", "source", "savedate"]
    column_searchable_list = ["title", "source", "savedate"]


class FundAdmin(ModelView):
    page_size = 25
    create_modal = True
    edit_modal = True

    column_labels = {
        "id": "ID",
        "windcode": "证券代码",
        "category": "证券类型",
    }

    form_choices = {
        "category": [
            (1, "公募基金"),
            (2, "私募基金"),
            (3, "银行理财")
        ]
    }

    column_list = ["windcode", "category"]
    column_searchable_list = ["windcode"]
    column_filters = ["category"]
