from django.shortcuts import render,redirect
from noteapp.forms import TODOForm
from django.contrib import messages
from noteapp.models import TODO,Contact
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,"front.html")

def note(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login First")
        return redirect('/auth/signup')
    return redirect("home")

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user = user).order_by('priority')
        return render(request , 'index.html' , context={'form' : form , 'todos' : todos})

@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return redirect("home")
        else: 
            return render(request , 'index.html' , context={'form' : form})


def delete_todo(request , id ):
    print(id)
    TODO.objects.get(pk = id).delete()
    return redirect('home')

def change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')


def signout(request):
    logout(request)
    return redirect('login')

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"we will get back to you soon..")
        return render(request,"contact.html")


    return render(request,"contact.html")

# def signup(request):
#     return render(request,"signup.html")

# def signin(request):
#     return render(request,"login.html")

