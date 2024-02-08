
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from myProject.forms import *
from django.contrib import messages
from datetime import date
from django.db.models import Q

def signupPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('mySigninPage')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signupPage.html', {'form': form})

def mySigninPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashBoardPage')
    else:
        form = AuthenticationForm()

    return render(request, 'loginPage.html', {'form': form})

def logoutPage(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('login_view')

def dashBoardPage(request):
    total_tasks = myTaskModel.objects.all().count()
    completed_tasks = myTaskModel.objects.filter(completed=True).count()
    upcoming_tasks = myTaskModel.objects.filter(completed=False, due_date__gt=date.today()).count()

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'upcoming_tasks': upcoming_tasks,
    }
    return render(request, 'dashBoardPage.html',context)

def create_taskPage(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_listPage')
    else:
        form = TaskForm()

    return render(request, 'create_taskPage.html', {'form': form})

def task_listPage(request):
    tasks=myTaskModel.objects.all()
    categories = TaskCategory.objects.all()

    return render(request,'task_listPage.html',{'tasks':tasks,'categories':categories})

def create_categoryPage(request):
    if request.method == 'POST':
        form = TaskCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('task_listPage')
    else:
        form = TaskCategoryForm()

    return render(request, 'create_category.html', {'form': form})


def taskEditPage(request, myid):
    task = get_object_or_404(myTaskModel, id=myid)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task) 
        if form.is_valid():
            form.save()
            return redirect("task_listPage")

    else:
        form = TaskForm(instance=task) 

    return render(request, 'taskEdit.html', {'form': form})

def taskDeletePage(request, myid):
    myTaskModel.objects.filter(id=myid).delete()
    messages.success(request, 'Task Delete Successfully!')

    return redirect('task_listPage')


def TaskCompleteViewPage(request, myid):

    task = get_object_or_404(myTaskModel, pk=myid, user=request.user)
    task.completed = True
    task.save()
    messages.success(request, 'Task Complete Successfully!')
    return redirect('task_listPage')

def searchTaskPage(request):
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('search', '')

    tasks = myTaskModel.objects.all()

    if category_filter:
        tasks = tasks.filter(category__id=category_filter)

    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    categories = TaskCategory.objects.all()

    return render(request, 'searchTaskPage.html', {'tasks': tasks, 'categories': categories})