from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

def loginView(request):
    if request.method=='GET':
        return render(request, 'MyAdmin/login.html', {})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request, user)
            #return redirect('mainmenu/')
            return render(request, 'MyAdmin/mainmenu.html', {})
        else:
            return render(request, 'MyAdmin/login.html', {})

def logout_view(request):
    logout(request)
    return render(request, 'MyAdmin/logout.html', {})
#    return redirect(loginView, {})
    #return render(request, 'home.html', {})
# Create your views here.

def baseexample(request):
    return render(request, 'MyAdmin/baseexample.html', {})

def homepage(request):
    return render(request, 'MyAdmin/home.html', {})

def about(request):
    return render(request,'MyAdmin/About.html')

def mainmenu(request):
    return render(request, 'MyAdmin/mainmenu.html', {})

def register(request):
    form = UserCreationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            #return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "MyAdmin/newuser.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "MyAdmin/newuser.html",
                  context={"form":form})
