
from django.urls import path

from tasks.views import *

urlpatterns = [
    path("", IndexView.as_view(),name='tasks'),
    path("task/<int:task_id>/<int:first_id>/<int:second_id>/",interact_task, name='task'),
    path("task/alter/<int:task_id>/<int:first_id>/<int:second_id>/",alter_value_assignment,name='alter_value_assignment'),
    path("upload",upload_task,name='upload'),
    path("my_tasks/<str:user_name_path>/",MytasksView.as_view(), name="my_tasks"),
    path("my_tasks/remove/<int:task_id>/", delete_task, name="delete_task"),
    path("my_tasks/edit/<int:task_id>/", edit_task, name="edit_task"),
    path("task/chat/<int:task_id>/<int:first_id>/<int:second_id>/",task_chat_page, name="task_chat_page"),
    path("my_tasks/chats/<str:user_name_path>/",MyTaskChatsView.as_view(), name="my_task_chats"),
    path("my_tasks/chat/<int:task_id>/<int:first_id>/<int:second_id>/",my_task_chat, name="my_task_chat_page")
]