from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.Home.as_view()), name='home'),
    path('add_to_do_list/', login_required(views.AddToDoList.as_view()), name='add_project'),
    path('edit_todolist/<int:id>/', login_required(views.EditToDoList.as_view()), name='edit_project'),
    path('add_task/<int:id>/', login_required(views.AddTask.as_view()), name='add_task'),
    path('edit_task/<int:id>/', login_required(views.EditTask.as_view()), name='edit_task')
]
