
from django.contrib import admin
from django.urls import path

from .views import (
    dashBoardPage,
    mySigninPage,
    signupPage,
    logoutPage,
    create_taskPage,
    task_listPage,
    create_categoryPage,
    taskEditPage,
    TaskCompleteViewPage,
    taskDeletePage,
    searchTaskPage,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signupPage, name='signupPage'),
    path('logoutPage/', logoutPage, name='logoutPage'),
    path('mySigninPage/', mySigninPage, name='mySigninPage'),
    path('dashBoardPage/', dashBoardPage, name='dashBoardPage'),
    path('create_taskPage/', create_taskPage, name='create_taskPage'),
    path('searchTaskPage/', searchTaskPage, name='searchTaskPage'),
    path('task_listPage/', task_listPage, name='task_listPage'),
    path('create_categoryPage/', create_categoryPage, name='create_categoryPage'),
    path('taskDeletePage/<str:myid>', taskDeletePage, name='taskDeletePage'),
    path('taskEditPage/<str:myid>', taskEditPage, name='taskEditPage'), 
    path('TaskCompleteViewPage/<str:myid>', TaskCompleteViewPage, name='TaskCompleteViewPage'),
]
