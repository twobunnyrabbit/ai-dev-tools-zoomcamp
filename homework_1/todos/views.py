from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo

def todo_list(request):
    todos = Todo.objects.all().order_by('-created_at')
    context = {
        'todos': todos
    }
    return render(request, 'todos/todo_list.html', context)

def create_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority', Todo.Priority.MEDIUM)
        
        if title:
            Todo.objects.create(
                title=title,
                description=description,
                priority=priority
            )
            return redirect('todo-list')
    
    return render(request, 'todos/create_todo.html')

def update_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.title = request.POST.get('title', todo.title)
        todo.description = request.POST.get('description', todo.description)
        todo.priority = request.POST.get('priority', todo.priority)
        todo.completed = 'completed' in request.POST
        todo.save()
        return redirect('todo-list')
    
    context = {
        'todo': todo
    }
    return render(request, 'todos/update_todo.html', context)

def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    
    if request.method == 'POST':
        todo.delete()
        return redirect('todo-list')
    
    context = {
        'todo': todo
    }
    return render(request, 'todos/delete_todo.html', context)
