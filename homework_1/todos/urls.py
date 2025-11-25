from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo-list'),
    path('create/', views.create_todo, name='create-todo'),
    path('update/<int:pk>/', views.update_todo, name='update-todo'),
    path('delete/<int:pk>/', views.delete_todo, name='delete-todo'),
]