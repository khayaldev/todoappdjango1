from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='home'),
    path('create/',views.createToDo,name='create'),
    path('todo/<id>/',views.todo_detail,name='todo'),
    path('delete/<id>/',views.todo_delete,name='delete'),
    path('update/<id>/',views.updateTodo,name='update'),
]
