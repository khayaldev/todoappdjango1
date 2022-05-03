from django.shortcuts import redirect, render, get_object_or_404
from todo.forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

def getshowing(request,todo):
 
  if request.GET and request.GET.get('filter'):
    if request.GET.get('filter')=='completed':
      return todo.filter(is_completed=True)
    elif request.GET.get('filter')=='uncomplete':
      return todo.filter(is_completed=False)
  return todo
 
  
@login_required
def index(request):
  todo=Todo.objects.filter(owner=request.user)
  completed=Todo.objects.filter(is_completed=True).count()
  uncompleted=Todo.objects.filter(is_completed=False).count()
  all=todo.count()
  context={"todo":getshowing(request,todo),"completed":completed,"uncompleted":uncompleted,"all":all}
  
  return render(request,'todo/index.html',context)

@login_required
def createToDo(request):
  form=TodoForm()
  context={'form':form}
  if request.method=='POST':
    title=request.POST.get('title')
    description=request.POST.get('description')
    is_completed=request.POST.get('is_completed',False)
    
    todo=Todo()
    todo.title=title
    todo.description=description
    todo.owner=request.user
    todo.is_completed=True if is_completed=='on' else False
    
    if todo.owner==request.user:
         todo.save()
         messages.success(request,'Your todo created succesfully')
    
         return HttpResponseRedirect(reverse('todo',kwargs={"id":todo.pk}))
    # redirect("todo",id=todo.pk)
  return render(request,'todo/create-todo.html',context)

@login_required
def todo_detail(request,id):
  todo=get_object_or_404(Todo,pk=id)
  print(todo)
  context={'todo':todo}
  return render(request,"todo/todo-detail.html",context)


@login_required
def todo_delete(request,id):
  todo=get_object_or_404(Todo,pk=id)
  context={'todo':todo}
  if request.method=='POST':
    if todo.owner==request.user:
      todo.delete()
      messages.error(request,'Your todo deleted')
      return redirect(reverse('home'))
  return render(request,"todo/delete-todo.html",context)



@login_required
def updateTodo(request,id):
  todo=get_object_or_404(Todo,pk=id)
  form=TodoForm(instance=todo)
  context={'todo':todo, 'form':form}
  if request.method=='POST':
    title=request.POST.get('title')
    description=request.POST.get('description')
    is_completed=request.POST.get('is_completed',False)
    
    todo.title=title
    todo.description=description
    todo.is_completed=True if is_completed=='on' else False
    if todo.owner==request.user:
      todo.save()
      messages.success(request,'Your todo updated   succesfully')
      return redirect('todo',id=todo.pk)
  
  return render(request,'todo/update-todo.html',context)
