from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('add_to_do_list/', views.AddToDoList.as_view(), name='add_project'),
    path('edit_todolist/<int:id>/', views.EditToDoList.as_view(), name='edit_project'),
    path('add_task/<int:id>/', views.AddTask.as_view(), name='add_task'),
    path('edit_task/<int:id>/', views.EditTask.as_view(), name='edit_task')
]
