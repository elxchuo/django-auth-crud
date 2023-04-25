from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate  # Crea la cookie
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# importar el formulario creado
from .forms import TaskForm

# importar para interactuar con la base de datos
from .models import Task


# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):  # Creando usuario

    if request.method == 'GET':
        # print("Enviando formulario")
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        # print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()  # nos crea las cookies para poner datos del usuario (con esa informacion se puede utilizar para saber si tiene acceso a diferentes paginas, si hay que guardar algo en el...)

                # return HttpResponse("User created successfully")

                login(request, user)
                # Cuando se crea un nuevo usuario redireccionar a la vista inicial
                return redirect('tasks')
            except:  # se pueden considerar excep para errores especificos.
                # Cuando el usuario ya existe
                # return HttpResponse("User already exist")
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "User already exist"
                })

        # Cuando las contrase;as no coinciden
        # return HttpResponse("Password do not match")
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': "Password do not match"
        })

@login_required
def tasks(request):  # tareas Pendientes 
    tasks = Task.objects.filter(user= request.user, datecompleted__isnull = True) #todas las consultas // Las del usuarios
    return render(request, 'tasks.html', {
        'tasks' : tasks
    })

@login_required
def tasks_completed(request):  # Crear tareas completas
    tasks = Task.objects.filter(user= request.user, datecompleted__isnull = False).order_by('-datecompleted') #todas las consultas // Las del usuarios
    return render(request, 'tasks.html', {
        'tasks' : tasks
    })

@login_required
def create_task(request):

    if request.method == "GET":
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        
        except ValueError:
            return render(request, 'create_task', {
                'form' :TaskForm,
                'error': 'Please provide valide data'
            })

@login_required
def task_detail(request, task_id):    
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        #print(task_id)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try: 
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task':task,
                'form':form,
                'error':"Error updating Task"
            })

@login_required
def complete_task(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        #print(task.datecompleted)
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request) 
    return redirect('home')

def signin(request):

    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        print(request.POST)
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "Username or Password is incorrect"
            })
        else:
            login(request, user)
            return redirect('tasks')
